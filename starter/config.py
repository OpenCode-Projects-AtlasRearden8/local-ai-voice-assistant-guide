"""House Voice — plain-text configuration. Edit this file; nothing else."""

import os

# What you call it (choose a phrase unlikely to appear in TV dialogue — see
# docs/02-wake-words.md for the honest comparison)
WAKE_WORD = "hey kitchen"

# Speech-to-text engine: "faster-whisper" (default), "vosk", or "push-to-talk"
STT_ENGINE = "faster-whisper"
STT_MODEL = "base.en"          # try "small.en" if kids will use it
INPUT_DEVICE_INDEX = None      # None = OS default; use device.py to list devices

# Where household data lives (plain files you can open any time)
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "house-data")

# The lists your household actually uses. Names here are what the router allows.
LISTS = {
    "grocery": "grocery list",
    "todo": "todo list",
    "kids": "kid list",
}

# Boundaries (see docs/06-kids-and-guests.md). Profile is one of:
#   "adult" — everything allowed
#   "family" — commands on, chat off
#   "kid"    — timers + own list only
#   "guest"  — timers + guest list only, resets to "family" after GUEST_TTL_MIN
PROFILE = "family"
GUEST_TTL_MIN = 120
QUIET_HOURS = ("20:30", "07:00")   # during quiet hours: no speech, list reads print only

# The brain (see docs/03-ollama-brain.md). No API keys — Ollama is local.
OLLAMA_MODEL = "llama3.2:3b"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
USE_OLLAMA = True            # if False (or Ollama is down), the rules parser takes over


if __name__ == "__main__":
    def show(name, value):
        if isinstance(value, dict):
            for key, sub in value.items():
                print(f"- list '{key}' (spoken as '{sub}')")
        elif isinstance(value, tuple) and len(value) == 2:
            print(f"- {name.replace('_', ' ')}: from {value[0]} to {value[1]}")
        elif isinstance(value, (int, float)):
            print(f"- {name.replace('_', ' ')}: {value}")
        else:
            print(f"- {name.replace('_', ' ')}: {value}")
            if name == "DATA_DIR" and not os.path.isdir(value):
                print("  (folder will be created on first run — that's normal)")

    print("House Voice is configured to:")
    show("wake_word", WAKE_WORD)
    show("stt_engine", STT_ENGINE)
    show("stt_model", STT_MODEL)
    show("lists", LISTS)
    show("current_profile", PROFILE)
    show("quiet_hours", QUIET_HOURS)
    show("brain_model", OLLAMA_MODEL)
    show("data_dir", DATA_DIR)
