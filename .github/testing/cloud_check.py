#!/usr/bin/env python3
"""The Comfy platform's side of this pack, read only and free: the Registry, and what Comfy Cloud can run of it.

    python3 .github/testing/cloud_check.py [--json report.json] [--github-output]

Rows, in the ErosCraft test-report format (the same one comfyui_smoke.py writes):

    registry         the newest version on the Comfy Registry (where Manager, Desktop and Cloud install from) is
                     Active, and it is the version pyproject.toml names, or older while a release is under way
    cloud-comfyui    the ComfyUI version Comfy Cloud runs, from `comfy --where cloud system-stats`; the parity job
                     runs the CPU smoke at exactly that version
    cloud-nodes      whether the pack's node classes are in Cloud's node library (`comfy --where cloud nodes ls`).
                     Today they are not, and cannot be: Cloud runs only its own library, and is safe-for-work only.
                     That row is "Cloud cannot" with its reason, never a failure; renders of the policy happen in each
                     workflow repository's comfy-cloud.yml (a deployment carrying the pack) and on Verda.

The Cloud rows need comfy-cli on PATH and the Comfy API key in COMFY_CLOUD_API_KEY or COMFY_API_KEY; without them
they are "skipped" with the reason. Nothing here queues a job or spends a credit. With --github-output the Cloud
ComfyUI version is written to $GITHUB_OUTPUT as `comfyui=<tag>` for the parity job.
"""
import argparse
import datetime
import json
import os
import pathlib
import shutil
import subprocess
import sys
import urllib.request

sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from comfyui_smoke import Report, pack_facts, pack_version  # noqa: E402

REGISTRY = "https://api.comfy.org"
ENV = dict(os.environ, DO_NOT_TRACK="1", COMFY_NO_TELEMETRY="1", COMFY_NO_WATCH="1")
if not ENV.get("COMFY_CLOUD_API_KEY") and ENV.get("COMFY_API_KEY"):
    ENV["COMFY_CLOUD_API_KEY"] = ENV["COMFY_API_KEY"]
VERDICT = {
    "NodeVersionStatusActive": (True, "Active: Manager, Desktop and Cloud can install it"),
    "NodeVersionStatusPending": (True, "Pending: waiting on the Registry's security scan"),
    "NodeVersionStatusFlagged": (False, "Flagged by the Registry's scan: nothing installs it until a manual review "
                                        "(an issue on Comfy-Org/registry-backend)"),
    "NodeVersionStatusBanned": (False, "Banned by the Registry"),
    "NodeVersionStatusDeleted": (False, "Deleted from the Registry: publish a new version"),
}
PENDING_STALE = datetime.timedelta(days=1)


def _key(v):
    return tuple(int(x) if x.isdigit() else 0 for x in v.split("."))


def registry(rep, name, version):
    try:
        with urllib.request.urlopen(f"{REGISTRY}/nodes/{name}/versions", timeout=30) as r:
            versions = json.loads(r.read() or b"[]")
    except Exception as e:                  # the Registry being down is a failed row, not a crash
        rep.add("registry", "the newest version is Active", f"could not ask the Registry: {e}", False)
        return
    if not versions:
        rep.add("registry", "the newest version is Active", "no version on the Registry", False)
        return
    newest = max(versions, key=lambda v: v.get("createdAt", ""))
    ok, says = VERDICT.get(newest.get("status"), (False, f"unknown status {newest.get('status')}"))
    if newest.get("status") == "NodeVersionStatusPending":
        made = datetime.datetime.fromisoformat(newest["createdAt"].replace("Z", "+00:00"))
        if datetime.datetime.now(datetime.timezone.utc) - made > PENDING_STALE:
            ok, says = False, "Pending for over a day: the scan errored (Comfy-Org/registry-backend#211)"
    ahead = _key(newest.get("version", "0")) > _key(version)
    if ahead:
        ok, says = False, says + f"; the Registry's {newest['version']} is ahead of pyproject's {version}"
    rep.add("registry", f"{name} {version} or older on the Registry, newest Active",
            f"{newest.get('version')}: {says}", ok)


def comfy(*args):
    r = subprocess.run(["comfy", "--json", "--where", "cloud", *args], capture_output=True, text=True, env=ENV,
                       timeout=300)
    try:
        env = json.loads(r.stdout)
    except ValueError:
        return None, (r.stderr or r.stdout).strip()[:300]
    return (env.get("data"), None) if env.get("ok") else (None, str((env.get("error") or {}).get("message")))


def cloud(rep, classes):
    why = None
    if not shutil.which("comfy"):
        why = "comfy-cli is not on PATH (uv tool install comfy-cli)"
    elif not ENV.get("COMFY_CLOUD_API_KEY"):
        why = "no Comfy API key: set the COMFY_API_KEY secret (Settings, Secrets and variables, Actions)"
    if why:
        rep.skip("cloud-comfyui", "Comfy Cloud's ComfyUI version", why)
        rep.skip("cloud-nodes", "the pack's classes on Cloud", why)
        return None
    stats, err = comfy("system-stats")
    tag = ((stats or {}).get("system") or {}).get("comfyui_version")
    rep.add("cloud-comfyui", "Comfy Cloud answers system-stats", f"ComfyUI {tag}" if tag else f"no answer: {err}",
            bool(tag))
    listing, err = comfy("nodes", "ls")
    if listing is None:
        rep.add("cloud-nodes", "Cloud's node library lists", f"no answer: {err}", False)
        return tag
    have = {row.get("name") for row in listing.get("rows", [])}
    on = [c for c in classes if c in have]
    if len(on) == len(classes):
        rep.add("cloud-nodes", "the pack's classes on Cloud", f"all {len(classes)} on Cloud", True)
    else:
        rep.rows.append({"workflow": rep.workflow, "stage": "T2", "case": "cloud-nodes",
                         "expected": "the pack's classes on Cloud", "ok": True, "status": "Cloud cannot",
                         "observed": f"{len(on)} of {len(classes)} on Cloud ({len(have)} classes there)",
                         "reason": "Cloud runs only its own node library and is safe-for-work only, so the policy is "
                                   "rendered on a deployment carrying the pack (each workflow's comfy-cloud.yml) "
                                   "and on Verda"})
        print(f"  cannot cloud-nodes: {len(on)} of {len(classes)} on Cloud")
    return tag


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--json", help="write the report here")
    p.add_argument("--github-output", action="store_true", help="write comfyui=<Cloud's tag> to $GITHUB_OUTPUT")
    p.add_argument("--advisory", action="append", default=[], metavar="CASE",
                   help="report this case but leave it out of the exit code (a pull request cannot fix the Registry)")
    a = p.parse_args()
    facts = pack_facts()
    rep = Report("comfy-cloud", facts["workflow"] or facts["name"])
    registry(rep, facts["name"], pack_version())
    tag = cloud(rep, facts["classes"])
    for row in rep.rows:
        row["stage"] = "T2"
    md = rep.markdown("Comfy Registry and Comfy Cloud, read only", tag or "?").replace("ComfyUI smoke", "Comfy check")
    print(md)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write(md)
    if a.github_output and os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as f:
            f.write(f"comfyui={tag or ''}\n")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(rep.document("comfy-cloud", tag or "?"), indent=1),
                                        encoding="utf-8")
    blocking = [r for r in rep.rows if not r["ok"] and r["case"] not in a.advisory]
    for r in rep.rows:
        if not r["ok"] and r["case"] in a.advisory:
            print(f"::warning title={r['case']}::{r['observed']}")
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
