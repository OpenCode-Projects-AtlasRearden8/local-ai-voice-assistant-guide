# Glossary

Every jargon word this manual (or its companion guides) uses, in plain English —
"like a friend would," per the house style. Ordered roughly by when you meet the
concepts in the build.

## The physical parts

**Brain box** — the computer your assistant lives on. A laptop, mini-PC, or Raspberry
Pi. Doesn't have to be fancy; it does have to be always-on.

**Far-field** — hearing you from across the room rather than from a metre away.
A hardware property of microphones and mic *arrays*, not a software feature. This is
what commercial speakers spend serious engineering on.

**Mic array** — several microphones pointed in slightly different directions, combined
so the computer can prefer your voice over the dishwasher. The [chapter 1](01-parts-and-hardware.md)
Tier 3 upgrade option.

**VAD (voice activity detection)** — the cheap classifier that decides "that was a human
voice" before anything expensive runs. Wakes the transcript engine up and puts it
back asleep, all day, for free.

## The pipeline (in the order your voice travels)

**Wake word** — the phrase that flips your assistant from *erring on the side of
ignoring you* to *actually listening*. Compared honestly in [chapter 2](02-wake-words.md).

**STT (speech-to-text)** — the engine that turns recorded words into typed words.
Whisper, faster-whisper, whisper.cpp, and Vosk are all STT engines. Sometimes called
ASR (automatic speech recognition); same thing, older name.

**Transcript** — the text the STT engine produced. What shows up in rows 8 and 9 of
the [troubleshooting table](troubleshooting.md).

**Inference** — the act of *running* a model on input. "Doing inference" = "the machine
thought about your sentence." Running a model once is inference; the model itself just
sits there in a file.

**Token** — the unit a language model reads and writes in, roughly-but-not-exactly a
word or piece of a word. When engineers say "a 3B model," they mean three billion
*machine-learning knobs* (parameters), not three billion tokens; both numbers matter
and they're different dials.

**Quantization (and `int8`)** — storing the model with less precision per number so
it takes four times less memory and runs several times faster, releasing a sliver of
accuracy nobody will miss in a household. The `int8` in [chapter 4](04-offline-speech-to-text.md)'s
code sample is exactly this.

## The brain

**LLM (large language model)** — the neural net that reads and writes text. In this
build it has exactly one narrow job: translating your spoken sentences into
computer-legible command JSON ([chapter 3](03-ollama-brain.md)). The "large" in the
name is relative; the ones in this manual are small enough to live in your laptop.

**Ollama** — the app that downloads, stores, and runs LLMs on your machine with one
command each. Not itself a model — it's the *runner*.

**Model** — one particular neural net in a file. "llama3.2:3b" is a model. "qwen2.5:3b"
is a different one. Swapping models is a free, reversible choice, not a purchase.

**Prompt** — the text you give a model to steer it. In this build the most important
prompt is the command-parser one ([chapter 3](03-ollama-brain.md)), because its strictness
is what makes a small model behave like a predictable appliance.

## The command layer

**Intent** — *what you meant*, as opposed to what you literally said. "Can you make
sure I get up in forty minutes" has the *intent* SET_TIMER(40) even though no timer
noun is present. Extracting intent is the LLM's whole job here.

**Router** — the small script ([chapter 5](05-household-commands.md)) that takes the
LLM's JSON, sanity-checks it, and actually does the thing. The gatekeeper. Where
[kids-and-guests boundaries](06-kids-and-guests.md) are enforced.

**Chat mode** — the optional path where the LLM just *talks* instead of returning a
command. Fun, optional, and the first thing [kid mode](06-kids-and-guests.md) turns off.

**JSON** — the text format humans and machines both can read, shaped like
`{"command":"SET_TIMER","args":{"minutes":10}}`. Used here because it's strict,
inspectable, and impossible to accidentally "interpret."

**Allowlist** — the opposite of a blocklist: instead of listing what's forbidden, you
name exactly what's permitted and everything else is refused by default. How kid and
guest modes are built in [chapter 6](06-kids-and-guests.md).

## The housekeeping

**Systemd / LaunchAgent / Task Scheduler** — the three operating systems' built-in
"run this at boot/login" mechanisms. The autostart step in
[chapter 8](08-two-evening-plan.md) uses whichever matches your machine.

**False wake / false positive** — the assistant deciding you called it when you
didn't (TV dialogue, podcasts, a similar name). The cost of wake words, honestly
graded in [chapter 2](02-wake-words.md).

**Hybrid setup** — keeping a cloud speaker for its genuine strengths (music, shopping)
alongside your local box for everything private. Recommended without shame in
[chapter 7](07-when-cloud-is-simpler.md).

**Local-first** — the design rule that data and computation stay on hardware you own,
inside your house. The whole point of this manual, and (per the README) the point of
everything Asdale Dynamics releases.
