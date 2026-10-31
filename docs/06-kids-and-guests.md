# Kids and Guests: Drawing the Lines in Code, Not in Vibes

A household voice assistant is a loud, public device. Everything it says is heard by
everyone in the room, everything in its lists is readable by anyone who finds the
file, and — if you build it the way this manual does — every rule it follows is one
you wrote on purpose. This chapter is about writing those rules *on purpose*, for the
two categories of human most likely to surprise a system: small family members, and
visitors.

## The baseline promise (what this build can't do, even by accident)

Because [chapter 5's](05-household-commands.md) script has no network code, and the
LLM is only allowed to *suggest* commands that the script then sanity-checks:

- It cannot browse the web, post anything, message anyone, or order anything.
- It cannot run commands you didn't write, because there is no code path that executes
  arbitrary requests. This is a load-bearing property — keep it. The moment you add
  "and also let the assistant run me a shell command," you've turned a household tool
  into a microphone with `sudo`. Don't say we didn't warn you, and also, that feature
  would be very fun to have on a machine with nothing else on it. Compartmentalize.
- It cannot hear anyone when it's unplugged, asleep, or switched off at the wall.
  That's a stronger privacy promise than any commercial speaker makes, and it belongs
  in your [house rules](#the-family-rules-card).

## Kid mode: an allowlist, checked before anything happens

Kids will say unexpected things to it — that's the good part. The problem isn't their
weird questions; it's what a large-ish chat model might *answer*. So in this build,
kid mode isn't a softer prompt or a warning; it's a **hard allowlist** enforced in the
router script, before anything reaches the model for chat:

| Allowed in kid mode | Blocked in kid mode |
|---|---|
| SET_TIMER, CANCEL_TIMER | CHAT (any open conversation at all) |
| ADD_TO_LIST, READ_LIST (their own list only) | Reading the *grocery* or *todo* lists (adult lists) |
| "What time is it" | Anything that isn't in the table's left column |

Implementation is genuinely four lines in `starter/household.py`: if the current
profile is `kid` and the parsed command isn't on the allowlist, the assistant responds
"that one's not in my kid mode" and does nothing. It doesn't judge, it doesn't
elaborate, it doesn't try to be helpful in ways you didn't approve.

**The timing of when to introduce this matters more than the settings.** A child who
is told "this is the house timer, it sets timers and keeps your own list, and grown-up
mode has more" will treat those walls as furniture. A child who's told "it can do
everything but you're only allowed some" will spend every Saturday probing the
difference. Frame it as *what the assistant is*, not *what it's restricted from*.

## Voice honesty: there is no magic speaker-ID here

To be fully honest, a small local build like this **cannot tell speakers apart**. It
doesn't know whether an adult or a kid said "read me the todo list." Kid mode is a
switch you flip (a one-line config), not a voice-recognition system. The practical
pattern most households land on:

- **Daytime, family present:** `family` mode. Allowlists `CHAT` off, timers/lists on.
- **Adults-only hours or the home office:** `adult` mode, everything on.
- **When nobody's around:** it's unplugged or the machine is asleep. See above.

Voice identification *is* possible in this stack, and there are open models for it,
but they're the "third weekend" project, not the "second evening" one. Start with the
switch.

## Guests: the thirty-second card, and what it guarantees

Houseguests will meet the assistant within a minute of arriving — that's the nature
of things that talk. Handle it with a small printed (or image-messageed) card near the
box, and make the card's promises match what the code really does:

> **This is our home assistant.** It runs on that box, not on the internet.
> Say the wake word, then your request: "set a timer for 10 minutes,"
> "add napkins to the grocery list," "what time is it."
> It does not record conversations, and it can't send anything anywhere.
> **Guest mode** (say: "enable guest mode" as an adult, which sets a two-hour
> returns-to-family flag) only allows timers and reading our *guest list* —
> the grocery list stays ours.

Guest mode is just kid-mode's allowlist plus a narrower list, wired to a timestamp
that self-expires. It exists mostly so guests feel *welcomed* rather than policed —
the actual security gain is small, and the courtesy gain is large.

## The family rules card (the one-page constitution)

Write this down — actually write it, on paper, taped near the box. Four lines now
saves a hundred future arguments:

1. **What this is:** our family's timer and lists device; it talks back; it's offline.
2. **What's always okay:** timers, your own list, time questions.
3. **What's grown-up territory:** chatting with it, adult lists, changing settings.
4. **The power rule:** the machine's screen/keyboard is a parent tool; the *voice*
   part is everyone's. If the box ever says something strange, the grown-up opens
   `log.txt` *with the kids* and shows them what happened.

That last line is the sneaky-good parenting move in this whole chapter: because every
interaction is logged in a plain file, "let's look at what it heard" is a teachable
moment about how all these systems actually work — including the big ones, which
*definitely* also have logs; they just don't hand them to you.

## The kill switch, formalized

Every household needs an obvious, instant "that's enough" gesture. Ours: unplug, or
press the box's physical power, or — the gentle version that doesn't reboot anything —
say "goodnight" while an adult profile is on, which mutes the assistant until the next
morning. Implement it as a single flag file (the starter script's `quiet_until`
setting); the specifics matter less than the existence of a gesture *everyone in the
house knows*.

And that closes the build's ethics. Next, the needed-contrarian chapter: when the
answer to "should I build this at all" is, honestly, "maybe just buy the Amazon one":
[chapter 7](07-when-cloud-is-simpler.md).
