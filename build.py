#!/usr/bin/env python3
"""Build the static HTML site from docs/. Stdlib + python-markdown only.

Usage: ./build.sh   (which runs this)  ->  site/index.html + site/<page>.html
"""

import glob
import os
import re
import shutil
import sys
from datetime import datetime

import markdown

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")
SITE = os.path.join(ROOT, "site")
ASSETS = os.path.join(ROOT, "assets")

# order fixes the nav; everything else lands alphabetically after
ORDER = ["index", "01-parts-and-hardware", "02-wake-words", "03-ollama-brain",
         "04-offline-speech-to-text", "05-household-commands",
         "06-kids-and-guests", "07-when-cloud-is-simpler",
         "08-two-evening-plan", "troubleshooting", "glossary"]

MD = markdown.Markdown(extensions=["tables", "fenced_code", "toc", "sane_lists"],
                       output_format="html5")

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — The House Voice</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="site-header">
  <p class="kicker">The House Voice</p>
  <p class="sub">A friend-paced manual for a private, local voice assistant at home</p>
  <nav>{nav}</nav>
</header>
<main>
{body}
</main>
<footer>
  <p>The House Voice — part of the Asdale Dynamics beginner-friendly AI guides.
     Offline-first, no accounts, no API keys.</p>
  <p>© {year} Asdale Dynamics, LLC ·
     <a href="https://github.com/dylanasdale/dylanasdale.github.io">dylanasdale.github.io</a>
     · MIT licensed. Not affiliated with any voice-assistant vendor; no accounts
     or keys were used to build any of this.</p>
</footer>
</body>
</html>
"""


def md_files():
    return [os.path.basename(p)[:-3] for p in sorted(glob.glob(os.path.join(DOCS, "*.md")))]


def page_title(stem):
    with open(os.path.join(DOCS, f"{stem}.md"), encoding="utf-8") as f:
        m = re.search(r"^#\s+(.+)$", f.read(), re.M)
    return (m.group(1) if m else stem).split(":")[0]


def nav_for(current):
    links = []
    for stem in ORDER:
        if stem == "index":
            short = "Home"
        elif stem.startswith("0") and stem[1].isdigit():
            short = f"Ch {stem[1]}"           # "01-parts..." -> "Ch 1"
        elif stem == "troubleshooting":
            short = "Troubleshooting"
        elif stem == "glossary":
            short = "Glossary"
        else:
            short = page_title(stem)
        cls = ' class="active"' if stem == current else ""
        links.append(f'<a href="{stem}.html"{cls}>{short}</a>')
    return "\n".join(links)


def convert(stem):
    with open(os.path.join(DOCS, f"{stem}.md"), encoding="utf-8") as f:
        text = f.read()
    # internal doc links -> html links
    text = re.sub(r"\]\((([^)#]+))\.md\)", r"](\1.html)", text)
    return MD.reset().convert(text)


def build():
    os.makedirs(SITE, exist_ok=True)
    shutil.copy(os.path.join(ASSETS, "style.css"), os.path.join(SITE, "style.css"))
    stems = [s for s in ORDER if os.path.exists(os.path.join(DOCS, s + ".md"))]
    extra = [s for s in md_files() if s not in stems]
    all_stems = stems + extra
    for stem in all_stems:
        html = TEMPLATE.format(title=page_title(stem), nav=nav_for(stem),
                               body=convert(stem), year=datetime.now().year)
        out = os.path.join(SITE, f"{stem}.html")
        with open(out, "w", encoding="utf-8") as f:
            f.write(html)
    print(f"Built {len(all_stems)} pages into site/ from {len(all_stems)} docs.")
    return all_stems


if __name__ == "__main__":
    built = build()
    missing = [s for s in ORDER if s not in built]
    if missing:
        sys.exit(f"MISSING docs: {missing}")
