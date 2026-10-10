# HANDOFF: the ErosCraft adult policy (policy/ in Eros-Craft/ComfyUI-Adult-Policy)

The session record for this repository's package: `policy/`, the one adult policy every ErosCraft workflow reads,
and the place it is proven. It lives in `policy/` because the pack export (`eroscraft/_build/publish_pack.py` in the
private workspace) removes every public file outside `.github/`, `policy/` and `.comfyignore`. Written for a reader
who was not there. The top four sections are replaced as the state changes; the entries under "Sessions" are
appended and never rewritten.

## 1. Where the package stands, gate by gate (2026-10-06 06:30 UTC, main at `f6f8393`, policy 0.1.3 after #19)

What T0 to T4 and "ready to sell" mean for a policy is decided in §5, D1. Short form: the policy owes its own T0,
T1 and T3 here, and reaches buyers only inside a workflow's zip, so its T2 and T4 are its adopters' render sweep and
Verda release check.

| Gate | State | Evidence |
|---|---|---|
| T0 policy test | green | `python3 policy/test_policy.py`, 16 passed, warnings as errors; on CI in `tests.yml` on Linux, macOS and Windows, Python 3.10, 3.12 and 3.14, and in `checks.yml` (PR #10 merged with 18 of 18 checks green) |
| T0 house rules | green | `checks.yml` and `.github/testing/house_rules.py`: no other brand's name, no em dash, no token, no local home path, Registry ruff rules S102, S307, E702 |
| T1 on CI | green | `comfyui_smoke.py`, 9 of 9 rows on Linux, macOS and Windows with ComfyUI v0.38.2 and with master: the pack from a Registry-shaped zip, all 5 nodes registered, both gates refuse through the real `/prompt` with the exact sentence the policy file holds, a changed sentence caught at its gate position |
| T1 Desktop | carried by Qwen 2.1's T1 | D7: CI's macOS smoke (green, above) plus Qwen 2.1's T1 Desktop sweep, which runs the derived policy on the Mac's dev install (that sweep is the Qwen 2.1 project's; port 8296 went to it). `desktop-check.sh` stays for a later change to the pack |
| T2 Cloud check | green, with "Cloud cannot" and "skipped" rows | `comfy-cloud.yml`: the parity smoke at Comfy Cloud's own ComfyUI v0.38.2 passes; Cloud has no node library entry for the pack ("Cloud cannot": Cloud runs only its own library, and is safe for work only); the rows that read Cloud say "skipped" until the `COMFY_API_KEY` secret is set (§6) |
| T2 render | inherited, not run | a stop through a real run and an image out, on a workflow's Comfy deployment carrying the pack: owed by each adopter (Qwen 2.1's sweep is owed in its own HANDOFF §6) |
| T3 copies | Wan 2.2 and MiniMax H3 current; Qwen 2.1 in review; three workflows carry none | Read 2026-10-06 with `cmp` of the JSON and `diff` of `adult_policy.py` below its generated header: Wan 2.2 (workspace main `02d4b56`, ErosCraft #64) and MiniMax H3 (main `9558386`) are byte-equal to 0.1.3, and both ask `famous_person_in_image` (`FAMOUS_IMAGE` in each `policies.py`). Qwen 2.1 main (`717ba72`, V1.4.0) still carries 0.1.0; its PR #54, stacked on its gate PR #51, carries 0.1.3 byte-equal and asks the new fact, under review. Krea 2 Image Creator, the Character Creator and Anima carry no copy (this week's adoption check, relayed 2026-10-06); Anima takes no photo or clip input (its `policies.py:246`, `input_facts=()`, held by its `suite.py:192`), so request 5 does not reach it, but it still reads its words from its own engine rather than the file. Requests in §9 |
| T3 export, staged | green, not run | `policy/` plus Qwen 2.1's 1.4.0 `qwen21_adult_policy/` laid side by side: `test_policy.py` 14 passed at 0.1.1; the export's refusal scan and ruff S102, S307, E702 clean over the 1.4.0 pack. ErosCraft #45 and #46 make an export keep `policy/` and rewrite `.github/` to exactly what is here (`checks.yml`, `publish_action.yml`, `dependabot.yml` and all seven community files compared equal this session) |
| T3 words, every compared pack | green | `test_policy.py` with no skip, 2026-10-06: `WAN22_POLICIES` at the Wan 2.2 pack on workspace main `02d4b56`, `H3_POLICIES` at MiniMax H3's main `9558386`, and the 1.1.4 pack in this repository: 16 passed, every question and stop sentence each pack shows equal to the file resolved for its entry (the 1.1.4 pack's old unclear sentence is allowed by `CHANGED_IN`, D12). Wan 2.2's famous-face stop is tested only with a fake judge in its own suite (its project's note) |
| T3 version | green for the policy; the pack here is stale | the file and `POLICY.md` both say 0.1.3, and `test_document_names_the_file_version` (#9) holds them together. The exported pack here is 1.1.4; its source is 1.4.0; the export is the Registry publish (§4) |
| T3 read as a buyer | corrected in this PR | `policy/README.md` had four stale statements (§2); `POLICY.md` read clean |
| T4 Verda | inherited, not run | the first adopter's release check, Qwen 2.1 V1.4.0 (`docs/verda-release.md` in that repository): not run |

**Live defect first:** the Registry's default install of the pack is 1.1.3, which is Active and the node's
`latest_version`, and 1.1.4 (Flagged) still installs too; both read a hedged age answer as a pass. The fix, PR #12,
waits for the owner (§4, §6). **Ready to sell (D1): not yet.** What is left is Qwen 2.1's T1 Desktop sweep, T2 render
and T4 (not run), its 0.1.3 adoption (#54 after #51), and the owner's merges of ErosCraft #45 and #46. Nothing in
`policy/` itself is red.

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
- **The other workflows' adoption**: Wan 2.2 and MiniMax H3 carry 0.1.3 and ask the famous-face fact; Qwen 2.1's
  0.1.3 is in review (#54); Krea 2, the Character Creator and Anima carry no copy. Each is its own project's change
  (`README.md`, "The order"); the finding went to their coordinators once (§9).
- **A live safety defect in a public version (urgent).** Read again 2026-10-06: the Registry lists 1.1.4 as
  `NodeVersionStatusFlagged` and 1.1.3 as `NodeVersionStatusActive`, and the node's `latest_version` is 1.1.3, so a
  plain install gets 1.1.3 (`cdn.comfy.org/.../1.1.3/node.zip` answers 200, 29,086 bytes); 1.1.3's reader is older
  than 1.1.4's and no stricter. As read on 2026-10-03, the published pack 1.1.4 (and 1.1.3) still installs:
  `api.comfy.org/nodes/comfyui-qwen21-adult-policy/install?version=1.1.4` answers with a `downloadUrl` although the
  version reads `NodeVersionStatusFlagged`, and that `cdn.comfy.org/.../1.1.4/node.zip` answers 200, 29,207 bytes
  (both read this session). Qwen 2.1 measured at 14:20 UTC that it loads in ComfyUI 0.38.2 and that its answer reader
  fails open: "minor: no idea", "minor: no (but unsure)" and "minor: no" followed by "minor: yes" all read as a clear
  no. The fix is 1.1.5, the strict reader (policy repository PR #12, Qwen 2.1's: #4's commits placed on today's main,
  keeping `policy/` and `.comfyignore`, not an export, since the source is 1.4.0), which waits for the owner
  (§6, first row). An earlier line here said a flagged version cannot be installed; that was wrong.
- **Registry**: the node's `repository` still reads the old name until the next publish (Qwen 2.1's, D3).

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

**D4. PR #4 (pack 1.1.5, the bare-no reader) is superseded by PR #12** (Qwen 2.1's, D3: #4's commits
cherry-picked onto today's main so `policy/` stays; an export could not make 1.1.5, because the source is 1.4.0 and
the export tool refuses a version that differs from the workflow's). #4 closes when #12 merges. 1.4.0 goes public
by export after Qwen 2.1's Verda release check.

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
not before, and not while the age-check finding (§8) is open: until a run on a buyer's machine has shown the stops,
"draft" is the honest word.

**D11. An additive age margin, `age_margin` at 25, may ship without the owner once measured** (the "Age check safety
margin" thread, 2026-10-03; its full note is `notes/age-margin.md` in the project's shared files). A second image-only
fact, asked in the same call as `anyone_under_18`, where either "yes" stops; the text fact `minor` gets none. The
file goes to 0.2.0, and merges only after an adults-only measurement passes. Its grounds: `POLICY.md` lets a
check be added and refuses only weakening, rule 3 (`eroscraft/CLAUDE.md:30-34`, `:42-44`) protects the rules from
removal or moving, and `adult_policy.py`'s `validate` refuses only weakening. Nothing is removed or moved, and the
measured `anyone_under_18` wording stays, so every adopter's words still match. Each adopter's engine must ask the
new fact before it has any effect. Cost to note for that measurement: the margin also stops finished images of adults
aged 18 to 24 whose request the text check passed, so it needs its false-stop rate on adults 18 to 24 and 25 to 30
reported, not only its catch rate.

**D12. The request's unclear stop says reword, not run again** (the coordinator's decision, 2026-10-03, on Qwen 2.1's
release owner's finding; policy 0.1.2). The checker decodes greedily (Qwen 2.1's pack, `nodes.py:96`,
`do_sample=False`), so the same words and photos give the same unclear answer on every run, which Qwen 2.1's T2
reproduced. The sentence now says so and asks the person to reword the request with who is in it and an adult age,
or to use a different photo; it still says plainly that the stop is not a finding about the request. The two output
sentences keep "run it again", because a new run draws a new picture. `test_policy.py` gains `CHANGED_IN`: a pack
that copied its words before a version shows the old wording of exactly the names that version changed, and every
other word must still be equal; `test_unclear_request_says_reword_not_rerun` holds the new wording. The age margin
(D11) rebases onto this.

**D13. A famous face in an input photo is asked, and ships unmeasured** (the coordinator's decision, 2026-10-03, on
Qwen 2.1's rule 3 audit; policy 0.1.3). Rule 2 asked only the words, so a recognisable famous person in an uploaded
photo with no name typed was never checked, and the uploader's ✅ Consent was the only guard. The file adds the image
fact `famous_person_in_image`, asked of every photo or clip the person adds, in the same call as `anyone_under_18`;
"yes" stops, and the stop sentence names nobody. Rule 2 is now checked at `inputs` too, and the reader refuses a copy
that drops it, a rule checked on photos that asks no image fact, or the stop's sentence. It is not asked of the output,
so the reader asks an `output` sentence only of image facts whose rule checks the output. Grounds: strictly tighter,
which `POLICY.md` allows ("may add checks", lines 8 and 9) and rule 3 does not forbid. It ships marked "unmeasured"
(`POLICY.md`, "Changing this policy"), because measuring it needs photos of real famous people, which no ErosCraft test
makes or uses. Cost to watch: its false-stop rate on ordinary people's photos is unknown, and a false stop blocks a
consented real-photo edit (D9). Rule 2's own words, "No famous real person named", are the owner's and are unchanged;
the rule's description in `POLICY.md` now names photos. It stops nothing in a pack until that pack's engine asks it
(§9, request 5). `test_a_famous_face_in_a_photo_is_asked` holds it.

**D14. Frame readers log the judge's raw answer beside the parsed verdict** (the coordinator's decision, 2026-10-10,
under the owner-away mandate). Wan 2.2's render thread reported, through the weekly adoption check because Qwen 2.1's
orchestrator was offline, that the under-18 check on output frames stopped a video of a fictional 18-year-old man, on
an H100 and earlier on an RTX PRO 6000 (its logs: `eroscraft-video-creator-wan-2.2/t2-phase2-2026-10-10/h100/logs/`
in the workspace). The logs held the verdict but not what the judge said, so the stop could not be told apart from a
parse failure. The recommendation to every pack owner, Wan 2.2 first: log the judge's answer text next to the parsed
verdict, as text only and never image data. It changes no outcome and nothing in the policy file; it makes a false
stop diagnosable.

**D15. No special handling for 18 and 19 year olds on frames** (the coordinator's decision, 2026-10-10, on the same
report). The age check stays fail-closed, and a young-looking adult being stopped is the cost `POLICY.md` already
accepts ("asked and failing closed", not measured). Any change to the margin belongs to the age margin's pending
approval in §6 (D11), not to a carve-out for an age band.

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
the JSON's messages and a refusal in each pack's engine, made in one PR here and then re-derived by every adopter. **Resolved** the same day: the storefront orchestrator confirmed rule 3,
withdrew the claim (the hold was its own decision, not the owner's), and matches and links `POLICY.md` instead.

**D6. A policy README edit needs no version bump** (`POLICY.md`, "Changing this policy", bumps on a change to the
policy): only the JSON and the reader are derived into packs, so a README edit leaves every adopter's copy equal.

## 6. Pending approvals (stopped at a prompt or a permission check; not routed around)

| What | Why it waits | Who |
|---|---|---|
| **First, a live safety defect:** merge and publish policy repository PR #12 (pack 1.1.5, the strict answer reader). Published 1.1.4 and 1.1.3 still install from the Registry and its CDN and read "minor: no idea" as a clear no (§4) | Qwen 2.1's permission check refused it as creating a public surface | the owner |
| The age margin (0.2.0, D11): the owner decides (a) the render venue for the adults-only measurement, (b) the exemptions to the render floor of 25 (ages 18 to 24 must render) and to the SFW screen (it refuses the pinned age question), and (c) the budget, about 627 credits by Anima's estimate; or chooses to ship the margin marked "unmeasured". The edit to `policy/eroscraft-adult-policy.json` has no branch or PR yet; every value and test is in `notes/age-margin.md`. Qwen 2.1 PR #51 (in progress) prefills the checker's answer label, so once it merges any measurement is asked again with it | Anima parked the measurement on four blockers (2026-10-03, relayed by the coordinator): no allowed render venue (Anima reports Comfy deployments run on RunPod Serverless, which `eroscraft/CLAUDE.md` rule 2 forbids, and the Mac never renders, root `CLAUDE.md` §0.5), the SFW screen, the render floor and the cost. The edit itself was also refused by the "Age check safety margin" thread's permission check as modifying a shared resource | the owner |
| ErosCraft #45, then #46 (publish_pack keeps `policy/`, targets the new name, writes the Checks and community files) | the session permission check refuses an unreviewed merge | the owner |
| `python3 tools/github_settings.py --repo Eros-Craft/ComfyUI-Adult-Policy` on the Mac (labels, rulesets, security settings) | the cloud proxy refuses repository-settings writes | the owner |
| The Claude GitHub App on this repository | an installation is the owner's | the owner |
| Whether to hold explicit real-photo edits until "Consent in person" ships (stricter than rule 3; the design names UK s.66I and asks for a lawyer's read before any sale) | rule 3 and `POLICY.md` move only on the owner's own words (D9) | the owner, with a legal review |
| The `COMFY_API_KEY` repository secret, for `comfy-cloud.yml`'s Cloud rows | a secret value is the owner's | the owner |

## 7. Session roster (this project, 2026-10-03 14:15 UTC; this row refreshed 2026-10-06)

| Session | Owns | State | Next |
|---|---|---|---|
| Coordinator (project chat) | the roster, answers every question, merges | active | relays approvals |
| Policy package readiness and HANDOFF (this) | `policy/HANDOFF.md`, `policy/README.md` accuracy, the gate definitions, reviews of `policy/` PRs | working (owner: "Keep going!", 2026-10-06) | §1 kept current; the adopters' re-derives |
| Desktop and Cloud testing setup | `.github/testing/`, `tests.yml`, `comfy-cloud.yml`, `.github/actions/` | PRs #10 and #11 merged | the Cloud rows once `COMFY_API_KEY` is set |
| GitHub best-practice repo setup | the `.github/` community files through ErosCraft #46, `tools/github_settings.py` | waiting on the owner | none until #46 merges |
| Draft the shared adult policy | policy PRs #6, #7, ErosCraft #45 | done, resolved | none |
| Wire the policy into Qwen 2.1 | Qwen 2.1 #47, #48, #49 | done, resolved | none |
| Rename the policy repo (the Mac) | the rename | done, resolved | none |
| Age check safety margin | the open finding below (§8) and its change, D11 | designed; the measurement is parked on four owner decisions (§6) | the owner's answer, then the measurement, asked again once Qwen 2.1 #51 merges; until it lands nobody else edits the JSON's or `POLICY.md`'s age question |
| Weekly policy adoption check (a routine) | reads each workflow's adoption state weekly | review ready | next weekly run |

## 9. Requests to other projects (sent through the coordinator; nothing edited in their repositories)

1. **To Qwen 2.1: re-derive the policy to 0.1.3.** `python3 _build/derive.py` with this repository beside it, then
   the zips; its `derive.yml` turns red the next night until then. 0.1.1 changed only MiniMax H3's entry; 0.1.2
   rewords the request's unclear stop (D12), the one sentence its buyers will read differently; 0.1.3 adds a fact
   (D13) and changes no word. Its pack, with the new file and reader copied in, loads and passes `test_policy.py`
   (measured), and fails on any other word.
2. **To Qwen 2.1: assert the policy's version in its suite.** `policy/README.md` step 5 asks the suite to check
   `SHARED.version` against the version the handbook names; `grep` finds no such assertion in its `suite.py`.
3. **To MiniMax H3:** done. Its main (`9558386`) derives the two files at 0.1.3 and reads them.
4. **To Wan 2.2 and MiniMax H3:** done for Wan 2.2 (ErosCraft #64, 0.1.3). Was: Wan 2.2's pack carries its own literal of the old unclear sentence; it moves to the
   new one when it adopts the file. MiniMax H3's entry rewords its own unclear stops and still says "run it again"
   for a request, which D12 found does not help; its project decides whether to follow (its entry, its words).
5. **To every adopter that takes photos or clips (Qwen 2.1 first): ask `famous_person_in_image`** (D13) at `inputs`, in
   the same call as `anyone_under_18`, and show `messages.request.famous_person_in_image` on "yes" (an unclear answer
   shows the unclear stop, as for every fact); not at `output`. `policy/README.md` step 4 has the line. State
   2026-10-06: Wan 2.2 and MiniMax H3 ask it; Qwen 2.1 in #54; Anima takes no photo or clip, so it does not apply.
6. **To Krea 2 Image Creator, the Character Creator and Anima: derive the policy at 0.1.3**: this week's adoption
   check found no copy of the file in any of the three. Delivered to Anima's coordinator on 2026-10-06.
   **Not delivered to Qwen 2.1 or Krea 2**: the Qwen 2.1 coordinator session (which relays to Krea 2) was inactive,
   and the project coordinator's retry was refused the same way, so this entry is the record for them to pick up
   when it resumes, with no further retries (the weekly adoption check shows when it lands). What it carries: Qwen
   2.1 main (`717ba72`) still on 0.1.0, with its #54 (on #51) carrying 0.1.3 and pending review; Krea 2 Image
   Creator and the Character Creator without the file; and the Registry defect, where a plain install gets pack
   1.1.3 (Active, the node's `latest_version`) with the fail-open reader, fixed by PR #12 (§4, §6).

## 8. Known external defects (recorded, not patched here)

- **The base**: ComfyUI Base 3.6.0 `lib/85-launch.sh` lines 125 and 143 pass `--enable-cors-header`, which lets any
  web origin call the local ComfyUI API (found by the storefront orchestrator; the request is with the base's
  maintainers; nothing here edits the base). Nothing in `policy/` tells a buyer how to launch ComfyUI, so no caution
  belongs here; the testing thread's smoke binds loopback only.
- **The Registry**: 1.1.4 is flagged and still installs; 1.1.3 is Active and the default install; both have the fail-open reader (§4).
- **The workspace's `base/desktop.sh --stand-ins` truncates real model files** (found by the storefront orchestrator,
  whose project owns the fix): lines 112 to 118 open every path its stand-in manifest lists with `"wb"`, so a real
  file installed later at a listed path is zeroed (the Character Creator's 8.9 GB Qwen3-VL encoder was). This
  repository is not exposed: `.github/testing/desktop-check.sh` never calls `desktop.sh` (it only names
  `desktop.sh --server` as how to build the dev install when its Python is missing), never passes `--stand-ins`, and
  the smoke writes only under its own scratch `--base-directory` (`comfyui_smoke.py:156`), never into a model path.
- **The age check reads apparent age within a wide band** (open, 2026-10-03, owned by the "Age check safety margin"
  thread). Anima's canary with the shared Qwen3-VL age question, under an "under 30?" proxy, missed 3 of 5 adults
  aged 20 to 24. The proposal is a "Challenge 25" margin, measured on adults only first (no minors data, ever). That
  thread decided the tightening is allowed (D11) and designed it; the adults-only measurement is with Qwen 2.1 and
  Anima's canary. `POLICY.md` already calls the age check "asked and failing closed", not measured, for the 8B. Side
  finding from that thread: the current age question's line "(Any adult, including a young-looking adult, is NOT
  under 18.)" nudges the checker toward passing young faces; the margin is designed to sit beside it rather than
  reword it, so the measured wording every pack shows stays equal.

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

### 3. 0.1.2 and 0.1.3, then the adoption state (2026-10-03 to 2026-10-06, no machine)

**Proven.** #17 (0.1.2, D12), #18 (the age margin's four owner decisions), #19 (0.1.3, D13), each merged with 16 of
16 checks green. On 2026-10-06: Wan 2.2 and MiniMax H3 byte-equal to 0.1.3 and passing the word comparison, Qwen 2.1's
#54 byte-equal, and the Registry's default install being 1.1.3 (§1, §4). ErosCraft #45 and #46 are still open, with
no check runs, and `publish_pack.py` is unchanged on workspace main since their base `fb388ce`, so they still apply
as reviewed. **How.** `git archive` of each adopter's main into a scratch folder, `cmp` and `diff`, then
`WAN22_POLICIES=... H3_POLICIES=... python3 policy/test_policy.py`; the Registry's own API
(`api.comfy.org/nodes/comfyui-qwen21-adult-policy/versions`) and a GET of the CDN zip. **Owed.** §4, §6.
