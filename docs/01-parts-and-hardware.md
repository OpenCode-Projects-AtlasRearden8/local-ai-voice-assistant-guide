# Parts and Hardware: Getting Ears and a Mouth

Your assistant needs exactly three things from its hardware:

1. **Ears** — a microphone it can hear you with.
2. **A mouth** — a speaker to answer from.
3. **A brain box** — some computer that never has to be fancy, only always on.

The good news you won't hear from gadget reviewers: **you almost certainly already own
tier one.** Let's start there, because the fastest path to a working assistant is the
one with zero spent dollars.

## Tier 1: What you already have (cost: $0)

- **Brain box:** a laptop, desktop, or mini-PC running Windows, macOS, or Linux. Even a
  5–6 year old machine with 8 GB of RAM is genuinely enough for the build in this manual
  (one small model, one small speech model). A Raspberry Pi 5 or 4 (4 GB+) also works,
  with some patience and the lighter engine choices described in
  [chapter 4](04-offline-speech-to-text.md).
- **Mic and speaker:** the laptop's own built-in mic and speakers. For a first build,
  these are *fine*. The far-field pickup (hearing you from across the room) is worse
  than a commercial smart speaker, and the troubleshooting table has a row for every
  symptom of that, but you can walk across the room and talk to it — it's allowed.
- Upgrade when (if) you fall in love with it. Not before.

## Tier 2: Under ~$60 (the most common home)

| Part | Good pick | Fine-enough pick | Why it matters |
|---|---|---|---|
| Microphone | USB condenser mic on a small boom arm (any brand, ~$25–45) | Any decent **USB** headset mic, or a webcam with a mic | USB is plug-and-play everywhere. A mic that points *at the chair you talk from* beats an expensive mic on the other side of the room. |
| Speaker | Small USB or 3.5 mm desktop speaker (~$15–30) | The computer's existing output | The assistant only speaks short sentences. Don't buy sound quality for this; buy *aim*. Put it where you'll hear it while cooking. |
| Mic placement | Within ~1–2 meters of where you talk | On the desk | Distance is the single biggest quality variable. Closer beats better. |

## Tier 3: The shelf-box (roughly $90–$180, and optional)

This is the version that looks and behaves like a real room assistant — a small silent
box on a shelf with a proper mic array, no fans.

| Part | Pick | Notes |
|---|---|---|
| Brain box | Raspberry Pi 5 (8 GB) or a used mini-PC (8 GB RAM) | The mini-PC is my honest pick for most people: silent, cheap, and roomier for the LLM. The Pi is smaller and cuter but tighter on memory. |
| Mic array | A 4-mic USB array or an I2S MEMS mic hat | Multiple oriented mics hear you from across the room far better than one cheap mic. Worth it only if you truly want far-field. |
| Speaker | Small 5W speaker with its own amp | Standard, boring, fine. |
| Case/framing | Anything ventilated | People skip this and then complain about it overheating. Don't skip it. |

You do not need Tier 3 for the two-evening plan. Buy it later, once Tier 1 has annoyed
you in a *specific* way (like "I hate leaning in toward the laptop"), because a
specific annoyance tells you exactly what to buy.

## The parts checklist (print me)

Copy this into a notes app or print this section. Based on
[chapter 8's plan](08-two-evening-plan.md).

- [ ] A computer you can leave on (8 GB+ RAM, any OS) — **Tier 1 counts**
- [ ] ~10 GB of free disk space (models take room)
- [ ] Working audio out (speakers, any kind)
- [ ] A microphone, any kind (built-in counts)
- [ ] Internet *once*, for the installs — then it can go away entirely
- [ ] Admin rights on the machine (`sudo` on Linux/macOS,Administrator on Windows)
- [ ] The willingness to paste 6 commands into a terminal
- [ ] (Evening 2 only) A chosen wake-word approach from [chapter 2](02-wake-words.md)
- [ ] (Optional, later) One quieter machine + better mic if you decide to go Tier 3

## Rules of thumb that save money

- **Sound quality is irrelevant; intelligibility is everything.** The assistant says
  "your timer went off." A $5 speaker can do that.
- **Microphone distance matters more than microphone quality.** A $30 mic 1 meter away
  beats a $150 mic 4 meters away.
- **Your brain box's biggest job is the LLM.** If you're constrained (old machine),
  keep the *speech-to-text* model small and your *searching-down-the-room mic* close,
  and the build still works — see
  [chapter 4](04-offline-speech-to-text.md) for the light options.
- **Everything here runs fine on a machine with no GPU.** GPUs speed things up, they
  don't unlock them.

Now that you know what you're plugging in, the next question is *when* it should be
listening. That's wake words — and some of them have, to put it kindly, a personality.
