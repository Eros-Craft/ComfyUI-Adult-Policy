# HANDOFF: the ErosCraft adult policy (policy/ in Eros-Craft/ComfyUI-Adult-Policy)

The session record for this repository's package: `policy/`, the one adult policy every ErosCraft workflow reads,
and the place it is proven. It lives in `policy/` because the pack export (`eroscraft/_build/publish_pack.py` in the
private workspace) removes every public file outside `.github/`, `policy/` and `.comfyignore`. Written for a reader
who was not there. The top four sections are replaced as the state changes; the entries under "Sessions" are
appended and never rewritten.

## 1. Where the package stands, gate by gate (2026-10-03 14:20 UTC, main at `3bdf059`, after #9 and #11)

What T0 to T4 and "ready to sell" mean for a policy is decided in §5, D1. Short form: the policy owes its own T0,
T1 and T3 here, and reaches buyers only inside a workflow's zip, so its T2 and T4 are its adopters' render sweep and
Verda release check.

| Gate | State | Evidence |
|---|---|---|
| T0 policy test | green | `python3 policy/test_policy.py`, 14 passed, warnings as errors; on CI in `tests.yml` on Linux, macOS and Windows, Python 3.10, 3.12 and 3.14, and in `checks.yml` (PR #10 merged with 18 of 18 checks green) |
| T0 house rules | green | `checks.yml` and `.github/testing/house_rules.py`: no other brand's name, no em dash, no token, no local home path, Registry ruff rules S102, S307, E702 |
| T1 on CI | green | `comfyui_smoke.py`, 9 of 9 rows on Linux, macOS and Windows with ComfyUI v0.38.2 and with master: the pack from a Registry-shaped zip, all 5 nodes registered, both gates refuse through the real `/prompt` with the exact sentence the policy file holds, a changed sentence caught at its gate position |
| T1 Desktop | carried by Qwen 2.1's T1 | D7: CI's macOS smoke (green, above) plus Qwen 2.1's T1 Desktop sweep, which runs the derived policy on the Mac's dev install (that sweep is the Qwen 2.1 project's; port 8296 went to it). `desktop-check.sh` stays for a later change to the pack |
| T2 Cloud check | green, with "Cloud cannot" and "skipped" rows | `comfy-cloud.yml`: the parity smoke at Comfy Cloud's own ComfyUI v0.38.2 passes; Cloud has no node library entry for the pack ("Cloud cannot": Cloud runs only its own library, and is safe for work only); the rows that read Cloud say "skipped" until the `COMFY_API_KEY` secret is set (§6) |
| T2 render | inherited, not run | a stop through a real run and an image out, on a workflow's Comfy deployment carrying the pack: owed by each adopter (Qwen 2.1's sweep is owed in its own HANDOFF §6) |
| T3 copies | one re-derive owed | Qwen 2.1 main (`717ba72`, V1.4.0): `adult_policy.py` equal below its two-line GENERATED header (source sha256 prefix `769f0da12e48b925`, this folder's file); its `eroscraft-adult-policy.json` is byte-equal to 0.1.0 (`8a7d6ed`), and both zips (`-verda.zip`, `-verda-customer.zip`) carry those exact bytes. #9 made the file 0.1.1 (MiniMax H3's entry only), so Qwen 2.1 re-derives once (§9, request 1); its words do not change (the staged test below passes with 0.1.1). Measured with `cmp` and a zip read |
| T3 export, staged | green, not run | `policy/` plus Qwen 2.1's 1.4.0 `qwen21_adult_policy/` laid side by side: `test_policy.py` 14 passed at 0.1.1; the export's refusal scan and ruff S102, S307, E702 clean over the 1.4.0 pack. ErosCraft #45 and #46 make an export keep `policy/` and rewrite `.github/` to exactly what is here (`checks.yml`, `publish_action.yml`, `dependabot.yml` and all seven community files compared equal this session) |
| T3 words, every compared pack | green | `test_policy.py` with no skip: Qwen 2.1's pack in this repository, `WAN22_POLICIES` at the Wan 2.2 pack on workspace main `288a888`, `H3_POLICIES` at MiniMax H3's main `de2168c`: 14 passed, every question and stop sentence each pack shows equal to the file resolved for its entry. Krea 2, the Character Creator and Anima are not compared yet (their projects' adoption) |
| T3 version | green for the policy; the pack here is stale | the file and `POLICY.md` both say 0.1.1, and `test_document_names_the_file_version` (#9) holds them together. The exported pack here is 1.1.4; its source is 1.4.0; the export is the Registry publish (§4) |
| T3 read as a buyer | corrected in this PR | `policy/README.md` had four stale statements (§2); `POLICY.md` read clean |
| T4 Verda | inherited, not run | the first adopter's release check, Qwen 2.1 V1.4.0 (`docs/verda-release.md` in that repository): not run |

**Ready to sell (D1): not yet.** What is left is Qwen 2.1's T1 Desktop sweep, T2 render and T4 (not run),
and the owner's merges of ErosCraft #45 and #46, plus Qwen 2.1's one re-derive to 0.1.1. Nothing in `policy/` itself is
red.

## 2. What finished overnight (2026-10-02 evening to 2026-10-03 14:15 UTC)

- Policy PRs merged: #6 (the shared policy: `POLICY.md`, the JSON, the reader, the test), #7 (the renamed
  repository's links), #8 (the Checks workflow and the community files), #10 (the ComfyUI smoke on three systems,
  the Desktop check, the Comfy Cloud check, `.github/testing/TESTING.md`), #11 (TESTING.md drops the
  required-check ask). Earlier: #2 (security policy and issue
  forms), #3 (pack 1.1.4, a check answer that only starts with "no" fails closed).
- Qwen 2.1 adopted the policy: eroscraft-image-creator-qwen-2.1 #47 (derives the two files, `policies.py` reads
  them), #48 (Krea 2's stricter answer reader), #49 (the new repository name in `derive.py`, `derive.yml`, the
  pack's Repository URL and the workflow's `aux_id`).
- The repository was renamed from ComfyUI-Qwen21-Adult-Policy to ComfyUI-Adult-Policy (the old URL redirects).
- This session: the gate definitions (§5), the measurements in §1, MiniMax H3's entry reviewed and merged (#9,
  policy 0.1.1, 14 tests, 16 of 16 checks green after its branch took `main`), and the
  README corrections: the folder's `.comfyignore` note, the claim that every pack derives its engine, the
  `eroscraft.env` variable that does not exist (it is a sibling checkout or `CRAFT_POLICY`), and "the order" and the
  1.1.4 comparison paragraph, both written before Qwen 2.1 adopted.

## 3. What spent credits, and confirmation it was torn down

Nothing. Comfy: $0 of the $5 the testing thread announced, because the gates refuse at validation, before any
model loads, so no sweep needed a GPU; nothing was deployed, so nothing is left running. Verda: no machine was
created or used by this project. GitHub Actions on this public repository cost nothing. The two Registry publishes
(1.1.3 on 2026-09-26, 1.1.4 on 2026-10-03 at 05:40 UTC) are free and are not credits.

## 4. What has not happened yet, and why

- **T1 Desktop on the Mac**: carried by Qwen 2.1's T1 Desktop sweep (D7), which that project runs.
- **T2 render and T4 Verda**: inherited from Qwen 2.1, whose render sweep and release check are not run (its
  HANDOFF §6). The policy adds no case of its own to either; its stops ride Qwen 2.1's gate and famous-name cases.
- **The 1.4.0 export of the pack to this repository**: it is the Registry publish (a changed `pyproject.toml` on
  `main` runs `publish_action.yml`), owned by the Qwen 2.1 project, and the owner's instruction stops short of
  publishing. It also must not run before ErosCraft #45 is merged, or it deletes `policy/`.
- **The other workflows' adoption**: Wan 2.2 compared equal, MiniMax H3 compared equal through its entry (#9),
  Krea 2, the Character Creator and Anima not compared. Each is its own project's change (`README.md`, "The order").
- **Registry**: versions 1.1.3 and 1.1.4 are `NodeVersionStatusFlagged` (read from `api.comfy.org/nodes/
  comfyui-qwen21-adult-policy/versions` this session), so Manager will not install them until a human review. The
  node's `repository` still reads the old name until the next publish. Both are the Qwen 2.1 project's (D3).

## 5. Decisions made

**D1. What T0 to T4 and "ready to sell" mean for the policy** (this session, 2026-10-03). Sources: the workspace's
`docs/testing-ci.md` (the ladder T0 offline, T1 Desktop, T2 Comfy Cloud, T3 package, T4 Verda), this repository's
`.github/testing/TESTING.md` (the ladder cut down to a policy and a node pack), the owner's ready-to-sell list
(2026-10-03), and the publishing plan `docs/superpowers/plans/2026-09-25-adult-node-packs-publishing.md`
("Verification"). The policy is never sold on its own; it reaches a buyer only inside a workflow's zip. So:
- T0: `test_policy.py` and the house rules green on CI on every system and Python the tests name.
- T1: the CI smoke green on the newest ComfyUI release, and the Desktop check green on the Mac's dev install.
- T2: the Cloud check and parity green, every "Cloud cannot" row with its reason; the render is the adopter's.
- T3, the package: every adopted workflow's derived copies byte-equal to `policy/` and inside its zips; the export
  staged and proven against the checks; the file's version and `POLICY.md`'s agree; `README.md` and `POLICY.md`
  read as a buyer would.
- T4: the first adopter's Verda release check passes with those copies.
- Ready to sell: all of the above, every change merged, this file current. Not publishing: no Registry version and
  no export is made by this project.

**D2. MiniMax H3's five reworded stops live in its entry, not in the shared wording** (2026-10-03). Its additions
help an adult who was stopped by mistake, but moving them into the shared file would change what Qwen 2.1's buyers
read and make Qwen 2.1 re-release for a wording change. The entry keeps the policy's own sentence first and adds,
which `test_h3_rewords_only_its_five_stops` holds. Revisit when a second workflow wants the same sentences.

**D3. Ownership** (agreed with the storefront orchestrator, relayed 2026-10-03): this project owns `policy/`; the
Qwen 2.1 project owns the node pack, its versions and every Registry publish. A change to the pack's code arrives
only through an export (`.github/CONTRIBUTING.md`).

**D4. PR #4 (pack 1.1.5, the bare-no reader) stays open until the 1.4.0 export supersedes it** (agreeing with the
13:21 comment on it): merging it would publish from the export instead of the source.

**D5. `tests` is not a required check on `main`** (the testing thread, PR #11): exports push to `main` directly.

**D7. T1 Desktop for the policy is CI's macOS smoke plus Qwen 2.1's T1 Desktop sweep** (the coordinator,
2026-10-03): the Mac port 8296 went to Qwen 2.1's sweep, which runs the derived policy, and our own Mac smoke was
cancelled. A separate Desktop run here would prove nothing that sweep does not.

**D8. Agreed with Qwen 2.1, recorded in both HANDOFFs** (2026-10-03, through the coordinator): this project owns the
`policy/` wording and Qwen 2.1 owns the pack code and publishing; no export until ErosCraft #45 and #46 merge;
Qwen 2.1 measures whether 1.1.3 and 1.1.4 can be installed, then decides between holding and releasing 1.1.5, and
says so before any merge.

**D10. The policy leaves "draft" when its first adopter passes T4** (this session, 2026-10-03). The file's
`status` and `POLICY.md`'s first line say draft. Every status change is a version change that every adopter
re-derives, so it is made once, as 1.0.0, when Qwen 2.1's Verda release check passes with the derived copies, and
not before: until a run on a buyer's machine has shown the stops, "draft" is the honest word.

**D9. Real-photo edits stay on ✅ Consent; the policy is not changed to hold them** (2026-10-03, on the storefront
orchestrator's report, relayed by the coordinator, that `eroscraft/CLAUDE.md` rule 3 holds explicit real-photo edits
until "Consent in person" ships). Rule 3 says the opposite: "An explicit edit of a real photo runs on ✅ Consent
(Paul, 2026-09-17)" (`eroscraft/CLAUDE.md:36`, workspace main `288a888`; the same in `.claude/rules/packages.md`,
"Two gates", and `docs/pipeline.md:47`), and no branch of the workspace carries other wording. The design record
agrees: D11 of `docs/superpowers/specs/2026-09-26-mac-cloud-package-design.md:30` keeps ✅ Consent required on every
explicit path, a watermark on every output, and "Consent in person" as an optional feature. Rule 3 and `POLICY.md`
("Changing this policy") both say the gates and rules move only on the owner's own words, which a relay is not. So
`POLICY.md` stays as it is. If the owner decides to hold real-photo edits until in-person consent ships (the
design names UK s.66I and asks for a lawyer's read before any sale, §7 of that spec), the change is a new stop in
the JSON's messages and a refusal in each pack's engine, made in one PR here and then re-derived by every adopter.

**D6. A policy README edit needs no version bump** (`POLICY.md`, "Changing this policy", bumps on a change to the
policy): only the JSON and the reader are derived into packs, so a README edit leaves every adopter's copy equal.

## 6. Pending approvals (stopped at a prompt or a permission check; not routed around)

| What | Why it waits | Who |
|---|---|---|
| ErosCraft #45, then #46 (publish_pack keeps `policy/`, targets the new name, writes the Checks and community files) | the session permission check refuses an unreviewed merge | the owner |
| `python3 tools/github_settings.py --repo Eros-Craft/ComfyUI-Adult-Policy` on the Mac (labels, rulesets, security settings) | the cloud proxy refuses repository-settings writes | the owner |
| The Claude GitHub App on this repository | an installation is the owner's | the owner |
| The `COMFY_API_KEY` repository secret, for `comfy-cloud.yml`'s Cloud rows | a secret value is the owner's | the owner |

## 7. Session roster (this project, 2026-10-03 14:15 UTC)

| Session | Owns | State | Next |
|---|---|---|---|
| Coordinator (project chat) | the roster, answers every question, merges | active | relays approvals |
| Policy package readiness and HANDOFF (this) | `policy/HANDOFF.md`, `policy/README.md` accuracy, the gate definitions, reviews of `policy/` PRs | working | the re-audit, §1 kept current |
| Desktop and Cloud testing setup | `.github/testing/`, `tests.yml`, `comfy-cloud.yml`, `.github/actions/` | PRs #10 and #11 merged | the Cloud rows once `COMFY_API_KEY` is set |
| GitHub best-practice repo setup | the `.github/` community files through ErosCraft #46, `tools/github_settings.py` | waiting on the owner | none until #46 merges |
| Draft the shared adult policy | policy PRs #6, #7, ErosCraft #45 | done, resolved | none |
| Wire the policy into Qwen 2.1 | Qwen 2.1 #47, #48, #49 | done, resolved | none |
| Rename the policy repo (the Mac) | the rename | done, resolved | none |
| Weekly policy adoption check (a routine) | reads each workflow's adoption state weekly | review ready | next weekly run |

## 9. Requests to other projects (sent through the coordinator; nothing edited in their repositories)

1. **To Qwen 2.1: re-derive the policy to 0.1.1.** `python3 _build/derive.py` with this repository beside it, then
   the zips; its `derive.yml` turns red the next night until then. Measured: `cmp` of its derived JSON with `main`
   differs at line 4 (the version); its pack passes `test_policy.py` against 0.1.1, so no word a buyer reads moves.
2. **To Qwen 2.1: assert the policy's version in its suite.** `policy/README.md` step 5 asks the suite to check
   `SHARED.version` against the version the handbook names; `grep` finds no such assertion in its `suite.py`.
3. **To MiniMax H3:** its entry is in (#9, 0.1.1); it can derive the two files and switch `policies.py` to reads
   (`policy/README.md`, "Wiring it into a workflow").

## 8. Known external defects (recorded, not patched here)

- **The base**: ComfyUI Base 3.6.0 `lib/85-launch.sh` lines 125 and 143 pass `--enable-cors-header`, which lets any
  web origin call the local ComfyUI API (found by the storefront orchestrator; the request is with the base's
  maintainers; nothing here edits the base). Nothing in `policy/` tells a buyer how to launch ComfyUI, so no caution
  belongs here; the testing thread's smoke binds loopback only.
- **The Registry**: 1.1.3 and 1.1.4 flagged (§4), sent to the Qwen 2.1 orchestrator by the testing thread.

## Sessions

### 1. The gates defined and measured; H3's entry reviewed; the README made true (2026-10-03, no machine)

**Proven.** §1, each row with its measurement. **How.** `python3 policy/test_policy.py`; `cmp` of
`policy/eroscraft-adult-policy.json` with Qwen 2.1's derived copy and `diff` of `adult_policy.py` below its header;
a zip read of both Qwen 2.1 zips; the staged export (copy `policy/` and Qwen 2.1's `qwen21_adult_policy/` into one
folder, run the test there, run the refusal scan and `ruff check --isolated --select S102,S307,E702`); publish_pack
from ErosCraft #46 imported and its `CHECKS`, `PUBLISH_ACTION`, `DEPENDABOT` and `community_files()` compared with
`.github/`. **Owed.** §4. **Found on the way.** §8, and the README's four stale statements, fixed in this PR.

### 2. The re-audit against the plan and the source (2026-10-03, no machine)

**Proven.** Read again against `docs/testing-ci.md`, `.github/testing/TESTING.md`, the publishing plan, root
`CLAUDE.md` and `eroscraft/CLAUDE.md` rule 3: the gate table holds, D9 holds, no em dash or refused string in
`policy/` (`house_rules.py`, 35 files). Added: the three-pack word comparison (§1, "T3 words"), D10. Nothing in
the JSON or the reader changed, so the file stays 0.1.1. **How.** `H3_POLICIES=... WAN22_POLICIES=... python3
policy/test_policy.py` from the three checkouts above. **Owed.** §4 and §9; none of it is in `policy/`.
