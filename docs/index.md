# The House Voice: A Friend-Paced Manual for a Private, Local Voice Assistant

Welcome. This is the manual for building a small voice assistant that lives entirely
inside your house. It hears you, it understands you, it answers you — and nothing it
hears has to leave the building.

Everything in here requires **no accounts, no API keys, and no subscriptions.** If a
step ever demands a credit card or a login, we've made a mistake; there's a project
mailbox (the GitHub issues page for this repo) for reporting those.

## Who this is for

Anyone who wants a home assistant they fully control: night-shift workers who despise
smart speakers talking after 9 pm, parents who don't want a corporation storing
recordings of their kids, tinkerers who just think it's cool that a tiny brain can sit
on a shelf and listen for their name.

You do **not** need to be a programmer. You need a computer you're allowed to install
things on, a few evenings, and the willingness to paste commands into a terminal. The
manual is written in the same voice as everything else from Asdale Dynamics: like a
friend explaining it over coffee, never like a lecture.

## What this manual covers (and what it doesn't)

This is the **hands-on build manual**. It sits alongside two companion guides, and each
one owns a different slice of the same territory:

| Guide | What it covers | What it does *not* cover |
|---|---|---|
| **The Local AI Handbook** | Local AI in general — what LLMs are, picking models, installing Ollama on any machine, general setup theory | Voice specifically. No microphones, no wake words. |
| **Voice Assistants: A Comfort Guide** | Whether voice is right for you, where to place it, household etiquette, when your family will actually use it | Building anything. It's the "should we?" guide, not the "how?" |
| **This manual (The House Voice)** | The concrete two-evening build: microphone and speaker choices, wake words, offline speech-to-text, a scripted one-household command brain, kids-and-guests boundaries | Big local-AI theory, cloud assistant features, and smart-home integration beyond this box |

If you're reading this before touching the other two, that's fine — this manual is
self-contained. But when a topic belongs to a companion (like "which LLM should I
download in general"), we point there instead of repeating it.

## The chapters, in the order a friend would give them

1. **[Parts and hardware](01-parts-and-hardware.md)** — your microphone-and-speaker
   options, honestly priced, including the "use what you already have" tier, plus the
   printable parts checklist.
2. **[Wake words, compared](02-wake-words.md)** — how your assistant decides *when* to
   listen. Four options, each with the honest downsides, including the free one nobody
   talks about: a physical button.
3. **[Ollama as the brain](03-ollama-brain.md)** — installing the local LLM and using it
   in the one way it's genuinely great at here: turning messy spoken sentences into
   small, predictable commands.
4. **[Offline speech-to-text](04-offline-speech-to-text.md)** — how your voice becomes
   text without the internet, and which engine to pick depending on how old your
   computer is.
5. **[Household commands: timers, lists, rituals](05-household-commands.md)** — the
   scriptable part. Commands you write for *your* house, stored in plain files you can
   read with your eyeballs.
6. **[Kids and guests: drawing the lines](06-kids-and-guests.md)** — what the assistant
   may and may not do, enforced in code, not vibes.
7. **[When a cloud assistant is honestly the simpler choice](07-when-cloud-is-simpler.md)** —
   the chapter where we admit that sometimes the big-company speaker is the right tool,
   and nobody is failing a test by keeping it.
8. **[The two-evening build plan](08-two-evening-plan.md)** — the whole thing sequenced
   into two evenings, with checkpoints at each step so you always know it's working.
9. **[Troubleshooting table](troubleshooting.md)** — symptoms, likely causes, fixes.
10. **[Glossary](glossary.md)** — every jargon word this manual uses, in plain English.

## The promise, restated

- Everything runs on hardware you own, inside your walls.
- No account creation, ever. No API keys, ever.
- Every script in this manual is short, readable, and yours to change.
- If a step doesn't work, the [troubleshooting table](troubleshooting.md) is exhaustive,
  and the fallback in
  [chapter 7](07-when-cloud-is-simpler.md) is always available without guilt.

Ready? Start with [parts and hardware](01-parts-and-hardware.md) — even if the first
thing on the list is "your current laptop, probably."
