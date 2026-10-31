# Troubleshooting Table

Every failure mode we've heard of, in the format *symptom → most likely cause → fix*.
Rows are ordered roughly by when you'll hit them across
[the two-evening plan](08-two-evening-plan.md). The general-first rule: **the
[household log](05-household-commands.md) (`house-data/log.txt`) tells you which of
the three stages failed** — heard nothing, heard wrong, or heard right and did
nothing. Check it before anything else.

| # | Symptom | Most likely cause | Fix |
|---|---|---|---|
| 1 | `ollama` command not found | Install didn't finish or PATH wasn't refreshed | Close and reopen the terminal; reinstall from [chapter 3](03-ollama-brain.md) if still missing. |
| 2 | `ollama pull` stalls at 0% | Not actually about the network — usually disk full | Free the ~10 GB from the [parts checklist](01-parts-and-hardware.md); retry. |
| 3 | Ollama answers, but *slowly* (10+ s) | Model too big for this machine's RAM | Drop to a smaller 3B-class model (same chapter); close memory-hungry apps. |
| 4 | Wake word never triggers | Mic too far, too quiet, or the phrase is too common | Move within 1–2 m; re-check mic input level in OS settings; pick a rarer phrase ([chapter 2](02-wake-words.md)). |
| 5 | Wake word fires constantly (TV, podcasts) | Phrase matches common speech | Pick a two-word, made-up phrase; move the box away from speakers; or go [push-to-talk](02-wake-words.md). |
| 6 | `sounddevice.OSError` / "no input device" | OS hasn't granted mic access to the terminal | OS settings → Privacy → Microphone → allow the terminal/Python. Then retest. |
| 7 | `--listen` hangs, no transcript ever appears | Wrong input device (e.g., selected webcam mic is dead) | List devices (`device.py` helper in `starter/`), pick the real mic index in `config.py`. |
| 8 | Transcript is empty or one sad word | Vosk model path wrong, or model file missing | Verify the model folder path in `config.py`; re-download if deleted. |
| 9 | Transcript is gibberish | Engine mismatched to language or scene | Confirm `language="en"` (or your language model); for noisy rooms try `small.en` on faster-whisper ([chapter 4](04-offline-speech-to-text.md)). |
| 10 | LLM returns prose, not JSON | Prompt got diluted | Restore the strict parser prompt from `starter/` verbatim; [chapter 3](03-ollama-brain.md) explains why looseness breaks it. |
| 11 | Timer never chimes | System output device changed (headphones plugged in) | Set OS default output to the speakers the assistant should use; first check the headphone jack. |
| 12 | Timer worked yesterday, nothing today | Computer rebooted since — timers die with the process | Documented in [chapter 5](05-household-commands.md); re-set the timer, or add autostart so the process survives reboots ([chapter 8](08-two-evening-plan.md)). |
| 13 | Lists file has duplicates | Model emitted the same command twice (near-miss STT) | The sanity-checker dedupes identical entries within 30 s; update `starter/household.py` from the repo if yours predates it. |
| 14 | Kid mode lets something through | Profile flag not actually set in `config.py` | Re-run `python3 config.py` and read the printed confirmation; the allowlist is enforced only when the flag is set. |
| 15 | systemd unit starts, script fails instantly | Wrong Python — the service used system Python, not your venv | Point the unit at the venv's `bin/python` explicitly ([chapter 8](08-two-evening-plan.md)). |
| 16 | Everything silent after suspend/resume | The audio stack on some Linux distros drops the USB mic on suspend | Add a pre-suspend hook to restart the service; or unplug/replug the mic as the workaround. |
| 17 | Assistant hears only some family members | Distance + individual mics differ more than people expect | Closer mic first; then faster-whisper `small.en`, which is notably kind to varied voices ([chapter 4](04-offline-speech-to-text.md)). |
| 18 | Log says the *right* command but nothing happened | The command's function silently errored | Run the same sentence with `--text` (typed pipeline) and watch the full stderr; that isolates the bug from the voice layer. |
| 19 | Permissions error on `lists.json` | Script was once run with `sudo` and now the file belongs to root | `sudo chown $USER house-data/lists.json`; and stop running a home assistant as root — there's no reason. |
| 20 | Convinced it's broken but it works by typing | So the bug is the *voice layer*, not the brain | That's rows 6–9 territory. Walk backward from the log: wake event? transcript? JSON? |

## Footer rules that save evenings

1. **One change at a time.** Change the mic *or* the model, not both, then re-test.
   The typed pipeline (`--text`) is your control variable — treat it as ground truth
   ([chapter 8, Step 4](08-two-evening-plan.md)).
2. **Read the log with fresh eyes.** Nine misdiagnosed issues in ten are solved by
   noticing the log *doesn't say what you assumed it said*.
3. **When in doubt, reboot once.** Half the Linux audio-stack issues on this page
   politely vanish; then you've earned the right to be suspicious of the actual problem.
4. **If a fix here needs an account, a key, or a purchase,** pause and re-read
   [chapter 7](07-when-cloud-is-simpler.md) — maybe the honest answer for that one job
   is the other box, and that's allowed.
