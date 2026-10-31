# STATUS — The House Voice (local-ai-voice-assistant-guide)

Last verified: Oct 31, 2026. All tests pass (30/30) and the site builds clean.

## What was built

A friend-paced manual for a **private, local, offline home voice assistant**, from
Asdale Dynamics, LLC. No accounts, no API keys, no subscriptions anywhere in the
build or its instructions.

- **`docs/` — the manual (11 chapters):**
  `index.md` (start here), `01-parts-and-hardware.md` (mic/speaker tiers + printable
  parts checklist), `02-wake-words.md` (openWakeWord vs Porcupine vs ESP32-S3 vs
  push-to-talk, honestly graded), `03-ollama-brain.md` (the strict
  sentence-to-JSON-command trick), `04-offline-speech-to-text.md`
  (faster-whisper/whisper.cpp/Vosk), `05-household-commands.md` (timers, lists,
  quiet hours, plain-file data), `06-kids-and-guests.md` (allowlists in code, family
  rules card, kill switch), `07-when-cloud-is-simpler.md` (the contrarian chapter),
  `08-two-evening-plan.md` (checkpointed two-evening build), plus
  `troubleshooting.md` (20-row symptom/cause/fix table) and `glossary.md`.
- **`starter/` — runnable, keyless scripts:** `config.py` (plain-text settings,
  readable printout), `household.py` (one script: lists + timers + speech out +
  router + allowlists + CLI `--text/--listen/--profile`), `listen.py` (mic helper
  with push-to-talk fallback and typed-input fallback), `device.py`
  (troubleshooting helper), `systemd/house-voice.service` (autostart unit).
  Designed to work with zero dependencies: with no microphone stack and no Ollama
  installed, the rules-based fallback parser still runs the whole command pipeline.
- **`build.py` + `build.sh` + `assets/style.css` — the static site builder:**
  converts `docs/*.md` to `site/*.html` (python-markdown, tables/fenced-code
  extensions), rewrites `.md` links to `.html`, injects nav + footer credit.
- **`tests/` — homegrown suite, no test framework needed:** `tests/run_tests.sh`
  → `tests/test_all.py` (plain `unittest`).
- **`README.md`** (credit to Asdale Dynamics, LLC; positioning against the two
  companion guides), **`LICENSE`** (MIT, © 2026 Asdale Dynamics, LLC), `.gitignore`.

Positioning vs. companion guides (no repetition): *The Local AI Handbook* owns
general local-AI theory and Ollama install depth; *Voice Assistants: A Comfort
Guide* owns the "should your household have one" question; this manual owns the
hands-on two-evening build.

## How to run it

```bash
./build.sh                 # builds site/ from docs/ (needs: pip install markdown)
open site/index.html       # read the manual
./tests/run_tests.sh       # full test suite (30 tests)
# starter/ scripts (after copying to a home folder, per chapter 8):
python3 starter/config.py                       # print your configuration
python3 starter/household.py --text "set a timer for 10 minutes for the pasta"
python3 starter/household.py --text "read the grocery list" --profile kid
python3 starter/household.py --listen           # full voice loop (mic required)
```

## Verification results (all run in this workspace)

1. `./tests/run_tests.sh` → **OK, 30/30**, covering:
   - **Build:** `build.sh` exits 0, produces 11 HTML pages + `style.css`; every
     internal `.html` link in every generated page resolves; every `.md` link in
     docs resolves; companion-guide references present.
   - **No-secrets scan:** repo-wide regex scan for key-like strings
     (sk-/AKIA/ghp_/xox/pepkeen/private-key blocks/bearer tokens/api_key=) → none.
   - **No-account check:** no fenced command block anywhere in docs requires an
     account, signup, access key, or API key.
   - **Starter logic (offline):** rules parser (timers incl. hours, list add/read/
     remove, remove-last, TIME_NOW, CHAT fallback, cancel), `sanitize`
     gatekeeper (out-of-range timers, non-numeric, unknown/imposter list names,
     `RUN_SHELL` rejected — the load-bearing no-arbitrary-code guarantee),
     allowlists (kid blocks chat + adult lists; guest blocks lists + chat; family
     blocks chat), `act` refusal logging, list round-trips via `lists.json`,
     timer set/cancel/bounds/fires-and-logs, quiet-hours print-only path,
     logged readable transcript, documented CLI commands via subprocess
     (`--text`, `config.py`).
2. `python3 -m py_compile` on all Python files → clean.
3. `./build.sh` twice (from clean and dirty states) → 11 pages each time.
4. Live CLI smoke test (no Ollama present): `--text` timer/list/read/cancel all
   behaved, log + `lists.json` on disk in plain text as documented.

## How the tests fake what's absent

The suite swaps `household`'s data-dir globals into a temp folder per test
(restored by saving/restoring `household.__dict__`), silences the OS speaker
(`say`), and pins `in_quiet_hours` to a deterministic value. The no-Ollama path is
a *feature*: the rules parser is the documented fallback brain, so tests exercise
the real pipeline, not a mock of it.

## Known gaps / honest limitations

- **No audio hardware here.** The mic-loop path (`--listen`, `listen.py`) is
  written defensively — push-to-talk fallback, typed-input fallback, device
  listing for troubleshooting rows 6–7 — but was not exercised against a real
  microphone in this workspace. Chapter 8's checkpoints cover that on a real box.
- **Ollama path not live-tested** in this environment (binary not installed).
  Documented commands are standard Ollama usage; the LLM parser is also exercised
  indirectly via its testable contract (strict JSON, `format: "json"`).
- **`--listen` wake-word detection requires `pip install openwakeword
  sounddevice soundfile`** on a real machine — deliberately not auto-installed,
  since chapters 2 and 4 walk those choices; the starter degrades gracefully
  without them.
- **Windows/macOS autostart paths** are described in chapter 8 text; only the
  Linux systemd unit ships as a file.
- **No speaker-recognition (voice ID)** — an intentional near-term omission,
  documented honestly in chapter 6 (profile is a switch, not a voiceprint).
- README links to the companion guides descriptively; if/when those repos are
  public at their final URLs, add explicit links.

## Repo hygiene

- Git initialized; single-ish plain commits, no Co-authored-by trailers, committed
  as the existing local identity only (`Dylan Asdale
  <dylanasdale@users.noreply.github.io>`).
- Never pushed; no remote configured; nothing published.
- `site/` and `starter/house-data/` are generated at runtime and gitignored.
- No secrets, API keys, or personal data in any file (verified by test).
