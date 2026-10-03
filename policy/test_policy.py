"""Proves the shared policy file says exactly what the Qwen 2.1 pack says today, and that a weakened copy is refused.

Run it with `python3 policy/test_policy.py` (or pytest). Standard library only, no GPU, no ComfyUI. A pack that adopts
the file gets this test's second half for free: equal words now means adopting the file changes no behaviour.

Optional: `WAN22_POLICIES=/path/to/wan22_adult_policy/policies.py python3 policy/test_policy.py` checks the video
wording against the Wan 2.2 pack the same way. It lives in the private workspace, so without it that test skips.
`H3_POLICIES=/path/to/h3_adult_policy/policies.py` does the same for MiniMax H3, through its entry's rewording.
"""
import copy
import importlib.util
import json
import os
import pathlib
import sys

sys.dont_write_bytecode = True      # a test run leaves nothing in the export to commit by mistake
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import adult_policy as ap  # noqa: E402

RAW = json.loads((HERE / ap.FILE_NAME).read_text(encoding="utf-8"))


def _module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _pack_policies(path, name):
    """A pack's policies.py, loaded by path beside its generated engine (its by-path fallback handles that)."""
    return _module(name, pathlib.Path(path))


# The words each version of the file changed, by the names `_matches` gives them. A pack that copied its words before
# a change (its own literals, or a derived copy of an older file) shows the old words until it re-derives, so those
# names are left out for it, and only those: every other word must still be equal.
CHANGED_IN = {
    "0.1.2": {"unclear"},       # the request's unclear stop: rerunning gets the same answer, so reword instead
}


def _ver(v):
    return tuple(int(x) for x in v.split("."))


def _behind(mod):
    """The names a pack may still show in an older wording: those changed after the file version it read."""
    shared = getattr(mod, "SHARED", None)
    read = getattr(shared, "version", "0.1.1")    # a pack with its own literals was last compared at 0.1.1
    return set().union(*(names for ver, names in CHANGED_IN.items() if _ver(ver) > _ver(read)))


def _matches(pol, mod):
    """Every word a pack asks and shows, compared with the shared file resolved for its medium."""
    m = pol.messages
    pairs = {
        "minor question": (pol.question("minor"), mod.MINOR_TEXT.question),
        "famous question": (pol.question("well_known_real_person"), mod.FAMOUS_TEXT.question),
        "age question": (pol.question("anyone_under_18"), mod.AGE_FACT_QUESTION),
        "checker system": (pol.system, mod.FACT_SYSTEM),
        "consent off": (m["gates_off"]["consent"], mod.CONSENT_OFF),
        "adult off": (m["gates_off"]["adult"], mod.ADULT_OFF),
        "both off": (m["gates_off"]["both"], mod.BOTH_GATES_OFF),
        "unclear": (m["unclear"]["request"], mod.UNCLEAR),
        "output unclear": (m["unclear"]["output"], mod.OUTPUT_UNCLEAR),
    }
    for key in ("minor", "anyone_under_18", "well_known_real_person"):
        pairs["request stop " + key] = (m["request"][key], mod.STOPS[key])
    for key, text in mod.OUTPUT_STOPS.items():
        pairs["output stop " + key] = (m["output"][key], text)
    for key, text in getattr(mod, "REWRITE_STOPS", {}).items():
        pairs["rewrite stop " + key] = (m["rewrite"][key], text)
    if hasattr(mod, "REFUSED_WORDS"):
        pairs["refused words"] = (pol.refused_word_list, tuple(mod.REFUSED_WORDS))
    behind = _behind(mod)
    bad = [k for k, (a, b) in pairs.items() if a != b and k not in behind]
    assert not bad, "the shared file and the pack differ on: " + ", ".join(bad)


# --------------------------------------------------------------------------- the file matches the packs

def test_file_loads_for_both_media():
    for media in ap.MEDIA:
        pol = ap.load(media=media)
        assert pol.gates == ("consent", "adult")
        assert all(isinstance(v, str) for s in pol.messages.values() for v in
                   (s.values() if isinstance(s, dict) else [s]) if not isinstance(v, dict))


def test_matches_qwen21_pack():
    mod = _pack_policies(HERE.parent / "qwen21_adult_policy" / "policies.py", "qwen21_policies_under_test")
    _matches(ap.load("eroscraft-image-creator-qwen-2.1"), mod)
    civitai = _module("qwen21_civitai_under_test", HERE.parent / "qwen21_adult_policy" / "civitai.py")
    assert tuple(RAW["civitai"]["refused_flags"]) == civitai.REFUSED_FLAGS
    for flag, reason in RAW["civitai"]["refused_flags"].items():
        version = {"baseModel": "Qwen 2.1", flag: True}
        assert civitai.civitai_refusal(version) == reason


def test_matches_wan22_pack():
    path = os.environ.get("WAN22_POLICIES")
    if not path:
        print("skip: WAN22_POLICIES is unset (the Wan 2.2 pack lives in the private workspace)")
        return
    _matches(ap.load("eroscraft-video-creator-wan-2.2"), _pack_policies(path, "wan22_policies_under_test"))


H3 = "eroscraft-video-creator-minimax-h3"
# The five stop sentences MiniMax H3 words its own way (compared 2026-10-03). Every other word it shows is the file's.
H3_REWORDED = {("request", "minor"), ("request", "anyone_under_18"), ("output", "anyone_under_18"),
               ("unclear", "request"), ("unclear", "output")}


def test_matches_h3_pack():
    path = os.environ.get("H3_POLICIES")
    if not path:
        print("skip: H3_POLICIES is unset (the MiniMax H3 pack lives in its own repository)")
        return
    _matches(ap.load(H3), _pack_policies(path, "h3_policies_under_test"))


def test_h3_rewords_only_its_five_stops():
    pol, plain = ap.load(H3), ap.load(media="video")
    changed = {(s, k) for s, entries in plain.messages.items() for k in entries
               if pol.messages[s][k] != plain.messages[s][k]}
    assert changed == H3_REWORDED, changed
    for section, key in H3_REWORDED:                    # a rewording keeps the policy's own sentence, then adds
        assert pol.messages[section][key].startswith(plain.messages[section][key].split(":")[0]), (section, key)


def test_refused_words_agree_with_qwen21():
    mod = _pack_policies(HERE.parent / "qwen21_adult_policy" / "policies.py", "qwen21_policies_under_test")
    pol = ap.load()
    for text in ("Teen outfit LoRA", "celeb lookalike", "Lingerie Studio", "Adult Woman Portrait", "Kidney beans"):
        assert pol.refused_words(text) == mod.refused_words(text), text


def test_gates_off_sentences():
    pol = ap.load()
    assert pol.gates_off({"consent": True, "adult": True}) == ""
    assert pol.gates_off({}) == pol.messages["gates_off"]["both"]
    assert pol.gates_off({"consent": True}) == pol.messages["gates_off"]["adult"]


# --------------------------------------------------------------------------- a weakened copy is refused

def _refused(mutate):
    data = copy.deepcopy(RAW)
    mutate(data)
    try:
        ap.validate(data)
    except ap.PolicyError:
        return
    raise AssertionError("a weakened policy was accepted")


def test_weakened_copies_are_refused():
    _refused(lambda d: d["gates"].pop())                                           # a gate removed
    _refused(lambda d: d["gates"][0].update(default=True))                          # a gate shipped on
    _refused(lambda d: d["gates"].append({"key": "skip_checks", "default": False})) # a new toggle
    _refused(lambda d: d["rules"].pop(0))                                           # nobody-under-18 removed
    _refused(lambda d: d["rules"][1].update(overridable=True))                      # a rule made optional
    _refused(lambda d: d["rules"][0]["checked_at"].remove("output"))                # the output check dropped
    _refused(lambda d: d["rules"][0]["facts"].append("not_a_fact"))                 # a rule naming nothing
    _refused(lambda d: d["facts"][0].update(unsafe=False))                          # a fact inverted
    _refused(lambda d: d["fail_closed"].update(required=False))                     # fail open
    _refused(lambda d: d["fail_closed"]["answer_words"]["safe"].append("unsure"))   # a maybe read as safe
    _refused(lambda d: d["messages"]["output"].pop("anyone_under_18"))              # a stop with no sentence
    _refused(lambda d: d["rules"][1]["checked_at"].remove("inputs"))                # photos no longer checked for fame
    _refused(lambda d: d["rules"][1]["facts"].remove("famous_person_in_image"))     # checked on photos, asking nothing
    _refused(lambda d: d["messages"]["request"].pop("famous_person_in_image"))      # a photo stop with no sentence
    _refused(lambda d: d["civitai"].update(refused_words=[]))                       # the picker unguarded
    _refused(lambda d: d.update(schema=2))                                          # a schema this reader can't judge


def test_weakened_workflow_entries_are_refused():
    qwen = "eroscraft-image-creator-qwen-2.1"
    _refused(lambda d: d["workflows"][qwen].update(gates=[]))                      # a workflow touching a gate
    _refused(lambda d: d["workflows"][qwen].update(rules=[]))                      # or a rule
    _refused(lambda d: d["workflows"][qwen].update(fail_closed={"required": False}))
    _refused(lambda d: d["workflows"][qwen]["checkpoints"].remove("output"))      # the output check dropped
    _refused(lambda d: d["workflows"][qwen].update(media="audio"))
    _refused(lambda d: d["workflows"][qwen].update(messages={"request": {"new_stop": "x"}}))
    _refused(lambda d: d["workflows"][qwen].update(messages={"request": {"minor": ""}}))
    _refused(lambda d: d["workflows"][qwen].update(messages={"request": {"minor": {"video": "x"}}}))


# --------------------------------------------------------------------------- one policy, every workflow

def test_every_workflow_loads():
    for name, entry in RAW["workflows"].items():
        pol = ap.load(name)
        assert pol.media == entry["media"] and pol.workflow == name
        assert {"request", "output"} <= set(pol.checkpoints)
        reworded = ((entry.get("messages") or {}).get("request") or {}).get("minor")
        assert pol.messages["request"]["minor"] == (reworded or RAW["messages"]["request"]["minor"])


def test_a_workflow_may_reword_a_stop_and_nothing_else():
    data = copy.deepcopy(RAW)
    data["workflows"]["eroscraft-video-creator-wan-2.2"]["messages"] = {
        "output": {"anyone_under_18": "A frame reads as someone under 18, so the clip was not saved."}}
    path = HERE / "_reworded_under_test.json"
    try:
        path.write_text(json.dumps(data), encoding="utf-8")
        pol = ap.load("eroscraft-video-creator-wan-2.2", path=path)
        assert pol.messages["output"]["anyone_under_18"].startswith("A frame reads")
        assert pol.messages["request"]["minor"] == RAW["messages"]["request"]["minor"]
        assert ap.load("eroscraft-image-creator-qwen-2.1", path=path).messages == ap.load(
            "eroscraft-image-creator-qwen-2.1").messages
    finally:
        path.unlink()


def test_an_unlisted_workflow_names_its_medium():
    try:
        ap.load("eroscraft-image-creator-new-model")
    except ap.PolicyError:
        pass
    else:
        raise AssertionError("an unlisted workflow loaded without a medium")
    assert ap.load("eroscraft-image-creator-new-model", media="video").media == "video"


def test_unclear_request_says_reword_not_rerun():
    """The checker decodes greedily, so the same words and photos get the same unclear answer every time (Qwen 2.1's
    T2 reproduced it). The request's unclear stop tells the person to reword; the output's may say run again, since a
    new run draws a new picture."""
    for media in ap.MEDIA:
        m = ap.load(media=media).messages["unclear"]
        assert "run it again" not in m["request"] and "Reword it" in m["request"]
        assert "a finding about your request" in m["request"]          # never tells them they asked for a minor
        assert "run it again" in m["output"]
    assert all(_ver(v) <= _ver(RAW["version"]) for v in CHANGED_IN), "CHANGED_IN names a version the file is not at yet"


def test_a_famous_face_in_a_photo_is_asked():
    """Rule 2 checked only the words, so a famous person in an uploaded photo with no name typed was never asked
    (Qwen 2.1's rule 3 audit, 2026-10-03). 0.1.3 asks every photo or clip the person adds, in the same call as the age
    question; the stop names nobody, and the fact is marked unmeasured because measuring it needs photos of real
    famous people."""
    fact = next(f for f in RAW["facts"] if f["key"] == "famous_person_in_image")
    assert fact["asked_of"] == "image" and fact["unsafe"] is True and fact["measured"].startswith("unmeasured")
    rule = next(r for r in RAW["rules"] if r["key"] == "no_famous_real_person")
    assert "famous_person_in_image" in rule["facts"] and "inputs" in rule["checked_at"]
    assert "output" not in rule["checked_at"] and "famous_person_in_image" not in RAW["messages"]["output"]
    for media in ap.MEDIA:
        stop = ap.load(media=media).messages["request"]["famous_person_in_image"]
        assert "famous real person" in stop and "{" not in stop and "nothing was made" in stop


def test_document_names_the_file_version():
    first = (HERE / "POLICY.md").read_text(encoding="utf-8").split("Version ", 1)[1]
    assert first.startswith(RAW["version"] + ","), "POLICY.md and the file name different versions"


def test_no_em_dash_ships():
    dash = chr(0x2014)
    for path in HERE.iterdir():
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            assert dash not in text and ("\\" + "u2014") not in text, path.name


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]
    for name, fn in tests:
        fn()
        print("ok", name)
    print("%d passed" % len(tests))
