#!/usr/bin/env python3
"""The House Voice test suite. Plain asserts, no dependencies. Run from anywhere:

    python3 tests/test_all.py        (or ./tests/run_tests.sh)
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
STARTER = os.path.join(ROOT, "starter")
sys.path.insert(0, STARTER)

import config  # noqa: E402
import household  # noqa: E402


class BuildSite(unittest.TestCase):
    """build.sh runs, produces the expected site pages, and page links resolve."""

    def test_build_runs_and_outputs_pages(self):
        run = subprocess.run(["bash", "build.sh"], cwd=ROOT, capture_output=True,
                             text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        site = os.path.join(ROOT, "site")
        for stem in ("index", "01-parts-and-hardware", "03-ollama-brain",
                     "08-two-evening-plan", "troubleshooting", "glossary"):
            path = os.path.join(site, f"{stem}.html")
            self.assertTrue(os.path.exists(path), f"missing {path}")
            with open(path, encoding="utf-8") as f:
                html = f.read()
            self.assertIn("style.css", html)
            self.assertIn("<link rel=\"stylesheet\"", html)
        self.assertTrue(os.path.exists(os.path.join(site, "index.html")))
        with open(os.path.join(site, "index.html"), encoding="utf-8") as f:
            self.assertIn("Asdale Dynamics, LLC", f.read())  # footer credit

    def test_every_site_page_follows_template(self):
        site = os.path.join(ROOT, "site")
        self.assertTrue(os.path.exists(os.path.join(site, "index.html")),
                        "run build first")
        with open(os.path.join(site, "index.html"), encoding="utf-8") as f:
            html = f.read()
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("The House Voice", html)
        self.assertIn("2026 Asdale Dynamics, LLC", html)

    def test_internal_links_resolve(self):
        targets = {stem for stem in
                   (os.path.splitext(f)[0] for f in os.listdir(DOCS))}
        for stem in targets:
            with open(os.path.join(DOCS, f"{stem}.md"), encoding="utf-8") as f:
                text = f.read()
            for link in re.findall(r"\]\(([^)#]+?\.md)\)", text):
                self.assertIn(link[:-3], targets,
                              f"{stem}.md links to missing doc {link}")
        site = os.path.join(ROOT, "site")
        for page in os.listdir(site):
            if not page.endswith(".html"):
                continue
            with open(os.path.join(site, page), encoding="utf-8") as f:
                html = f.read()
            for link in re.findall(r'href="([^"#]+?\.html)"', html):
                if link.startswith("http"):
                    continue
                self.assertTrue(os.path.exists(os.path.join(site, link)),
                                f"{page} links to missing {link}")

    def test_docs_reference_companions_without_repeating(self):
        """Each promise: we point to the two companion guides by name, once."""
        with open(os.path.join(DOCS, "index.md"), encoding="utf-8") as f:
            text = f.read()
        self.assertIn("Local AI Handbook", text)
        self.assertIn("Comfort Guide", text)


class NoSecrets(unittest.TestCase):
    """Scans every tracked file for accidental keys. Manual promise: none ever."""

    PATTERNS = (
        r"sk-[A-Za-z0-9]{20,}", r"AKIA[0-9A-Z]{16}", r"ghp_[A-Za-z0-9]{20,}",
        r"github_pat_[A-Za-z0-9_]{20,}", r"xox[a-z]-[A-Za-z0-9-]{10,}",
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----", r"api[_-]?key\s*=\s*['\"][A-Za-z0-9]",
        r"Bearer\s+[A-Za-z0-9_\-.]{20,}",
    )

    def test_no_look_alike_secrets_anywhere(self):
        offenders = []
        for walked, dirs, files in os.walk(ROOT):
            dirs[:] = [d for d in dirs if d not in (".git", "site", "house-data")]
            for name in files:
                path = os.path.join(walked, name)
                if not os.path.isfile(path) or os.path.getsize(path) > 2_000_000:
                    continue
                try:
                    with open(path, encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                except OSError:
                    continue
                for pattern in self.PATTERNS:
                    if re.search(pattern, content):
                        offenders.append(f"{path}: matches {pattern}")
        self.assertEqual(offenders, [])

    def test_no_account_requirements_in_doc_commands(self):
        """Every terminal command the manual gives should be key/account-free."""
        banned = re.compile(r"(signup|sign up|create an account|access key"
                            r"|api key)", re.I)
        for name in sorted(os.listdir(DOCS)):
            if not name.endswith(".md"):
                continue
            with open(os.path.join(DOCS, name), encoding="utf-8") as f:
                text = f.read()
            fenced = re.findall(r"```[^\n]*\n(.*?)```", text, re.S)
            for block in fenced:
                self.assertIsNone(banned.search(block),
                                  f"{name} has a fenced command needing a key/account")


class StarterLogic(unittest.TestCase):
    """The router: parsing, sanitize, allowlists, timers — all offline."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="housevoice-test-")
        self._saved = dict(household.__dict__)
        self._saved_profile = config.PROFILE
        config.DATA_DIR = self._tmp
        household.DATA_DIR = self._tmp
        household.LISTS_PATH = os.path.join(self._tmp, "lists.json")
        household.LOG_PATH = os.path.join(self._tmp, "log.txt")
        household.CHIME_PATH = os.path.join(self._tmp, "chime.wav")
        household.reset_for_tests()

    def tearDown(self):
        household.reset_for_tests()
        shutil.rmtree(self._tmp, ignore_errors=True)
        household.__dict__.update(self._saved)   # restore module state exactly
        config.PROFILE = self._saved_profile

    # ---- rules parser --------------------------------------------------

    def test_rules_parser_timer(self):
        got = household.parse_with_rules("set a timer for ten minutes")
        self.assertNotEqual(got.command, "SET_TIMER")   # words-not-digits fail fast
        got = household.parse_with_rules("set a timer for 10 minutes for the pasta")
        self.assertEqual(got.command, "SET_TIMER")
        self.assertEqual(got.args, {"minutes": 10.0, "label": "pasta"})

    def test_rules_parser_hour_timer(self):
        got = household.parse_with_rules("set a timer for 2 hours")
        self.assertEqual(got.command, "SET_TIMER")
        self.assertEqual(got.args["minutes"], 120.0)

    def test_rules_parser_lists(self):
        for sentence, (cmd, args) in {
            "add milk to the grocery list": ("ADD_TO_LIST", {"list": "grocery",
                                                            "item": "milk"}),
            "what's on the todo list": ("READ_LIST", {"list": "todo"}),
            "read the grocery list": ("READ_LIST", {"list": "grocery"}),
            "remove the last thing from the grocery": (
                "REMOVE_LAST", {"list": "grocery"}),
            "what time is it": ("TIME_NOW", {}),
            "tell me about penguins jazz": ("CHAT", {"text":
                                             "tell me about penguins jazz"}),
        }.items():
            with self.subTest(sentence=sentence):
                got = household.parse_with_rules(sentence)
                self.assertEqual((got.command, got.args), (cmd, args))

    def test_rules_parser_cancel(self):
        got = household.parse_with_rules("cancel the timer")
        self.assertEqual(got.command, "CANCEL_TIMER")

    # ---- sanitize ------------------------------------------------------

    def test_sanitize_rejects_out_of_range_timer(self):
        got = household.sanitize(household.Intent("SET_TIMER", {"minutes": 9000}))
        self.assertEqual(got.command, "CHAT")
        self.assertIn("range", got.args["text"])

    def test_sanitize_rejects_non_number(self):
        got = household.sanitize(household.Intent("SET_TIMER", {"minutes": "soon"}))
        self.assertEqual(got.command, "CHAT")

    def test_sanitize_rejects_unknown_list(self):
        got = household.sanitize(household.Intent("ADD_TO_LIST",
                                                  {"list": "shopping",
                                                   "item": "milk"}))
        self.assertEqual(got.command, "CHAT")       # "shopping" is not a defined list

    def test_sanitize_rejects_imposter_command(self):
        got = household.sanitize(household.Intent("RUN_SHELL", {"cmd": "ls"}))
        self.assertEqual(got.command, "CHAT")       # the load-bearing guarantee

    def test_sanitize_alias_list_allowed(self):
        got = household.sanitize(household.Intent("ADD_TO_LIST", {"list": "grocery",
                                                                  "item": "rice"}))
        self.assertEqual(got.args["list"], "grocery")

    # ---- allowlists ----------------------------------------------------

    def test_kid_mode_blocks_chat_and_grownup_lists(self):
        self.assertFalse(household.allowed(household.Intent("CHAT", {"text": "hi"}),
                                           "kid"))
        self.assertFalse(household.allowed(household.Intent("READ_LIST",
                                                            {"list": "todo"}), "kid"))
        self.assertTrue(household.allowed(household.Intent("SET_TIMER",
                                                           {"minutes": 5}), "kid"))
        self.assertTrue(household.allowed(household.Intent("ADD_TO_LIST",
                                                           {"list": "kids",
                                                            "item": "crayon"}), "kid"))

    def test_guest_mode_blocks_family_lists_and_chat(self):
        self.assertFalse(household.allowed(household.Intent("READ_LIST",
                                                            {"list": "grocery"}), "guest"))
        self.assertFalse(household.allowed(household.Intent("CHAT", {"text": "hi"}),
                                           "guest"))
        self.assertTrue(household.allowed(household.Intent("SET_TIMER",
                                                           {"minutes": 5}), "guest"))

    def test_family_mode_blocks_chat_but_not_commands(self):
        self.assertTrue(household.allowed(household.Intent("READ_LIST",
                                                           {"list": "grocery"}), "family"))
        self.assertFalse(household.allowed(household.Intent("CHAT", {"text": "hi"}),
                                           "family"))

    def test_act_refuses_in_kid_mode(self):
        out = []
        household.act(household.Intent("CHAT", {"text": "anything"}),
                      profile="kid", speak=out.append)
        self.assertIn("kid mode", out[0])
        with open(household.LOG_PATH, encoding="utf-8") as f:
            self.assertIn("REFUSED", f.read())

    def _silence_speaker_and_daytime(self):
        out = []
        saved = (household.say, household.in_quiet_hours)
        household.say = out.append                      # no speaker in CI
        household.in_quiet_hours = lambda: False       # not evening in tests
        return out, saved

    def _restore(self, saved):
        household.say, household.in_quiet_hours = saved

    # ---- lists & timers ------------------------------------------------

    def test_lists_round_trip(self):
        self.assertIn("Added", household.add_to_list("grocery", "milk"))
        self.assertIn("Added", household.add_to_list("grocery", "eggs"))
        self.assertIn("Added", household.add_to_list("todo", "call dentist"))
        reply = household.read_list("grocery")
        self.assertIn("2 things", reply)
        self.assertIn("eggs", reply)              # newest first
        self.assertIn("milk", reply)
        self.assertIn("Removed", household.remove_last("grocery"))
        reply = household.read_list("grocery")
        self.assertIn("1 thing", reply)
        self.assertNotIn("eggs", reply)
        with open(household.LISTS_PATH, encoding="utf-8") as f:
            disk = json.load(f)
        self.assertEqual([item for item, _ts in disk["grocery"]], ["milk"])

    def test_lists_politeness(self):
        self.assertIn("empty", household.read_list("grocery"))
        self.assertIn("don't have", household.read_list("shopping"))
        self.assertIn("What should I add?", household.add_to_list("grocery", "   "))

    def test_timer_set_and_cancel(self):
        reply = household.set_timer(1, "test")
        self.assertIn("Timer set", reply)
        self.assertEqual(len(household._active_timers), 1)
        self.assertIn("cancelled", household.cancel_timer())
        self.assertIn("No timer running", household.cancel_timer())

    def test_timer_bounds(self):
        self.assertNotIn("Timer set", household.set_timer(0))
        self.assertNotIn("Timer set", household.set_timer(601))
        self.assertIn("didn't come through", household.set_timer("soon"))

    def test_timer_fires_and_logs(self):
        self.assertNotIn("nothing set", household.set_timer(1, "smoke"))
        household.set_timer(1, "smoke")           # real one cancelled below
        household._active_timers.pop().cancel()   # don't wait a whole minute:
        quick = household.threading.Timer(0.05, household.timer_done, ["smoke"])
        quick.daemon = True
        quick.start()
        quick.join(2)
        with open(household.LOG_PATH, encoding="utf-8") as f:
            self.assertIn("TIMER_DONE label='smoke'", f.read())

    def test_log_readable(self):
        household.log("HEARD(text) 'test sentence'")
        with open(household.LOG_PATH, encoding="utf-8") as f:
            line = f.read().strip()
        self.assertIn("HEARD", line)
        self.assertIn(datetime.now().strftime("%Y-%m-%d"), line)

    def test_run_text_fires_timer(self):
        out, saved = self._silence_speaker_and_daytime()
        try:
            household.run_text("set a timer for 3 minutes for cookies")
            self.assertTrue(household._active_timers)
            self.assertIn("Timer set", out[-1])
        finally:
            household.cancel_timer()
            self._restore(saved)

    def test_run_text_kid_refuse_chat(self):
        out, saved = self._silence_speaker_and_daytime()
        try:
            household.run_text("tell me a joke about socks", profile="kid")
            self.assertIn("kid mode", out[-1])
            with open(household.LOG_PATH, encoding="utf-8") as f:
                self.assertIn("REFUSED", f.read())
        finally:
            self._restore(saved)

    def test_run_text_quiet_hours_prints_only(self):
        out, saved = self._silence_speaker_and_daytime()
        household.in_quiet_hours = lambda: True
        printed = []
        import builtins
        real_print = builtins.print
        quiet_capture = lambda *a, **k: printed.append(" ".join(map(str, a)))
        builtins_print_backup = builtins.print
        builtins.print = quiet_capture
        try:
            household.run_text("add cocoa to the grocery list")
            self.assertTrue(any("quiet hours" in p for p in printed))
            with open(household.LOG_PATH, encoding="utf-8") as f:
                self.assertIn("ADD_TO_LIST", f.read())
        finally:
            builtins.print = builtins_print_backup
            self._restore(saved)

    def test_config_is_keyless_and_localhost_only(self):
        with open(os.path.join(STARTER, "config.py"), encoding="utf-8") as f:
            source = f.read()
        self.assertIn("127.0.0.1", source)          # brain is localhost only
        self.assertNotIn("os.environ", source)      # no env-var secrets config

    def test_cli_runs_as_documented(self):
        """docs/08 Step 4: the typed pipeline runs with no Ollama, no keys."""
        run = subprocess.run([sys.executable, "household.py", "--text",
                              "set a timer for 10 minutes for the pasta"],
                             cwd=STARTER, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("Timer set", run.stdout)
        run2 = subprocess.run([sys.executable, "config.py"], cwd=STARTER,
                              capture_output=True, text=True)
        self.assertEqual(run2.returncode, 0)
        self.assertIn("wake word", run2.stdout)
        self.assertIn("llama3.2:3b", run2.stdout)


if __name__ == "__main__":
    unittest.main()
