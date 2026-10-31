# The Two-Evening Build Plan

This chapter is the whole manual sequenced into two evenings, with a checkpoint after
every step so you always know the machine is working *right now*. Total wall-clock
time: roughly 2 hours the first evening, 2–3 the second. If an evening goes sideways,
the [troubleshooting table](troubleshooting.md) has a row for every failure mode we've
heard of, and
[chapter 7](07-when-cloud-is-simpler.md) is the permanent no-guilt fallback.

The scripts referenced here live in the `starter/` folder of this repo. They're small
on purpose; read them before (or while) running them.

## Before Evening 1 (5 minutes, do it whenever)

- [ ] Front half of [chapter 1](01-parts-and-hardware.md): confirm your Tier 1 setup
      (existing computer + its mic/speaker) or plug in whatever you bought.
- [ ] ~10 GB free disk space on that machine.
- [ ] Admin access to it (`sudo` / Administrator).
- [ ] Internet available *now* — this is the last time the build needs it.

## Evening 1 — brain and ears (steps below, in order)

### Step 1 (10 min): install Ollama and pull a model

Follow [chapter 3](03-ollama-brain.md)'s short install, then:

```bash
ollama pull llama3.2:3b
```

**Checkpoint:** `ollama run llama3.2:3b "Say the word pineapple"` prints the word
pineapple. (Not the fruit — the *word*, typed back by your own computer, offline.)

### Step 2 (15 min): install Python tools and the speech-to-text engine

```bash
python3 -m venv ~/house-voice-venv
source ~/house-voice-venv/bin/activate     # Windows: venv\Scripts\activate
pip install faster-whisper
```

**Checkpoint:** in the same terminal, `python3 -c "import faster_whisper"` prints
nothing (which is Python's version of a silent success — no error is the win).

**Note:** On Windows, replace the `source …` line with the activate command shown.
On a Raspberry Pi or old machine, use `pip install vosk` instead and set
`STT_ENGINE = "vosk"` in `starter/config.py` — see
[chapter 4](04-offline-speech-to-text.md).

### Step 3 (25 min): copy the starter scripts and wire them

```bash
# copy the repo's starter/ folder to a home for it, e.g.:
cp -r /path/to/this/repo/starter ~/house-voice
cd ~/house-voice
```

Then open `starter/config.py` once and set three plain-text things: your wake word
from [chapter 2](02-wake-words.md), your household's list names, and quiet hours from
[chapter 6](06-kids-and-guests.md). Nothing else needs editing.

**Checkpoint:** `python3 config.py` runs and prints your settings back as plain
sentences, so you can *read* what you configured.

### Step 4 (20 min): test the pipeline by typing instead of talking

```bash
python3 household.py --text "set a timer for 10 minutes for the pasta"
```

This skips the microphone entirely — the router gets your sentence as typed text,
hands it to Ollama for parsing, does the plain-script sanity check, sets the timer,
speaks it back. Typing-first is the secret sauce of the whole build: **it separates
"does the brain work" from "does the microphone work," and you'll never fix two
broken things at once.**

**Checkpoint:** it says (out loud, through your speakers) that a 10-minute pasta timer
is running, and a line appears in `house-data/log.txt` recording exactly what happened.

**Second checkpoint (two minutes later):** at zero, the timer chimes audibly.

*If Evening 1 ended here, you have: an offline LLM that parses sentences, a working
timer voice, and a readable log. That's a real milestone; celebrate it.*

## Evening 2 — the microphone, the wake word, guests

### Step 5 (20 min): give it a microphone

Install one small audio-capture dependency (this is the step most likely to need a
helping hand from the mic-rows of [chapter 1](01-parts-and-hardware.md)):

```bash
pip install sounddevice
python3 household.py --text "test microphone"   # dry-run wiring check if mic isn't detected
```

Then say, out loud and nearby: **"set a timer for one minute."**

**Checkpoint:** log shows a heard transcript roughly matching that sentence, and a
60-second timer running. Ears attached.

### Step 6 (30 min): the wake word, honestly chosen

Install the openWakeWord path from
[chapter 2](02-wake-words.md) — or the push-to-talk alternative, which is *zero
install* if evenings are running out of runway. Then run:

```bash
python3 household.py --listen    # the real thing: wake word → mic → LLM → command
```

**Checkpoint:** say the wake word, pause, say "set a timer for one minute." Log shows
two entries: the wake event, and the command. If it never wakes, that's not a crisis —
it's troubleshooting row 4, and the fix is usually mic distance or a too-common phrase
(just like [chapter 2](02-wake-words.md) warned).

### Step 7 (25 min): boundaries before bedtime

Flip through [chapter 6](06-kids-and-guests.md)'s three modes now, because this is the
10-minutes-before-bedtime step where tired judgment is at its worst:

- Test `kid` mode: confirm `CHAT` is refused and a timer still works.
- Set quiet hours in `config.py` and confirm the screen goes polite.
- Say "goodnight" while in adult mode and confirm it goes mute until morning.

**Checkpoint:** the assistant does something you *didn't want* and it refuses —
politely, verifiably, in the log. Deliberately trying to break it now is the family
game that pays for itself later.

### Step 8 (15 min): autostart

Make it survive reboots: a `systemd --user` service (Linux), a LaunchAgent (macOS),
or a Task Scheduler entry (Windows) that runs `python3 household.py --listen` at
login. One-time setup, no code changes. The exact unit is in `starter/` with comments
for each OS.

**Checkpoint (the final one):** reboot. Wait for boot. Say the wake word. It answers.

## House rules, day one

Print the [family rules card](06-kids-and-guests.md) and tape it nearby. Say the four
lines out loud at dinner. Done — this is now a *house appliance*, not a project.

## After the two evenings

- Leave it running for a week before changing anything. Collect the moments it
  misunderstands (they're all in `log.txt`); tune the [prompt and commands](05-household-commands.md)
  in one sitting.
- The [parts checklist](01-parts-and-hardware.md)-Tier-3 upgrade, custom wake-word
  training, or whisper `small.en` for kids' voices — those are the third-weekend
  adventures. Not rushed.
- And keep [chapter 7](07-when-cloud-is-simpler.md) alive in your head: the kitchen
  speaker can still be the cloud one, and that was never a defeat.
