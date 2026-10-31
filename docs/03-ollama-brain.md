# Ollama as the Brain

The wake word decides *when* to listen. The speech-to-text engine turns your sentence
into words on a screen. The brain decides **what those words mean** and what to do
about them. That's the LLM's job, and for a household assistant, it's the single most
important design decision in the whole build — bigger than the mic, bigger than the
wake word.

This manual's local handbook companion (the *Local AI Handbook*) covers installing
Ollama in general depth — what models are, why they're file-sized machines, how
conversations work. This chapter stays voice-specific: which model class to reach for
in a house, and — much more importantly — **the one trick that makes a small local
model reliably useful for household commands.**

## The install (short version)

If Ollama isn't on your machine yet, the [handbook](https://ollama.com/download)
covers it fully; the short version for your terminal is:

```bash
# Linux
curl -fsSL https://ollama.com/install.sh | sh

# macOS: brew install ollama   (or the .dmg from ollama.com)
# Windows: the installer from ollama.com
```

Then pull one model:

```bash
ollama pull llama3.2:3b
```

A member of the **~3B class** (llama3.2:3b, qwen2.5:3b, phi3:mini — all close enough
to be interchangeable for this chapter) is the sweet spot for a household assistant:
small enough to run heartily on a laptop's CPU, clever enough to parse "can you make
sure I call the pharmacy before five" into something useful.

**Memory honesty:** leave ~4–6 GB RAM headroom for the model. On an 8 GB machine,
that's *fine but snug*; close your browser tabs first, or drop to a smaller model —
the [handbook](https://ollama.com) explains model sizing in general.

## The trick: don't ask the model to *answer*; ask it to *translate*

Here's where a friend saves you an evening of frustration. If you ask a 3B model

> "Hey assistant, warn me that I need to get the roast out of the oven in 45 minutes"

…you'll get a chatty paragraph about roasts that may or may not include an actual
45-minute timer. That's the wrong question to ask a small model.

The right question is different. **Ask the model to translate spoken language into
a strict command format**, and let a plain *script* — not the model — do the actual
work:

```text
You are the command parser for a household voice assistant.
Allowed commands: SET_TIMER, ADD_TO_LIST, READ_LIST, REMOVE_FROM_LIST, CANCEL_TIMER, CHAT.
Respond ONLY with a JSON object: {"command": "...", "args": {...}}
If the sentence is regular chat or anything uncertain, return {"command": "CHAT", "args": {"text": "<the sentence>"}}
```

Now the same spoken sentence comes back as:

```json
{"command": "SET_TIMER", "args": {"minutes": 45, "label": "roast"}}
```

…and your script — 40 tidy lines of Python, not a neural net — turns that into an
actual timer. **The model handles vocabulary and messiness; the script handles
consequences.** This is the whole architecture, and it's why this build works on a
laptop instead of a gaming PC.

### Why "CHAT" is in the allowed list

Because sometimes you *do* want to talk to it: "what's a good substitute for
buttermilk?" That path — the fun one — lets the same 3B model chat normally. But it's
optional, and [chapter 6](06-kids-and-guests.md) shows how to turn it *off* for kids
so the assistant physically cannot converse outside the household commands.

## Keeping Ollama warm (latency honesty)

A cold model load takes a few seconds; a warm model answers in under a second on most
machines. Once you've used it
once, Ollama keeps the model in memory for a while. If you find the first request of the
morning slow, that's the cold load; the fix is simply accepting it or asking Ollama to
keep it loaded longer (`OLLAMA_KEEP_ALIVE`, documented in their FAQ). Put that variable
in your [systemd unit or startup script](08-two-evening-plan.md) in Evening 2.

## The one-line test (do this on Evening 1)

After installing and pulling, run:

```bash
ollama run llama3.2:3b "Turn this into JSON: {\"command\":\"...\",\"args\":{\"minutes\":N,\"label\":\"...\"}} — sentence: set a timer for 45 minutes for the roast"
```

If you get back a JSON blob with `"minutes": 45` in it, the brain works. If you get
back a paragraph about "certainly, here's how you might set a timer," your prompt
wasn't strict enough — the format instruction matters more than anyone expects, and
[chapter 5](05-household-commands.md) shows the final version used by the starter
script, tuned over many evenings.

Onward to giving the brain ears worth trusting: [offline speech-to-text](04-offline-speech-to-text.md).
