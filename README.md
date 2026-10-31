# The House Voice

A friend-paced, fully offline manual for building your own private home voice
assistant — wake word, local LLM brain, offline speech-to-text, and scriptable
household commands (timers, lists, quiet hours, kid and guest modes) — with **no
accounts, no API keys, and no subscriptions** at any step.

Two evenings, one computer, zero cloud. Every script is small, readable, and yours
to change; all household data lives in plain text files you can open any time.

## What's in this repo

| Path | What it is |
|---|---|
| `docs/` | The manual — 11 markdown chapters |
| `starter/` | Copy-paste-ready scripts (`config.py`, `household.py`, `listen.py`, `device.py`, `systemd/`) used by the [two-evening build plan](docs/08-two-evening-plan.md) |
| `assets/`, `build.py`, `build.sh` | The static-site builder (stdlib + one `pip install markdown`) |
| `tests/` | The test suite (`./tests/run_tests.sh`) |
| `site/` | Generated HTML (created by `./build.sh`; not committed) |

## The manual, chapter by chapter

1. [Parts and hardware](docs/01-parts-and-hardware.md) — including the "use what you
   already have" tier and the printable parts checklist
2. [Wake words, honestly compared](docs/02-wake-words.md) — openWakeWord, Porcupine,
   ESP32-S3, and the push-to-talk cheat
3. [Ollama as the brain](docs/03-ollama-brain.md) — the strict-command trick that
   makes a small local model reliable
4. [Offline speech-to-text](docs/04-offline-speech-to-text.md) — faster-whisper vs
   Vosk vs whisper.cpp
5. [Household commands](docs/05-household-commands.md) — timers, lists, rituals, one
   small script
6. [Kids and guests](docs/06-kids-and-guests.md) — boundaries enforced in code, with
   a family rules card and a kill switch
7. [When a cloud assistant is honestly simpler](docs/07-when-cloud-is-simpler.md) —
   the contrarian chapter; nobody is failing a test by keeping both
8. [The two-evening build plan](docs/08-two-evening-plan.md) — every step checkpointed
9. [Troubleshooting table](docs/troubleshooting.md), [Glossary](docs/glossary.md)

## How to read it / build the site

```bash
./build.sh          # converts docs/*.md -> site/*.html
open site/index.html
```

Requirements: Python 3 with the `markdown` package (`pip install markdown`).
Everything else — the assistant itself — needs only what
[chapter 8](docs/08-two-evening-plan.md) installs, and once installed, runs offline.

## Where this fits in the family

This manual is one of three friendly guides from Asdale Dynamics, LLC, each owning a
different slice:

- **The Local AI Handbook** — local AI in general: what LLMs are, picking models, and
  installing Ollama on any machine. Read it for the general theory; this manual
  deliberately doesn't repeat it.
- **Voice Assistants: A Comfort Guide** — whether voice is right for your household,
  placement and etiquette, and the human side of living with a talking device. This
  manual is the hands-on "how"; that's the "should we."
- **The House Voice (this repo)** — the concrete two-evening build.

## Design promises

- **No accounts. No API keys. Ever.** Tools that require them (like Porcupine's
  access key) are described honestly and then passed over for keyless equivalents.
- **No network code.** The only network call in the starter scripts is to Ollama on
  `127.0.0.1` — the brain that lives on your own machine — and it's optional.
- **Plain-file data.** Lists and logs are human-readable files in `house-data/`.
- **Tested.** `./tests/run_tests.sh` builds the site, checks every internal link,
  scans the repo for accidental secrets, and exercises the router logic
  (parsing, sanitize, allowlists, timers) without needing a microphone or a GPU.
- **When cloud is simpler, we say so** — see
  [chapter 7](docs/07-when-cloud-is-simpler.md).

## License & credit

MIT — see [LICENSE](LICENSE). © 2026 Asdale Dynamics, LLC. Built by
[Asdale Dynamics, LLC](https://dylanasdale.github.io) — beginner-friendly AI
education, books, and practical local-first tools, explained like a friend would.

*Education only. Nothing here is medical, legal, or financial advice — not even a
little bit.*
