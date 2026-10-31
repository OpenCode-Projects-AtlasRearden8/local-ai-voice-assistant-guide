# Household Commands: Timers, Lists, and Your Own Rituals

This is the chapter where the assistant stops being a demo and starts being *useful*.
Everything here runs on one small Python file, stores its data in plain text you can
open with any editor, and has no network code at all. That combination — one file,
plain data, no network — is the whole philosophy, so let's be explicit about why.

## Why *one script* and *plain files* beat a framework

Every commercial assistant is thousands of features deep. Your house will use four.
Writing those four *yourself* means:

- **You can read it.** When something misbehaves at 7 am, you can open 120 lines of
  Python instead of a settings maze.
- **You can bend it.** "Timers, but the chime is the opening seconds of my kid's
  favorite song" is a two-line change, not a feature request.
- **It stores data where you can see it.** Lists live in a JSON file on disk. When
  the assistant *misses* something, you can look at the file and know instantly
  whether it recorded nothing, recorded the wrong thing, or recorded right and
  displayed wrong. That three-way split diagnoses 90% of voice-assistant bugs.
- **Trust is reviewable.** [Chapter 6's promises](06-kids-and-guests.md) are enforced in
  this file, where they can be read row by row — not in some remote config.

## The command menu to start with

Start with exactly these (all implemented in `starter/household.py` in this repo, and
walked through in [chapter 8](08-two-evening-plan.md)):

| Command (say this) | What it does | Stored where |
|---|---|---|
| "Set a timer for ten minutes" | Starts a timer; chime + spoken "Timer's done" at zero | RAM + a log line |
| "Set a timer for 45 minutes for the roast" | Same, with a friendly label it will say back | RAM + log |
| "Cancel the timer" | Cancels the most recent running timer | Log |
| "Add milk to the grocery list" | Appends "milk" | `lists.json` |
| "Add call the dentist tomorrow to the todo list" | Appends it, timestamped | `lists.json` |
| "Read the grocery list" | Speaks the list, numbered | — |
| "Remove the last thing from the grocery list" | Deletes most recent entry (for the accidental "and… and… and…") | `lists.json` |
| "What time is it" | Answers; the trivial command that makes guest demos satisfying | — |

That's it. Resist adding more until these are boring. Boring commands are the goal.

## Where the data lives

A single directory (default: `house-data/` next to the script, or set `HOUSE_VOICE_DATA_DIR`)
holding:

```
house-data/
  lists.json        ← your lists, plain JSON
  log.txt           ← one line per voice interaction (transcript + what it did)
```

The `log.txt` is deliberately readable with the eyes: date, the sentence it heard,
what it decided that meant, and what it did. Six times a year you'll open this file
and think, "oh *that's* why it ignored me" — and those moments are delightful, honest
debugging, the kind impossible with any cloud speaker.

## The two technical pieces, explained in friend terms

### Piece one: the intent parser (Chapter 3's trick, in code)

The LLM returns a tiny JSON like `{"command":"SET_TIMER","args":{"minutes":10,
"label":null}}`. The script then **checks that JSON with plain if-statements before
acting** — including a check that the minutes are a real number between 1 and 600, and
a check that the list name is one of the lists you actually defined. This is the
difference between a model *suggesting* a command and a house *obeying* one. The
speaker-facing result: you say the sentence your way; the model maps it; the script
sanity-checks it; the house does it predictably or tells you it couldn't.

### Piece two: timers without drama

The timer is the one piece of this build with clock machinery, so here's the entire
honest story:

- A timer is just a Python thread that sleeps for N minutes and then makes noise.
- **If the computer reboots, timers die** — that's the known cost of local-first, and
  the *fix* is simple: tell the household, "the box keeps timers only while it's awake,"
  and don't set overnight ones. A week in, this stops mattering and nobody misses it.
- The chime plays through the same speakers the assistant talks through, using the
  operating system's own sound player (see `starter/household.py`), so there's no extra
  audio dependency to install.

## Your own rituals (the fun part)

Once the four boring commands work, you're allowed to enjoy yourself. These are all
one-evening or one-hour additions, each a small function in the same file:

- **Trash-day nudge.** Every Tuesday morning at 7, a scheduled run says "trash day —
  bins out tonight." Uses your OS scheduler on the outside (`systemd` timer or Windows
  Task Scheduler), your same script on the inside.
- **Quiet-hours lock.** Between 20:30 and 07:00, the only command that works is
  `READ_LIST` — and even that *doesn't speak*, it prints to the screen. Your own rule,
  your own enforcement.
- **Medication list read-back** (education/organization only — never medical advice,
  just a spoken read-back of a list a human typed). The list, not the assistant, is
  the source of truth.

A closing note for this chapter, because it's the one people ask about: **no, you don't
need an agent framework.** You need one dictionary mapping command names to functions.
Everything fancier can come later, once the boring version has been useful for a
month. Onward to who gets to use it and what they're allowed to ask for:
[kids and guests](06-kids-and-guests.md).
