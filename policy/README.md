# The shared ErosCraft adult policy

One policy for every ErosCraft workflow, in three files:

| File | What it is |
|---|---|
| [`POLICY.md`](POLICY.md) | The policy in words: the two gates, the two rules, fail-closed, what is measured. |
| [`eroscraft-adult-policy.json`](eroscraft-adult-policy.json) | The same policy for code: gates, rules, facts and their questions, the checker prompt, every stop sentence (image and video wording), the Civitai refusals. |
| [`adult_policy.py`](adult_policy.py) | The reader. Standard library only. Refuses a file that weakens the policy, and resolves each message for the workflow's medium. |

[`test_policy.py`](test_policy.py) proves the file says exactly what the Qwen 2.1 pack says today, word for word,
and that a weakened copy is refused. `python3 policy/test_policy.py` runs it with no GPU and no ComfyUI.

This folder is in `.comfyignore`, so it is not part of the Qwen 2.1 node pack on the Registry until that pack adopts
it as below.

## What is shared and what is not

**Shared** (in the file): the gates, the rules, the fact questions, the checker system prompt, the fail-closed
reading, every stop sentence, the Civitai refused flags and words.

**Each workflow's own** (stays in its pack): the policy engine `policy.py` and its `verdict()`, which nodes check
what, which model answers, the output folder, the Civitai host and base-model filter, recommended LoRAs and their
sampling. The file supplies words; the decision to stop stays in the engine.

## Wiring it into a workflow

Every workflow already ships an adult pack (`ComfyUI-<Model>-Adult-Policy`) whose `policy.py` is generated from the
shared engine by `_build/derive.py`. The shared policy rides the same step.

1. **Derive it in.** `derive.py` copies `eroscraft-adult-policy.json` and `adult_policy.py` into the pack folder
   (`<pack>/<module>/`) beside `policy.py`, and lists both in `.claude/generated.txt` so the guard hook refuses a hand
   edit. `derive.py --check` compares them byte for byte with this folder, as it already does for the engine.
2. **Ship it.** Add both files to the script's `ZIP_EXTRA`, so the zip and `publish_pack.py` carry them.
3. **Read it in `policies.py`.** Load once at import, for the pack's medium:

       from .adult_policy import load
       SHARED = load(media="image")          # "video" for Wan 2.2 and MiniMax H3

       MINOR_TEXT = Fact("minor", SHARED.question("minor"))
       FAMOUS_TEXT = Fact("well_known_real_person", SHARED.question("well_known_real_person"))
       AGE_IMAGE = Fact("anyone_under_18", SHARED.question("anyone_under_18"))
       STOPS = {"toggle_consent": SHARED.messages["gates_off"]["consent"],
                "toggle_adult": SHARED.messages["gates_off"]["adult"], **SHARED.messages["request"]}
       REWRITE_STOPS = SHARED.messages["rewrite"]
       OUTPUT_STOPS = SHARED.messages["output"]
       UNCLEAR, OUTPUT_UNCLEAR = SHARED.messages["unclear"]["request"], SHARED.messages["unclear"]["output"]
       gates_off, refused_words = SHARED.gates_off, SHARED.refused_words

   A missing or weakened file raises at import, so the pack does not load and nothing samples: fail closed.
4. **Test it.** The suite asserts the pack's constants equal the file's (this folder's `_matches` is the check to
   copy) and that `SHARED.version` is the one the handbook names.
5. **Bump** the workflow's patch version in its seven places, rebuild the zip, and export the pack.

A workflow that only uses some checkpoints (no prompt enhancer, so no rewrite check) simply never shows the
`rewrite` sentences. It may not drop a checkpoint the file lists for a rule it has inputs for.

## Qwen 2.1 adopts it first

Qwen 2.1 goes first because nothing changes for a person using it: every word in the file was copied from its
`qwen21_adult_policy/policies.py` and `civitai.py`, and `test_policy.py` proves they are equal today. Its pack also
carries its own engine and loads alone, so it needs nothing from another pack. The Wan 2.2 wording was checked the
same way against the workspace copy (`WAN22_POLICIES=... python3 policy/test_policy.py`).

The steps, in the private `eroscraft-image-creator-qwen-2.1` repository, by the session that owns it:

1. Put this folder where every workflow can derive from it (proposed: the workspace's `eroscraft/policy/`, next to
   the shared engine's source) and have Qwen 2.1's `derive.py` copy the two files into `qwen21_adult_policy/`.
2. In `policies.py`, replace the literal `MINOR_TEXT`, `FAMOUS_TEXT`, `STOPS`, `REWRITE_STOPS`, `OUTPUT_STOPS`,
   `UNCLEAR`, `OUTPUT_UNCLEAR`, the three gate sentences, `gates_off` and `REFUSED_WORDS`/`refused_words` with reads
   from `load(media="image")`, as in step 3 above. In `civitai.py` (generated), nothing changes: its
   `REFUSED_FLAGS` and reasons already equal the file's, and the suite asserts it.
3. Add the two files to `ZIP_EXTRA` and `.claude/generated.txt`; move `test_policy.py`'s checks into `suite.py`.
4. Release 1.1.5: the seven version spots, the zip, then `publish_pack.py` exports the pack here and the Registry
   publishes it. The free tier of `_build/appe2e.py` should show every stop sentence unchanged.

Then Wan 2.2 and MiniMax H3 (`media="video"`), then Krea 2, Anima and the Character Creator, each by its own session.
