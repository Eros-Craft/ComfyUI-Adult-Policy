# Testing this repository: ComfyUI Desktop, Comfy Cloud and CI

This repository holds two things, and both are tested here: `policy/`, the one adult policy every ErosCraft workflow
reads, and the Qwen 2.1 node pack exported from its private workflow repository. The ladder is the workspace's
(T0 offline, T1 Desktop, T2 Comfy Cloud, T3 package, T4 Verda), cut down to what a policy and a node pack can owe.

**Every test is safe for work, everywhere.** No explicit content in any test, prompt, fixture, issue or report, and no
image, dataset or picture of a minor, ever. The only thing these tests type into ComfyUI is the two gate toggles.

## What runs where

| Stage | Where | When | Costs | What it proves |
|---|---|---|---|---|
| T0 policy | `tests.yml`, job `policy` | every pull request, `main`, nightly | nothing | `policy/test_policy.py` on Linux, macOS and Windows, Python 3.10, 3.12 and 3.14, warnings as errors |
| T0 rules | `tests.yml`, job `registry` | the same | nothing | `house_rules.py` (what the pack export refuses: the other brand's name, an em dash, a token, a /Users/ path; the Registry's ruff rules) and `comfy node validate` |
| T1 on CI | `tests.yml`, job `comfyui` | the same | nothing | the pack in the newest ComfyUI release on the CPU, on all three systems (below) |
| T1 canary | `tests.yml`, ComfyUI `master` | nightly and by hand | nothing | the same against ComfyUI's master, to see a break before a release carries it |
| T1 Desktop | the Mac, `desktop-check.sh` | a change to the pack or `policy/`, and each release | nothing | the same smoke in the ErosCraft dev install, launched the way Comfy Desktop launches it |
| T2 check | `comfy-cloud.yml`, job `check` | Mondays, by hand, a change to the checks | nothing | the Registry's verdict on the newest version; Cloud's ComfyUI version; whether Cloud has the pack's nodes |
| T2 parity | `comfy-cloud.yml`, job `parity` | the same | nothing | the smoke at exactly the ComfyUI version Comfy Cloud runs |
| T2 render, T4 | each workflow repository | per release | credits, dollars | a stop through a real run and an image out, on a deployment carrying the pack and on Verda |

Nothing in this repository queues a Cloud job or spends a credit. Comfy Cloud runs only its own node library (this
pack's classes are not in it: `cloud_check.py` reports that as "Cloud cannot", never as a failure) and is
safe-for-work only, so the policy is rendered where the pack is installed: a workflow's deployment, then Verda.

## The smoke: one script for CI, Desktop and Cloud parity

`comfyui_smoke.py` starts a scratch ComfyUI (`--cpu`, loopback, its own `--base-directory`, so the install it borrows
never changes), installs the pack from the `node.zip` the Registry would ship (`comfy node pack`: the git-tracked files
minus `.comfyignore`), and checks, each as one report row:

- the zip carries the pack and none of `.github/` or `policy/`;
- the server starts, the pack imports, every `NODE_CLASS_MAPPINGS` class is in `/object_info`, and the picker's
  script is in `/extensions`;
- **the gates through the real `/prompt`:** with either toggle off, ComfyUI refuses the prompt with exactly the
  sentence `policy/eroscraft-adult-policy.json` holds for that position, and nothing queues; with both on, the same
  prompt runs to success. So a change to the policy's words that the pack does not follow fails here, inside ComfyUI,
  not only in a unit test.

No model is loaded and nothing renders: the gates refuse at validation, which is the point of them.

## On the Mac: the Desktop check

    bash .github/testing/desktop-check.sh                                 # free, about two minutes
    bash .github/testing/desktop-check.sh --server http://127.0.0.1:8000  # a running Desktop that has the pack

It borrows the workspace's dev install (`~/ComfyUI-Installs/ErosCraft-Dev`, built by `base/desktop.sh`; set
`COMFYUI_DIR` and `COMFYUI_PYTHON` for another), runs `policy/test_policy.py` with that install's own Python, runs
`comfy node validate` and `comfy node pack`, then the smoke on port 8296 with Comfy Desktop's two launch flags. It never
stops early, so one run gives the whole list, and it writes its report to `.github/testing/reports/` (ignored by git).
Quote the Markdown under "How you checked it" in the pull request.

**By eye in Desktop, once per release** (what no script here checks): open Comfy Desktop on the dev install, add each
of the five nodes from the node library and read their names (🔞 ErosCraft policy, gate, rewrite check, output check;
➕ Civitai Red LoRA); confirm both toggles show "off"; press the picker's button and see its panel open. Type nothing
into the picker's search.

## The report

Every script writes the ErosCraft test-report format the workflow repositories use (`format: 1`, one row per case:
`workflow, stage, case, expected, observed, ok, status, reason`, under `venue, workflow, version, commit, when,
where, credits, cost_usd`), so the workspace's `reports.py summary` reads it. A run passes when every row is green
or a "CI cannot"/"Cloud cannot" row with its reason.

## Which change owes which run

| The change | It owes |
|---|---|
| `policy/` (words, rules, a workflow's entry) | T0 and T1 on CI, the Desktop check, then each adopting workflow re-derives and runs its own sweeps |
| the pack's code (only ever through an export) | everything above; the export itself runs from the private repository after its own sweeps |
| these tests or the workflows | the pull request's own CI; `comfy-cloud.yml` runs on it too |

## Settings, once (names only; a value never goes in a file)

1. **Secret** `COMFY_API_KEY` (Settings, Secrets and variables, Actions, New repository secret): the key from
   platform.comfy.org, for `comfy-cloud.yml`'s read-only Cloud rows. Without it those rows say "skipped".
2. **Required check** `tests` on `main` (Settings, Rules, Rulesets): the one job that passes only when every test job
   passed. `comfy-cloud` is never required: it answers for the Registry and Cloud, which a pull request cannot fix.
3. **Notifications**: a red nightly `tests` (a new ComfyUI release or master broke the pack) or a red Monday
   `comfy-cloud` (the Registry flagged a version, or Cloud moved its ComfyUI) emails the repository's watchers.

## Where these files live, and why

Everything here is under `.github/`, because the pack export (`eroscraft/_build/publish_pack.py`) removes every
public file outside `.github/`, `policy/` and `.comfyignore`, and `.comfyignore` keeps `.github/` out of the
Registry's `node.zip`. The export does rewrite a few named `.github/` files (the publish action, `dependabot.yml`,
`SECURITY.md`, `CONTRIBUTING.md`, the issue and pull request templates, `CODEOWNERS`); nothing in this folder or in
`tests.yml`, `comfy-cloud.yml` and `actions/comfyui-smoke/` is among them.
