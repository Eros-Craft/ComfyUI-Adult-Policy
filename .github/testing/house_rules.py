#!/usr/bin/env python3
"""What the pack export and the Comfy Registry would refuse, caught on the pull request instead of at release.

    python3 .github/testing/house_rules.py

Over every git-tracked file but the licence (kept verbatim): the refusals of the workspace's pack export
(eroscraft/_build/publish_pack.py, FORBIDDEN): the other brand's name, an em dash in any spelling, a token-shaped
string, a path under /Users/. Over every tracked Python file: the Registry's security rules (ruff S102, S307, E702,
the same `REGISTRY_RULES` the export runs). And policy/eroscraft-adult-policy.json parses. Standard library, plus
ruff (or uvx) for the second part. Exit 0 only when nothing is found.
"""
import json
import pathlib
import re
import shutil
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
EXEMPT = {"LICENSE"}
FORBIDDEN = (
    ("the other brand's name", re.compile("soul" + r"-?" + "craft", re.I)),
    # built by code point, so this file holds no dash in any spelling
    ("an em dash", re.compile("|".join(re.escape(x) for x in (chr(0x2014), "\\" + "u" + "2014", "&" + "mdash;",
                                                              "&#" + "8212;")))),
    ("a token-shaped string", re.compile(r"hf_[A-Za-z0-9]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}"
                                         r"|BEGIN [A-Z ]*PRIVATE KEY|(?<![0-9a-f])[0-9a-f]{32}(?![0-9a-f])")),
    ("a path under /Users/", re.compile(r"/Users/[A-Za-z]")),
)
REGISTRY_RULES = "S102,S307,E702"


def tracked():
    out = subprocess.run(["git", "ls-files", "-z"], cwd=REPO, capture_output=True, text=True, check=True).stdout
    return [f for f in out.split("\0") if f and f not in EXEMPT and (REPO / f).is_file()]


def main():
    problems = []
    files = tracked()
    for rel in files:
        try:
            text = (REPO / rel).read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for n, line in enumerate(text.splitlines(), 1):
            for what, rx in FORBIDDEN:
                if rx.search(line):
                    problems.append(f"{rel}:{n}: {what}")
    py = [f for f in files if f.endswith(".py")]
    ruff = [shutil.which("ruff")] if shutil.which("ruff") else (["uvx", "ruff"] if shutil.which("uvx") else None)
    if ruff is None:
        problems.append("the Registry's security rules could not run: neither ruff nor uvx is on PATH")
    elif py:
        r = subprocess.run([*ruff, "check", "--isolated", "--no-cache", "--output-format", "concise",
                            "--select", REGISTRY_RULES, *py], cwd=REPO, capture_output=True, text=True)
        if r.returncode:
            problems += [ln + " (the Registry's security scan)" for ln in r.stdout.splitlines()
                         if re.match(r"^\S+:\d+:\d+: ", ln)] or [(r.stderr or r.stdout).strip()[:300]]
    try:
        json.loads((REPO / "policy" / "eroscraft-adult-policy.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        problems.append(f"policy/eroscraft-adult-policy.json: {e}")
    for p in problems:
        print(p)
    print(f"house rules: {len(files)} files, {len(py)} Python, "
          + ("nothing found" if not problems else f"{len(problems)} problem(s)"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
