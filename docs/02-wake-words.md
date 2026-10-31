# Wake Words, Honestly Compared

Your assistant should not be recording you reading receipts out loud all day. Something
has to decide **when you're talking to it** versus **talking to your spouse about
dinner**. That's the wake word: the magic name it listens for before it starts actually
paying attention.

This chapter compares every realistic option for a home build, including the trade-offs
each glossary-level guide conveniently leaves out. There's a table at the bottom, and
an honest recommendation.

## Option 1: openWakeWord — the one this manual uses

**What it is:** an open-source wake-word detection engine that runs entirely on your
computer, on the CPU, in a whisper of computation. Ships with sensible pre-trained
phrases ("hey jarvis," "alexa" — careful with the last one, we'll get to that), and
lets you train your own phrase.

**The honest good parts:**

- Truly offline and keyless. It's a Python library. No account, no signup. This is
  why it's this manual's default.
- Detection happens locally; audio never leaves the machine even in principle.
- You can train a custom phrase (like a made-up family name) in an afternoon —
  remarkably safe from TV-ad false triggers, because ads don't say your dog's name.

**The honest ugly parts:**

- Accuracy on short, common phrases is good-not-great. Expect occasional false wakes,
  especially from TV dialogue with similar cadences.
- Python-only. If your brain box is a tiny non-Python thing, this option drags Python
  onto it.
- "Alexa" is one of the pre-trained phrases, and that's actively counterproductive
  in a house where an actual Alexa exists. Pick something else.

**Best for: literally this manual, and honestly most people reading it.**

## Option 2: Porcupine (Picovoice) — the accurate one with strings

**What it is:** a commercial wake-word engine from Picovoice. It's genuinely very
accurate and light.

**The honest good parts:** better detection than openWakeWord in noisy rooms, very
polished, custom free-tier wakewords.

**The honest ugly parts — and this matters for this manual's promise:**

- You have to create a Picovoice **account** and get an **access key**, even for the
  personal free tier. That's not a leak of your data to anyone, and it's not evil —
  but it breaks the "no accounts, no keys" rule this whole manual lives by.
- The free tier has per-device limits. Add a second machine someday and you'll hit
  paperwork you didn't want.

**Best for: someone who already has an account and values the accuracy. Fine tool,
wrong guest list for this house.**

## Option 3: microWakeWord on an ESP32-S3 — the independent one

**What it is:** wake-word detection that runs *on the microphone board itself* —
a tiny WiFi-microcontroller chip (the ESP32-S3 is the popular one) sipping power and
only "passing the ball" to your main computer once it hears the phrase.

**The honest good parts:**

- Your main computer can be asleep. The tiny chip wakes it up only when spoken to.
- Separation of duties feels right: the *eavesdropping* component is a $6 chip that
  can't do anything malicious even in theory, and your computer only spends attention
  after the phrase.
- Satisfying to build. It's a weekend-piercing project on its own.

**The honest ugly parts:**

- You need to buy the chip and flash firmware. The flashing process involves tools
  this manual otherwise never touches.
- More soldering-adjacent than most readers want on *evening two*.

**Best for: upgrade path. Not your first build; maybe your third.**

## Option 4: Push-to-talk / a physical button — the honest cheat

**What it is:** no wake word at all. You press a key on a wireless numpad, a foot
switch, or an old gamepad button the computer sees as a key, and *then* speak.

**The honest good parts:**

- **Zero false positives. Ever.** TV commercials can't trigger a button press.
- Zero additional software. Works on the grumpiest old hardware.
- Wonderful for houses with kids, because the kids learn immediately: press it,
  say your thing, get an answer. Cause and effect, stated physically. (See
  [chapter 6](06-kids-and-guests.md) for why that's a whole philosophy.)

**The honest ugly parts:**

- It's *less magical*. Part of any voice assistant's charm is that it's there
  without touching anything.
- Pedestrian. Doesn't make a good demo.

**Best for: bedrooms, offices, and any home with a baby, a light-sleeper shift worker
(nurses, we see you), or a TV that won't stop talking to smart speakers.** If you're
a night worker who's sick of devices chirping, seriously consider this for real.

## The one nobody should use: recording everything

To be complete and honest: an assistant *could* record continuously and let the text
processor decide what was a command. Don't. It's wasteful, it's the exact behavior
you'd explain to guests, and it requires you to trust a recording stack you control 100%
of — which sounds nice until a houseguest says something private near it. All four
options above are better. This row exists so you know we considered it.

## The comparison table

| Option | Cost | Key/account? | Runs where | False wakes | Effort | This manual uses it |
|---|---|---|---|---|---|---|
| openWakeWord | Free | **No** | Your computer's CPU (Python) | Occasional | Low | **Yes — default** |
| Porcupine | Free tier | **Yes (account + key)** | Your computer's CPU | Rare | Low | No (keyless rule) |
| microWakeWord on ESP32-S3 | ~$10–25 board | No | A separate tiny chip | Very rare, well-tuned | Medium-high | No (upgrade path) |
| Push-to-talk button | $0–25 | No | Anything | **Never** | Nearly zero | Allowed anytime |
| Record-everything | — | — | — | N/A | High | Never — see above |

## Choosing, honestly

- **Sleeping babies, shift workers, light sleepers:** button (opt 4). Not as a compromise
  — as a *preference*.
- **Everyone else, first build:** openWakeWord (opt 1), with the TV room and the
  bedroom as the two rooms to avoid, and the kitchen/living room as the wins.
- **If openWakeWord's false triggers start to genuinely bother you:** that's the
  *specific annoyance* from [chapter 1](01-parts-and-hardware.md) that justifies the
  ESP32-S3 path (opt 3).
- **Want the absolute cleanest, least-fuss setup with accuracy?** Porcupine (opt 2) is
  a fine tool. We're not using it in the manual because a key contradicts the promise,
  not because it's bad.

One behavioral note for whichever you pick: **the wake word should belong to the
house, not to you.** If your name is Melissa, calling it "Melissa" means every podcast
mentioning "Melissa" becomes a wake event. Pick a name that's unlikely to appear in
normal English (or a two-word phrase). "Hey Kitchen," "Box Wake," the dog's odd name —
these are boring by design, which is the entire point.

Next: the brain. Onward to [Ollama](03-ollama-brain.md).
