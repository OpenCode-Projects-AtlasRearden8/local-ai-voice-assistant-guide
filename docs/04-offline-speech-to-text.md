# Offline Speech-to-Text: Turning Voice Into Text Without the Internet

By now your assistant has a name trigger and a brain. This chapter gives it ears: an
engine that converts your spoken sentence into text on your machine, with no cloud and
no key. (The *Local AI Handbook* covers why "on-device" inference matters in general
depth; this chapter is only about which transcript engine belongs in *your house*.)

## The honest landscape

There are three engines worth your evening, and they divide along one clear line:
**accuracy versus speed on everyday computer hardware.**

| Engine | Models & footprint | Accuracy | Speed on CPU | Runs on a Pi? | Best for |
|---|---|---|---|---|---|
| **faster-whisper** (Whisper family, retooled) | `base.en` ~150 MB, `small.en` ~490 MB | Very good | Good | Yes, with patience | **Default in this manual** |
| **whisper.cpp** | Same model family, similar sizes | Very good | Good | Yes, with patience | Mac machines and C++ purists |
| **Vosk** | Tiny models from ~40 MB to ~2 GB | Good, not as good | **Excellent** | Comfortably | Old/slow machines, Pi 4, impatient people |

All three are volunteer-friendly, run entirely offline, and need no account. The
differences above are real but small in practice; pick by hardware, not by hype.

## This manual's default: faster-whisper with `base.en`

`faster-whisper` is a community re-packaging of OpenAI's Whisper family of models into
faster, CPU-friendly form. The `base.en` model — English-only, ~150 MB — is the point
where the accuracy/effort trade works for household sentences. Install with:

```bash
pip install faster-whisper
```

…and use it like this in the starter script (shown in full in
[chapter 8](08-two-evening-plan.md) and `starter/` in this repo):

```python
from faster_whisper import WhisperModel
model = WhisperModel("base.en", device="cpu", compute_type="int8")
segments, _ = model.transcribe("last_command.wav", language="en")
text = " ".join(s.text for s in segments).strip()
```

That `int8` is a small detail with a real payoff: it tells the engine to use the
cheap, slightly lossy math that runs several times faster on ordinary CPUs, losing
accuracy no household sentence will miss.

**Note — kids' voices, honestly:** Whisper models sometimes stumble more on young
children's voices than on adults' — pitch, diction, and vocabulary differ. If you have
kids who will use this, expect `small.en` to do noticeably better than `base.en`, and
expect [chapter 6](06-kids-and-guests.md)'s guardrails to matter even more than usual.
The universal kid-workaround (speak clearly, press the button, say the whole command
in one sentence) solves it for nearly every household.

## The fast one: Vosk (when your machine is tired)

If your brain box is a Raspberry Pi 4, a 2012 netbook, or anything that makes you
patient, use **Vosk**. Its smallest models are tens of megabytes, its speed on a Pi is
excellent, and while it's not as *brilliant* as Whisper, it is remarkably good at
**short command phrases** — exactly what a household assistant mostly hears:

```python
from vosk import Model
model = Model("vosk-model-small-en-us-0.15")
```

Its small model (~40 MB) is sensibly accurate for "set a timer for ten minutes,"
"add milk to the list," and the other sentences in
[chapter 5's](05-household-commands.md) menu. It's worse at long, rambling sentences —
but the house rules in [chapter 8](08-two-evening-plan.md) ask for one short sentence
per command anyway. Keep the sentences short and Vosk is a perfect fit for slow
hardware.

## The picky one: whisper.cpp

::: {.note}
Same models as faster-whisper, different runtime — better-suited to Macs and to
people who like single-file C++ builds. If you're not on a Mac and don't have a
reason, `faster-whisper` is the smoother evening. If you *are* on a Mac, it's a
coin flip; either works.
:::

## The one honest warning about "offline"

"Offline speech-to-text" means **the transcript never leaves your machine**. It does
*not* mean the microphone is turned off, or that the wake word misses nothing, or that
your family won't occasionally hear a recording played back and wonder. The realistic
privacy posture is:

- Audio is processed locally. ✓
- The only thing ever *stored* by default is your [household lists](05-household-commands.md)
  and a small log — both in plain text files you can open anytime. ✓
- Nothing here can upload anything, because the [build includes no network code](06-kids-and-guests.md). ✓

That's a stronger guarantee than any commercial speaker offers, and it's fine to feel
good about it. On to the fun part — teaching the house to answer real requests:
[household commands](05-household-commands.md).
