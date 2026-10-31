# When a Cloud Assistant Is Honestly the Simpler Choice

This is the contrarian chapter, and it exists because a friend-paced manual owes you
the other side of the argument. You've now read seven chapters about building a
private assistant. Here's the truth in one sentence: **for some homes and some jobs,
a commercial cloud speaker is cheaper, easier, and works *today*, and choosing it is
not a failure of nerve.** Knowing which jobs it wins means you can keep it for those
and free your local box (and your evenings) from everything else.

The table below is the whole chapter if you want it in one glance; after it, we do the
two lists of "cloud wins" honestly — including the emotional one.

## The scorecard

| Job | Cloud speaker | This local build | Why |
|---|---|---|---|
| Whole-home music via voice (multi-room, Spotify-class catalogs) | **Wins big** | Doesn't do it | Music licensing and streaming are cloud-native businesses; local has neither. |
| "Order more paper towels" | Wins | Deliberately doesn't | [Chapter 6](06-kids-and-guests.md) removed network code *on purpose*. |
| "Remind me in 12 minutes, hands covered in dough" (kitchen timer) | Ties | Ties | Honestly both handle the kitchen timer case well; this is a no-score row to make the table look balanced. |
| Remote-control skills (front-door cameras, thermostats, sprinklers) | **Wins** | Doesn't | That's an integration ecosystem, not an assistant; local builds bolt on slowly. |
| Voice ID per person ("only *my* calendar") | **Wins** (mostly) | Later project | See the honest speaker-ID note in [chapter 6](06-kids-and-guests.md). |
| Timer + lists with zero cloud recording | **Local wins** | **Wins hugely** | This is the build's home field. |
| Works when the internet is down | No | **Yes** | Storm-ready. It's a real household superpower. |
| No subscriptions, ever | Usually free-tier-limited | **Yes** | One-time model download. |
| Hearing *exactly* what it heard, stored where you can see it | No | **Yes** | `log.txt`, in [chapter 5](05-household-commands.md). |
| Guests asking odd questions at a party | Fine — it has guardrails | Depends on your [rules](06-kids-and-guests.md) | Cloud products were stress-tested by a billion users; your build was stress-tested by your Tuesday. |
| Holiday-home / senior-room second unit ($40, in a box by Thursday) | **Wins** | Build takes an evening-plus | Sometimes the right answer is money, not evenings. |

## The three times cloud is *really* the simpler choice

**One: the far-field kitchen.** Hearing "set a timer" from across a running
dishwasher, a stove hood, and two children is a *hardware* problem solved by
tech-giant-class audio engineering on multi-mic arrays. Your build can eventually match
it — [chapter 1's](01-parts-and-hardware.md) Tier 3 mic arrays are the path — but a
$40 cloud speaker matches it *today*, out of the box, and in the kitchen that
difference is the whole product. A reasonable arrangement: kitchen = cloud for
timers-that-don't-record-anyone-who-cares; everywhere else = local for everything
private.

**Two: elders or holiday homes — the "it must just work" room.** For a parent's house
where support means *you over video chat at midnight*, a product with global support
may honestly serve everyone better than a kit you have to babysit remotely. Set it up,
teach one command, let the baked-in guardrails do the day-to-day work. Your local
build is a love letter; it's also a thing that occasionally needs its person. Match
the tool to who's actually present.

**Three: multi-person households that talk to it *all day*.** Cloud assistants have
absorbed a decade of edge cases: accents, speech rates, interrupted-sentence handling,
seven languages going in one house. Your build will get there with
[your tuning](05-household-commands.md); meanwhile your in-laws won't wait. That's
fine. Neither system is the household brain — they're tools, and tool-fit beats
purity.

## The honest feelings part (because it matters)

A voice assistant in a house is partly an *emotional* piece of furniture: someone
feels safer with a known-brand box in the corner, someone else feels the opposite.
Both feelings are legitimate data. The genuinely local-first position isn't "cloud is
bad"; it's **"cloud is fine for things where privacy costs you nothing, and the
private box exists for the things that would cost you something."** Holding both at
once is not hypocrisy; it's what a good tool wall looks like.

**The practical hybrid, stated plainly:**
- Keep the cloud speaker for: music, delivery shopping, the kitchen's chaos-proof timer.
- Keep the local box for: lists you'd hate an ad-targeting pipeline to read, kid mode,
  storm nights, 2 am "what keeps oats fresh" chatter with no eavesdropper.
- Write the [family rules card](06-kids-and-guests.md) to cover *both* boxes, so guests
  never have to know which is which.

**And the exit criteria, so nobody feels trapped:** if after a month your local build
is only ever used as a kitchen timer's backup, that's *still a win* — you now own a
scriptable offline timer-and-list box that can't be bricked by any company, and it
took you two evenings. That's not a failure; that's Tuesday.

Next: the actual build, sequenced into two evenings — [chapter 8](08-two-evening-plan.md).
