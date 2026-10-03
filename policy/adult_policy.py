"""The reader for `eroscraft-adult-policy.json`, the one policy every ErosCraft workflow shares.

Pure Python, standard library only (NO ComfyUI imports), so a pack can copy this file beside its own engine and the
suite can run it off a GPU and off a server.

It does two things and nothing else:

  * `load()` reads the file, REFUSES one that weakens the policy (see `validate`), and picks each message for the
    workflow's medium, "image" or "video", so a pack sees plain strings.
  * `refused_words()` is the Civitai picker's word check, built from the file's list.

Deciding whether a run proceeds stays in each pack's engine (`policy.py`, `verdict()`): this file supplies the words
the engine asks and shows, never the decision.
"""
import json
import pathlib
import re

SCHEMA = 1
MEDIA = ("image", "video")
FILE_NAME = "eroscraft-adult-policy.json"

# What no copy of the file may change. A pack that loads a file without these stops at import, which is the
# fail-closed answer for a policy: a workflow that cannot read its rules does not run.
REQUIRED_GATES = ("consent", "adult")
REQUIRED_RULES = {
    "no_minors": {"request", "rewrite", "inputs", "output"},
    "no_famous_real_person": {"request", "rewrite"},
}


class PolicyError(ValueError):
    """The file is missing, unreadable, or weakens the policy."""


def validate(data):
    """Raise PolicyError when `data` is not a whole, unweakened policy. Returns `data` unchanged."""
    if data.get("schema") != SCHEMA:
        raise PolicyError("schema %r is not %d; this reader cannot judge it" % (data.get("schema"), SCHEMA))

    gates = {g.get("key"): g for g in data.get("gates") or ()}
    if tuple(sorted(gates)) != tuple(sorted(REQUIRED_GATES)):
        raise PolicyError("the gates are exactly %s, got %s" % (", ".join(REQUIRED_GATES), ", ".join(gates)))
    for key, gate in gates.items():
        if gate.get("default") is not False:
            raise PolicyError("the %s gate must ship off" % key)

    facts = {f.get("key"): f for f in data.get("facts") or ()}
    for f in facts.values():
        if f.get("unsafe") is not True or not str(f.get("question") or "").strip():
            raise PolicyError("fact %r needs a question and unsafe: true" % f.get("key"))

    rules = {r.get("key"): r for r in data.get("rules") or ()}
    for key, where in REQUIRED_RULES.items():
        rule = rules.get(key)
        if rule is None:
            raise PolicyError("rule %s is missing" % key)
        if rule.get("overridable") is not False:
            raise PolicyError("rule %s must not be overridable" % key)
        missing = where - set(rule.get("checked_at") or ())
        if missing:
            raise PolicyError("rule %s is no longer checked at %s" % (key, ", ".join(sorted(missing))))
        for fact in rule.get("facts") or ():
            if fact not in facts:
                raise PolicyError("rule %s names fact %s, which the file does not ask" % (key, fact))
        if not rule.get("facts"):
            raise PolicyError("rule %s asks no fact" % key)

    if (data.get("fail_closed") or {}).get("required") is not True:
        raise PolicyError("fail_closed.required must be true")
    words = (data.get("fail_closed") or {}).get("answer_words") or {}
    if words.get("safe") != ["no"]:
        raise PolicyError("only a plain 'no' may read as safe")

    messages = data.get("messages") or {}
    for section in ("request", "rewrite"):
        for fact in (f for r in rules.values() for f in r.get("facts") or () if facts[f].get("asked_of") == "text"):
            if fact not in (messages.get(section) or {}):
                raise PolicyError("no %s message for fact %s" % (section, fact))
    for fact in (k for k, f in facts.items() if f.get("asked_of") == "image"):
        for section in ("request", "output"):
            if fact not in (messages.get(section) or {}):
                raise PolicyError("no %s message for fact %s" % (section, fact))

    if not (data.get("civitai") or {}).get("refused_words"):
        raise PolicyError("civitai.refused_words is empty")
    return data


def _pick(value, media):
    """A message is a string, or {"image": ..., "video": ...}. Return the string for `media`."""
    if isinstance(value, dict):
        if media not in value:
            raise PolicyError("a message has no %s wording" % media)
        return value[media]
    return value


def _resolve(tree, media):
    return {k: (_resolve(v, media) if isinstance(v, dict) and not set(v) <= set(MEDIA) else _pick(v, media))
            for k, v in tree.items()}


class AdultPolicy:
    """The file, validated, with every message resolved for one medium."""

    def __init__(self, data, media):
        self.data = data
        self.media = media
        self.version = data["version"]
        self.gates = tuple(g["key"] for g in data["gates"])
        self.facts = {f["key"]: f for f in data["facts"]}
        self.system = data["checker"]["system"]
        self.messages = _resolve(data["messages"], media)
        civitai = data["civitai"]
        self.refused_flags = dict(civitai.get("refused_flags") or {})
        self.refused_word_list = tuple(civitai["refused_words"])
        self._refused_re = re.compile(r"(?<![a-z])(%s)(?![a-z])"
                                      % "|".join(re.escape(w) for w in self.refused_word_list), re.I)

    def question(self, key):
        return self.facts[key]["question"]

    def gates_off(self, toggle_state):
        """The one sentence for the gates that are off, in the form's order, or "" when both are on."""
        off = tuple(k for k in self.gates if not toggle_state.get(k))
        g = self.messages["gates_off"]
        return {(): "", ("consent",): g["consent"], ("adult",): g["adult"]}.get(off, g["both"])

    def refused_words(self, *texts):
        """The first refused word in any of `texts` (a model's name, its tags, a version's name), or None."""
        for t in texts:
            m = self._refused_re.search(str(t or ""))
            if m:
                return m.group(1).lower()
        return None


def load(path=None, media="image"):
    """Read and validate the policy file. `path` defaults to the file beside this one."""
    if media not in MEDIA:
        raise PolicyError("media is one of %s, not %r" % (", ".join(MEDIA), media))
    path = pathlib.Path(path) if path else pathlib.Path(__file__).resolve().with_name(FILE_NAME)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise PolicyError("cannot read %s: %s" % (path, exc)) from exc
    return AdultPolicy(validate(data), media)
