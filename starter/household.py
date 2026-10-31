"""House Voice — one small script: lists, timers, the router, and the CLI.

Design rules (from docs/05-household-commands.md):
  - The LLM only *suggests* commands; this script decides, with allowlists.
  - No network code anywhere except localhost Ollama (optional, keyless).
  - Data lives in plain files you can open with your eyes (house-data/).
  - If Ollama is down or off, the rules parser below takes over.

Usage:
  python3 household.py --text "set a timer for 10 minutes for the pasta"
  python3 household.py --text "read the grocery list" --profile kid
  python3 household.py --listen     # full voice loop (mic required)
"""

import argparse
import datetime
import json
import math
import os
import re
import struct
import subprocess
import sys
import threading
import urllib.request
import wave

import config


os.makedirs(config.DATA_DIR, exist_ok=True)
LISTS_PATH = os.path.join(config.DATA_DIR, "lists.json")
LOG_PATH = os.path.join(config.DATA_DIR, "log.txt")
CHIME_PATH = os.path.join(config.DATA_DIR, "chime.wav")

_active_timers = []


# ---------- lists (stored in house-data/lists.json) ----------


def load_lists():
    if not os.path.exists(LISTS_PATH):
        return {name: [] for name in config.LISTS}
    with open(LISTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_lists(lists):
    with open(LISTS_PATH, "w", encoding="utf-8") as f:
        json.dump(lists, f, indent=2, ensure_ascii=False)


def add_to_list(list_name, item):
    lists = load_lists()
    if list_name not in lists:
        return f"I don't have a list called '{list_name}'."
    if not item or not str(item).strip():
        return "What should I add?"
    item = str(item).strip()
    lists[list_name].append((item, datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
    save_lists(lists)
    return f"Added {item} to the {config.LISTS.get(list_name, list_name)}."


def remove_last(list_name):
    lists = load_lists()
    if list_name not in lists or not lists[list_name]:
        return f"The {list_name} list is already empty."
    item, _ts = lists[list_name].pop()
    save_lists(lists)
    return f"Removed {item} from the {list_name} list."


def read_list(list_name, speak=True):
    lists = load_lists()
    if list_name not in lists:
        return f"I don't have a list called '{list_name}'."
    if not lists[list_name]:
        return f"The {list_name} list is empty."
    lines = list(reversed(lists[list_name]))          # newest first, like a memory
    spoken = ", ".join(item for item, _ts in lines)
    numbered = "\n".join(f"{i}. {item}" for i, (item, _ts) in enumerate(lines, 1))
    if speak:
        return f"The {list_name} list has {len(lines)} things: {spoken}"
    return numbered


# ---------- timers (plain threads; they die if the computer reboots) ----------


def make_chime():
    """Write a short two-tone chime wav once, so the OS's own player can play it."""
    if os.path.exists(CHIME_PATH):
        return CHIME_PATH
    rate, half = 22050, 22050 // 4                    # quarter-second per tone
    frames = b""
    for freq, reps in ((660, 1), (880, 2)):
        for _ in range(reps):
            for i in range(half):
                env = 1 - i / half                     # fade out, no click
                sample = int(6000 * env * math.sin(2 * math.pi * freq * i / rate))
                frames += struct.pack("<h", sample)
    with wave.open(CHIME_PATH, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(frames)
    return CHIME_PATH


def _play(cmd_args):
    try:
        subprocess.run(cmd_args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       check=False)
    except FileNotFoundError:                          # player may not exist — fine
        pass


def play_sound():
    chime = make_chime()
    if sys.platform == "darwin":
        _play(["afplay", chime])
    elif sys.platform.startswith("linux"):
        for player in ("paplay", "aplay"):
            if subprocess.run(["which", player], capture_output=True).returncode == 0:
                _play([player, chime])
                return
        _play(["play", chime])
    elif sys.platform == "win32":
        _play(["powershell", "-c",
               f"(New-Object Media.SoundPlayer '{chime}').PlaySync();"])


def timer_done(label):
    ms = f" ({label})" if label else ""
    play_sound()
    say(f"Timer done{ms}. Time's up.")
    log(f"TIMER_DONE label={label!r}")


def set_timer(minutes, label=None):
    try:
        minutes = float(minutes)
    except (TypeError, ValueError):
        return "That timer number didn't come through as a number."
    if not (1 <= minutes <= 600):
        return f"{minutes:g} is outside my 1-to-600-minute range."
    t = threading.Timer(minutes * 60, timer_done, [label])
    t.daemon = True
    t.start()
    _active_timers.append(t)
    pretty = f"{minutes:g} minute{'s' if minutes != 1 else ''}"
    return f"Timer set: {pretty}" + (f" for {label}" if label else "") + "."


def cancel_timer():
    if not _active_timers:
        return "No timer running."
    _active_timers.pop().cancel()
    return "Timer cancelled."


# ---------- voice out + the log ----------


def say(text):
    """Print always; speak best-effort with whatever OS voice exists."""
    print(f"ASSISTANT: {text}", flush=True)
    spoken = text.replace('"', "'")[:300]
    try:
        if sys.platform == "darwin":
            subprocess.run(["say", spoken], check=False, timeout=30)
        elif sys.platform.startswith("linux"):
            for tts in ("espeak-ng", "espeak"):
                if subprocess.run(["which", tts], capture_output=True).returncode == 0:
                    subprocess.run([tts, spoken], check=False, timeout=30)
                    return
        elif sys.platform == "win32":
            subprocess.run(["powershell", "-c",
                            f"Add-Type -AssemblyName System.Speech;"
                            f"(New-Object System.Speech.Synthesis.SpeechSynthesizer)"
                            f".Speak('{spoken}')"], check=False, timeout=30)
    except Exception:
        pass  # voice is a nicety; the printed line above is the contract


def log(line):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} | {line}\n")


def reset_for_tests():
    _active_timers.clear()


# ---------- the intent model (what any parser must return) ----------

COMMANDS = frozenset(("SET_TIMER", "CANCEL_TIMER", "ADD_TO_LIST", "READ_LIST",
                      "REMOVE_LAST", "TIME_NOW", "CHAT"))


class Intent:

    def __init__(self, command, args=None):
        self.command = command
        self.args = dict(args or {})

    def __eq__(self, other):
        return (self.command, self.args) == (other.command, other.args)

    def __repr__(self):
        return f"Intent({self.command!r}, {self.args!r})"


# ---------- sanity checks (the gatekeeper) ----------


def sanitize(intent):
    """Force a parser's suggestion through plain if-statements, or reject it."""
    if intent.command not in COMMANDS:
        return Intent("CHAT", {"text": "(refused unclear command)"})
    if intent.command == "SET_TIMER":
        try:
            minutes = float(intent.args.get("minutes"))
        except (TypeError, ValueError):
            return Intent("CHAT", {"text": "(couldn't parse timer length)"})
        if not (1 <= minutes <= 600):
            return Intent("CHAT", {"text": "(timer length out of range)"})
        label = intent.args.get("label")
        label = str(label).strip() if label and str(label).strip() else None
        return Intent("SET_TIMER", {"minutes": minutes, "label": label})
    if intent.command in ("ADD_TO_LIST", "READ_LIST", "REMOVE_LAST"):
        list_name = intent.args.get("list")
        if list_name not in config.LISTS:
            return Intent("CHAT", {"text": f"(unknown list {list_name!r})"})
        if intent.command == "ADD_TO_LIST":
            item = str(intent.args.get("item", "")).strip()
            if not item:
                return Intent("CHAT", {"text": "(missing item to add)"})
            return Intent("ADD_TO_LIST", {"list": list_name, "item": item})
        return Intent(intent.command, {"list": list_name})
    if intent.command == "CHAT":
        text = str(intent.args.get("text", "")).strip()
        return Intent("CHAT", {"text": text}) if text else Intent("TIME_NOW")
    return intent


# ---------- allowances (kids and guests, docs/06-kids-and-guests.md) ----------

KID_ALLOWED = frozenset(("SET_TIMER", "CANCEL_TIMER", "ADD_TO_LIST",
                         "READ_LIST", "TIME_NOW"))
GUEST_ALLOWED = frozenset(("SET_TIMER", "CANCEL_TIMER", "TIME_NOW"))


def allowed(intent, profile=None):
    profile = profile or config.PROFILE
    if intent.command == "CHAT":
        return profile == "adult"                     # chat is off unless adult-mode
    if profile == "adult":
        return intent.command in COMMANDS
    if profile == "family":
        return intent.command in COMMANDS - {"CHAT"}
    if profile == "kid":
        if intent.command in ("ADD_TO_LIST", "READ_LIST"):
            return intent.args.get("list") == "kids"
        return intent.command in KID_ALLOWED
    if profile == "guest":
        return intent.command in GUEST_ALLOWED
    return False


# ---------- parsers: rules first (instant, offline), LLM second (flexible) ----------


def parse_with_rules(text):
    """Plain regexes — the fallback brain that needs nothing installed."""
    t = text.lower().strip()
    m = (re.search(r"(?:for|in|after)\s+(\d+(?:\.\d+)?)\s*(minutes?|mins?|hours?|hrs?)", t)
         or re.search(r"^(\d+(?:\.\d+)?)\s*(minutes?|mins?|hours?|hrs?)", t))
    if m and re.search(r"timer|remind|alarm|wake", t):
        value = float(m.group(1))
        if re.search(r"hours?|hrs?", m.group(2)):
            value *= 60
        label_m = re.search(r"\bfor the ([a-z ]{3,40})$", t)
        label = label_m.group(1).strip() if label_m else None
        return sanitize(Intent("SET_TIMER", {"minutes": value, "label": label}))
    if "timer" in t and re.search(r"cancel|stop|never mind", t):
        return Intent("CANCEL_TIMER")
    m = re.search(r"add\s+(?P<item>.+?)\s+to(?:\s+the)?\s+(?P<target>\w+)\s*list$", t)
    if m:
        target = _resolve_list(m.group("target"))
        return sanitize(Intent("ADD_TO_LIST", {"item": m.group("item"), "list": target}))
    m = re.search(r"(?:read|show|what.?s on)\s?(?:the)?\s*(\w+)", t)
    if m and re.search(r"list|read|what's on", t):
        return sanitize(Intent("READ_LIST", {"list": _resolve_list(m.group(1))}))
    m = re.search(r"remove (?:the )?last (?:thing|item) from (?:the )?(\w+)", t)
    if m:
        return sanitize(Intent("REMOVE_LAST", {"list": _resolve_list(m.group(1))}))
    if re.search(r"what time|time is it", t):
        return Intent("TIME_NOW")
    return Intent("CHAT", {"text": text})


def _resolve_list(word):
    word = (word or "").lower()
    return next((name for name in config.LISTS if name.startswith(word)), word)


LLM_PROMPT = """You are the command parser for a household voice assistant.
Allowed commands: SET_TIMER, CANCEL_TIMER, ADD_TO_LIST, READ_LIST, REMOVE_LAST, TIME_NOW, CHAT.
Lists that exist: {lists}.
Respond ONLY with a single JSON object, no other text:
{{"command":"...","args":{{...}}}}
Examples:
"set a timer for 10 minutes for the pasta" -> {{"command":"SET_TIMER","args":{{"minutes":10,"label":"pasta"}}}}
"add milk to the grocery list" -> {{"command":"ADD_TO_LIST","args":{{"list":"grocery","item":"milk"}}}}
"what's on the todo list" -> {{"command":"READ_LIST","args":{{"list":"todo"}}}}
"do penguins like jazz" -> {{"command":"CHAT","args":{{"text":"do penguins like jazz"}}}}
Sentence: {sentence}
JSON:"""


def parse_with_ollama(text):
    payload = json.dumps({
        "model": config.OLLAMA_MODEL,
        "prompt": LLM_PROMPT.format(lists=", ".join(config.LISTS),
                                    sentence=text.strip()),
        "stream": False,
        "format": "json",
    }).encode("utf-8")
    req = urllib.request.Request(config.OLLAMA_URL, data=payload,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    parsed = body.get("response", {})
    if isinstance(parsed, str):
        parsed = json.loads(parsed)
    return sanitize(Intent(parsed.get("command", "CHAT"), parsed.get("args") or {}))


def parse(text):
    """Rules first (instant, always works); Ollama only for the messy leftovers."""
    intent = parse_with_rules(text)
    if intent.command != "CHAT" or not config.USE_OLLAMA:
        return intent
    try:
        llm_intent = parse_with_ollama(text)
    except Exception:
        return intent                                  # stay offline and honest
    return llm_intent if allowed(llm_intent) else sanitize(llm_intent)


# ---------- acting on intents ----------


def act(intent, profile=None, speak=None):
    profile = profile or config.PROFILE
    speak = speak or say
    if not allowed(intent, profile):
        text = ("that one's not in my kid mode." if profile == "kid"
                else "that one's for the grown-ups.")
        speak(f"Sorry, {text}")
        log(f"REFUSED [{profile}] {intent}")
        return
    if intent.command == "SET_TIMER":
        reply = set_timer(intent.args["minutes"], intent.args.get("label"))
    elif intent.command == "CANCEL_TIMER":
        reply = cancel_timer()
    elif intent.command == "ADD_TO_LIST":
        reply = add_to_list(intent.args["list"], intent.args["item"])
    elif intent.command == "READ_LIST":
        reply = read_list(intent.args["list"], speak=profile != "kid")
    elif intent.command == "REMOVE_LAST":
        reply = remove_last(intent.args["list"])
    elif intent.command == "TIME_NOW":
        reply = f"It's {datetime.datetime.now().strftime('%I:%M %p').lstrip('0')}."
    else:                                              # CHAT
        reply = ("I keep to household commands in this profile. "
                 "Try a timer or a list.")
    speak(reply)
    log(f"{intent.command} {intent.args} -> {reply}")


def in_quiet_hours():
    start, end = config.QUIET_HOURS
    now = datetime.datetime.now().strftime("%H:%M")
    return now >= start or now < end                   # wraps over midnight


def run_text(sentence, profile=None):
    """The typed pipeline — the whole system minus the microphone."""
    if profile:
        config.PROFILE = profile
    log(f"HEARD(text) {sentence!r}")
    if in_quiet_hours() and config.PROFILE != "adult":
        print("ASSISTANT: (quiet hours — printing only, not speaking)")
        act(parse(sentence), speak=lambda reply: print(f"ASSISTANT: {reply}"))
        return
    act(parse(sentence))


def main():
    ap = argparse.ArgumentParser(description="House Voice assistant")
    ap.add_argument("--text", help="run one sentence as typed text")
    ap.add_argument("--listen", action="store_true",
                    help="run the full voice loop (mic required)")
    ap.add_argument("--profile", choices=["adult", "family", "kid", "guest"])
    args = ap.parse_args()
    if args.listen:
        voice_loop()                                   # imports mic deps lazily
    elif args.text:
        run_text(args.text, args.profile)
    else:
        ap.print_help()


def voice_loop():
    """Wake word -> record -> transcribe -> run_text. Mic deps load lazily."""
    import listen
    stt = listen.get_stt()
    import sounddevice as sd
    print(f"House Voice is listening for '{config.WAKE_WORD}' "
          f"(profile: {config.PROFILE}). Ctrl-C to stop.")
    while True:
        if listen.detect_wake_word():
            log("WAKE")
            path = listen.record_sentence(sd, stt)
            text = listen.transcribe(stt, path)
            log(f"HEARD(voice) {text!r}")
            if text:
                run_text(text)


if __name__ == "__main__":
    main()
