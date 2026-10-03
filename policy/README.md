# The ErosCraft adult policy

One adult policy for every ErosCraft workflow, whatever model it runs. Nothing in the policy names a model: the
gates, the rules, the questions and the stop sentences are the same for all of them, and each workflow is one entry
under `workflows` saying which medium it makes and which checkpoints it has.

| File | What it is |
|---|---|
| [`POLICY.md`](POLICY.md) | The policy in words: the two gates, the two rules, fail-closed, what is measured. |
| [`eroscraft-adult-policy.json`](eroscraft-adult-policy.json) | The same policy for code: gates, rules, facts and their questions, the checker prompt, every stop sentence (image and video wording), the Civitai refusals, and the workflow list. |
| [`adult_policy.py`](adult_policy.py) | The reader. Standard library only. Refuses a file that weakens the policy, applies a workflow's entry, and resolves each message for its medium. |
| [`test_policy.py`](test_policy.py) | `python3 policy/test_policy.py`, no GPU and no ComfyUI. Proves the file equals the words the packs show today and that a weakened file or workflow entry is refused. |
| [`HANDOFF.md`](HANDOFF.md) | The session record: where the policy stands gate by gate, the decisions made, what waits on whom. |

This folder is in `.comfyignore`, so the Registry's `node.zip` of the Qwen 2.1 node pack also published from this
repository never carries it. A pack that adopts the policy carries its own derived copy of the JSON and the reader in
its module folder instead (Qwen 2.1 does, since its 1.4.0 source).

## The workflows

| Workflow | Medium | Pack | Checkpoints | Words compared |
|---|---|---|---|---|
| `eroscraft-image-creator-qwen-2.1` | image | ComfyUI-Qwen21-Adult-Policy | request, rewrite, inputs, output | 2026-10-03, equal |
| `eroscraft-video-creator-wan-2.2` | video | ComfyUI-Wan22-Adult-Policy | request, inputs, output | 2026-10-03, equal |
| `eroscraft-video-creator-minimax-h3` | video | ComfyUI-H3-Adult-Policy | request, inputs, output | 2026-10-03, equal with five stops reworded in its entry |
| `eroscraft-image-creator-krea-2` | image | ComfyUI-Krea2-Adult-Policy | request, rewrite, inputs, output | not yet |
| `eroscraft-character-creator-krea-2` | image | ComfyUI-Krea2CC-Gate | request, inputs, output | not yet |
| `eroscraft-image-creator-anima` | image | none yet (a stub) | request, inputs, output | not yet |

"Not yet" means that workflow's pack has not been compared with the file, so its checkpoints above are a first
guess its session confirms when it adopts. A new workflow adds its own row to `workflows` in the same change that
wires it in.

## What a workflow may set, and what it may not

**The policy, the same for all:** the two gates, the two rules and where each is checked, the fact questions, the
checker system prompt, the fail-closed reading, every stop sentence, the Civitai refused flags and words.

**A workflow's entry, optional:**

- `media`: `image` or `video`, which picks the wording of every message that has two.
- `checkpoints`: which of `request`, `rewrite`, `inputs`, `output` it runs. `request` and `output` are required of
  every workflow; `rewrite` is required when it has a prompt enhancer, `inputs` when it takes photos or clips.
- `messages`: a rewording of a stop sentence the policy already shows, when the medium's wording does not fit (a
  trainer's proof render, say). It can only reword: a new stop, an empty sentence or one missing the workflow's
  medium is refused.
- `pack`, `civitai_picker`, `words_checked`: what the pack is called, whether it has the picker, when its words
  were last compared.

Anything else in an entry, such as `gates`, `rules`, `facts` or `fail_closed`, is refused, so no workflow can turn
a check off for itself.

**Each pack's own, outside this file:** the policy engine `policy.py` and its `verdict()`, which nodes check what,
which model answers the questions, the output folder, the Civitai host and base-model filter, recommended LoRAs.
The file supplies the words; the decision to stop stays in the engine.

## Wiring it into a workflow

Where a workflow's adult pack is generated in part by its `_build/derive.py` (Qwen 2.1 and MiniMax H3 derive their
`policy.py` that way), the policy rides the same step. A workflow without one (the Character Creator, whose pack is
`ComfyUI-Krea2CC-Gate`) copies the two files in its own build step and lists them as generated the same way.

1. **List it.** Add or confirm the workflow's row under `workflows`.
2. **Derive it in.** `derive.py` copies `eroscraft-adult-policy.json` and `adult_policy.py` into the pack's module
   folder beside `policy.py`, and lists both in `.claude/generated.txt` so the guard hook refuses a hand edit.
   `derive.py --check` compares them byte for byte with the source, as it does for the engine.
3. **Ship it.** Add both files to the script's `ZIP_EXTRA`, so the zip and `publish_pack.py` carry them.
4. **Read it in `policies.py`**, once at import:

       from .adult_policy import load
       SHARED = load("eroscraft-image-creator-qwen-2.1")      # the workflow's own folder name

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
5. **Test it.** The suite asserts the pack's constants equal the file's (`_matches` in `test_policy.py` is the check
   to copy) and that `SHARED.version` is the one the handbook names.
6. **Release.** The workflow's patch version in its seven places, the zip, then the pack's export.

## The order

1. **Qwen 2.1, done** (2026-10-03, eroscraft-image-creator-qwen-2.1 #47, #48 and #49, in its 1.4.0 source). Its
   `derive.py` copies the two files into `qwen21_adult_policy/`, `policies.py` reads every question, stop sentence,
   gate sentence and refused word from `load("eroscraft-image-creator-qwen-2.1")`, and both zips carry the copies,
   byte for byte equal to this folder (measured 2026-10-03, `HANDOFF.md`).
2. **Wan 2.2**, already compared equal on the video wording (`WAN22_POLICIES=... python3 policy/test_policy.py`).
3. **MiniMax H3, Krea 2, the Character Creator**: each compares its words first. Where its sentence differs, either
   the pack moves to the policy's wording or the workflow's entry rewords it; the decision is recorded in
   `HANDOFF.md`. MiniMax H3 is compared: its entry rewords five stops (#9; `HANDOFF.md`, D2).
4. **Anima** wires it in when its pack is built, from the start.

## Where this lives

This repository is the home of the adult policy for all ErosCraft workflows, and `policy/` is its source. Each
workflow's build reads it from here (a checkout of this repository beside the workflow's own folder,
`../ComfyUI-Adult-Policy`, or wherever `CRAFT_POLICY` points; Qwen 2.1's `derive.yml` checks it out the same way on
CI) and copies it into its pack. The Qwen 2.1 node pack also
published from this repository is an export, as `.github/CONTRIBUTING.md` says; this folder is not.

**The pack export:** the workspace's `eroscraft/_build/publish_pack.py` exports the Qwen 2.1 pack to this
repository, `Eros-Craft/ComfyUI-Adult-Policy`, and leaves `policy/` in place and out of the Registry's `node.zip`
once Eros-Craft/ErosCraft#45 is merged; until then an export would delete it, so none runs. The pack keeps its own
name, Registry node id and module; only the repository was renamed.

The pack exported here is still 1.1.4, from before it adopted the policy. Its source in the private Qwen 2.1
repository is 1.4.0 and passes `test_policy.py` with this folder (measured 2026-10-03). Its export is a Registry
publish, which the Qwen 2.1 project makes when its owner says so (`HANDOFF.md`).
