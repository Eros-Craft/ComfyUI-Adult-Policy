#!/usr/bin/env python3
"""The pack inside a real ComfyUI, on the CPU: the one smoke CI, the Mac's Desktop install and the Cloud parity run share.

    python3 .github/testing/comfyui_smoke.py --comfyui <ComfyUI dir> --python <its venv python>   # start a scratch server
    python3 .github/testing/comfyui_smoke.py --server http://127.0.0.1:8000                        # a server already up

Standard library only. With `--comfyui` it starts that ComfyUI on 127.0.0.1 with `--cpu` and a throwaway
`--base-directory`, so nothing in the install it borrows changes, and installs the pack there the way the Comfy
Registry ships it: the git-tracked files minus `.comfyignore` (or the `node.zip` from `comfy node pack`, given
`--zip`). With `--server` it checks a server someone else started, which must already have the pack.

The cases, each one row of the report:

    zip        the Registry's node.zip carries the pack and none of .github/ or policy/
    server     ComfyUI answers /system_stats (its version goes in the report)
    import     the pack imported: no "IMPORT FAILED" for it in the log (scratch server only)
    nodes      every class in NODE_CLASS_MAPPINGS is in /object_info
    web        the pack's WEB_DIRECTORY scripts are in /extensions
    gate-*     with either gate off, POST /prompt is refused with exactly the sentence policy/ holds, and nothing queues
    gates-on   with both gates on the same prompt queues and runs to success (nothing renders: no model is loaded)

Nothing here renders, loads a model or reaches the network beyond the server it names, so it is free on every venue.
Every input is safe for work: the only things typed are two booleans.

The report is the ErosCraft test-report format (format 1, one row per case: workflow, stage, case, expected,
observed, ok, status, reason), written with `--json` and summarised as Markdown on stdout (and in
$GITHUB_STEP_SUMMARY when set). The exit code is 0 only when every row is green.
"""
import argparse
import ast
import datetime
import fnmatch
import json
import os
import pathlib
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
import uuid
import zipfile

sys.dont_write_bytecode = True
REPO = pathlib.Path(__file__).resolve().parents[2]
POLICY_DIR = REPO / "policy"
# What Comfy Desktop adds when it launches a git install (the workspace's base/desktop.sh, measured on Desktop 1.1.3).
DESKTOP_FLAGS = ["--feature-flag", "show_signin_button=true", "--feature-flag", "supports_terminal=false"]
NEVER_SHIPPED = (".github/", "policy/")


# --------------------------------------------------------------------------- the pack, read without importing it
def pack_facts():
    """The pack's node classes, its product-gate class, its web directory and its workflow, read from source."""
    tree = ast.parse((REPO / "__init__.py").read_text(encoding="utf-8"))
    web = next((n.value.value for n in tree.body if isinstance(n, ast.Assign)
                and any(getattr(t, "id", "") == "WEB_DIRECTORY" for t in n.targets)), None)
    classes = []
    for py in sorted(REPO.glob("*/nodes.py")):
        for n in ast.parse(py.read_text(encoding="utf-8")).body:
            if isinstance(n, ast.Assign) and any(getattr(t, "id", "") == "NODE_CLASS_MAPPINGS" for t in n.targets):
                classes += [k.value for k in n.value.keys]
    if not classes:
        raise SystemExit("no NODE_CLASS_MAPPINGS found in */nodes.py")
    gate = next((c for c in classes if c.endswith("AdultProduct")), None)
    name = _pyproject_name()
    workflow = None
    data = json.loads((POLICY_DIR / "eroscraft-adult-policy.json").read_text(encoding="utf-8"))
    for wf, entry in data.get("workflows", {}).items():
        if str(entry.get("pack", "")).lower() == name:
            workflow = wf
    return {"name": name, "classes": classes, "gate": gate, "web": web, "workflow": workflow}


def _pyproject_name():
    for line in (REPO / "pyproject.toml").read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("name") and "=" in line:
            return line.split("=", 1)[1].strip().strip('"').lower()
    raise SystemExit("pyproject.toml has no name")


def pack_version():
    for line in (REPO / "pyproject.toml").read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("version") and "=" in line:
            return line.split("=", 1)[1].strip().strip('"')
    return "?"


def gate_sentences(workflow):
    """{(consent, adult): the sentence policy/ says for that position} for every position with a gate off."""
    sys.path.insert(0, str(POLICY_DIR))
    import adult_policy                     # noqa: E402  (policy/ is not a package; the reader is standard library)
    pol = adult_policy.load(workflow)
    return {(c, a): pol.gates_off({"consent": c, "adult": a}) for c in (False, True) for a in (False, True)
            if not (c and a)}


# --------------------------------------------------------------------------- the Registry's node.zip
def comfyignore():
    path = REPO / ".comfyignore"
    if not path.exists():
        return []
    return [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip() and not ln.startswith("#")]


def _ignored(rel, patterns):
    for p in patterns:
        if p.endswith("/") and (rel.startswith(p) or ("/" + p) in ("/" + rel)):
            return True
        if fnmatch.fnmatch(rel, p) or fnmatch.fnmatch(rel.rsplit("/", 1)[-1], p):
            return True
    return False


def build_zip(out):
    """What `comfy node pack` makes: the git-tracked files minus .comfyignore."""
    files = subprocess.run(["git", "ls-files", "-z"], cwd=REPO, capture_output=True, text=True, check=True).stdout
    patterns = comfyignore()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for rel in filter(None, files.split("\0")):
            if not _ignored(rel, patterns) and (REPO / rel).is_file():
                z.write(REPO / rel, rel)
    return out


# --------------------------------------------------------------------------- talking to ComfyUI
def http(base, path, body=None, timeout=30):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(base + path, data=data, headers={"Content-Type": "application/json"} if data else {})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read() or b"null")
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            return e.code, json.loads(raw or b"null")
        except ValueError:
            return e.code, raw.decode("utf-8", "replace")


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def start_server(comfyui, python, base_dir, port, desktop, log):
    args = [python, "-s", "main.py", "--cpu", "--listen", "127.0.0.1", "--port", str(port),
            "--base-directory", str(base_dir), "--disable-auto-launch"] + (DESKTOP_FLAGS if desktop else [])
    env = dict(os.environ, DO_NOT_TRACK="1", PYTHONUNBUFFERED="1")
    env.pop("PYTHONWARNINGS", None)         # the house rule is for our code; ComfyUI's own warnings are not ours
    return subprocess.Popen(args, cwd=comfyui, stdout=log, stderr=subprocess.STDOUT, env=env)


def wait_up(base, proc, seconds):
    end = time.time() + seconds
    while time.time() < end:
        if proc is not None and proc.poll() is not None:
            return False
        try:
            if http(base, "/system_stats", timeout=5)[0] == 200:
                return True
        except OSError:
            pass
        time.sleep(1)
    return False


def gate_prompt(gate, consent, adult):
    return {"1": {"class_type": gate, "inputs": {"consent": consent, "adult": adult}},
            "2": {"class_type": "PreviewAny", "inputs": {"source": ["1", 0]}}}


def error_text(resp):
    """Every message ComfyUI put in a refused /prompt answer, flattened."""
    if not isinstance(resp, dict):
        return str(resp)
    parts = []
    err = resp.get("error") or {}
    if isinstance(err, dict):
        parts += [str(err.get("message", "")), str(err.get("details", ""))]
    for node in (resp.get("node_errors") or {}).values():
        for e in node.get("errors", []):
            parts += [str(e.get("message", "")), str(e.get("details", ""))]
    return " | ".join(p for p in parts if p)


def wait_history(base, prompt_id, seconds):
    end = time.time() + seconds
    while time.time() < end:
        code, hist = http(base, "/history/" + prompt_id)
        if code == 200 and isinstance(hist, dict) and prompt_id in hist:
            return hist[prompt_id].get("status", {})
        time.sleep(0.5)
    return None


# --------------------------------------------------------------------------- the run
class Report:
    def __init__(self, venue, workflow):
        self.venue, self.workflow, self.rows = venue, workflow, []

    def add(self, case, expected, observed, ok, reason=""):
        self.rows.append({"workflow": self.workflow, "stage": "T1", "case": case, "expected": expected,
                          "observed": observed, "ok": bool(ok), "status": "green" if ok else "failed",
                          "reason": reason})
        print(("  ok    " if ok else "  FAIL  ") + case + ("" if ok else ": " + observed), flush=True)

    def skip(self, case, expected, reason):
        self.rows.append({"workflow": self.workflow, "stage": "T1", "case": case, "expected": expected,
                          "observed": "", "ok": True, "status": "CI cannot" if self.venue == "ci" else "skipped",
                          "reason": reason})
        print("  skip  " + case + ": " + reason, flush=True)

    @property
    def passed(self):
        return all(r["ok"] for r in self.rows)

    def document(self, where, comfyui_version):
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True, text=True).stdout.strip()
        return {"format": 1, "venue": self.venue, "workflow": self.workflow, "version": pack_version(),
                "commit": commit, "when": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
                "where": where, "comfyui": comfyui_version, "credits": 0, "cost_usd": 0, "rows": self.rows}

    def markdown(self, where, comfyui_version):
        good = sum(r["ok"] for r in self.rows)
        head = "passed" if self.passed else "FAILED"
        lines = [f"### ComfyUI smoke ({self.venue}): {head}, {good} of {len(self.rows)} rows",
                 "", f"ComfyUI {comfyui_version} on {where}, pack {pack_version()}.", "",
                 "| case | status | observed |", "|---|---|---|"]
        for r in self.rows:
            obs = (r["observed"] or r["reason"]).replace("|", "\\|").replace("\n", " ")
            lines.append(f"| {r['case']} | {r['status']} | {obs[:160]} |")
        return "\n".join(lines) + "\n"


def run(a):
    facts = pack_facts()
    rep = Report(a.venue, facts["workflow"] or facts["name"])
    if not facts["gate"]:
        raise SystemExit("no *AdultProduct class: this smoke checks the gates and has nothing to check")
    if not facts["workflow"]:
        raise SystemExit(f"policy/ lists no workflow whose pack is {facts['name']}")
    sentences = gate_sentences(facts["workflow"])
    proc = log = scratch = None
    base, where, version = a.server, a.server, "?"
    try:
        if a.comfyui:
            scratch = pathlib.Path(tempfile.mkdtemp(prefix="comfyui-smoke-"))
            zpath = pathlib.Path(a.zip) if a.zip else build_zip(scratch / "node.zip")
            with zipfile.ZipFile(zpath) as z:
                names = z.namelist()
                shipped = [n for n in names if n.startswith(NEVER_SHIPPED)]
                needed = [n for n in ("__init__.py", "pyproject.toml", "LICENSE") if n not in names]
                rep.add("zip", "the pack only, with __init__.py, pyproject.toml and LICENSE",
                        f"{len(names)} files" + (f"; ships {shipped[:3]}" if shipped else "")
                        + (f"; missing {needed}" if needed else ""), not shipped and not needed)
                target = scratch / "custom_nodes" / facts["name"]
                target.mkdir(parents=True)
                z.extractall(target)
            port = a.port or free_port()
            base, where = f"http://127.0.0.1:{port}", f"scratch server, {sys.platform}"
            logpath = pathlib.Path(a.log) if a.log else scratch / "comfyui.log"
            log = open(logpath, "w", encoding="utf-8")
            proc = start_server(a.comfyui, a.python, scratch, port, a.desktop_flags, log)
        else:
            rep.skip("zip", "the Registry's node.zip", "a running server was named, so it was not installed here")

        up = wait_up(base, proc, a.timeout)
        if up:
            version = (http(base, "/system_stats")[1] or {}).get("system", {}).get("comfyui_version", "?")
        rep.add("server", "/system_stats answers", f"ComfyUI {version}" if up else "no answer", up,
                "" if up else "the server did not start; the log has why")
        if not up:
            return rep, where, version

        if proc is not None:
            log.flush()
            text = pathlib.Path(log.name).read_text(encoding="utf-8", errors="replace")
            failed = [ln.strip() for ln in text.splitlines() if "IMPORT FAILED" in ln and facts["name"] in ln.lower()]
            rep.add("import", "the pack imports", failed[0] if failed else "imported", not failed)
        else:
            rep.skip("import", "the pack imports", "the log belongs to whoever started the server")

        code, info = http(base, "/object_info", timeout=120)
        missing = [c for c in facts["classes"] if not (isinstance(info, dict) and c in info)]
        rep.add("nodes", f"{len(facts['classes'])} node classes in /object_info",
                "missing " + ", ".join(missing) if missing else f"all {len(facts['classes'])} present", not missing)
        if "PreviewAny" not in (info or {}):
            rep.add("gates", "core PreviewAny exists to end the gate prompt", "this ComfyUI has no PreviewAny", False)
            return rep, where, version

        if facts["web"]:
            code, exts = http(base, "/extensions")
            want = sorted(p.name for p in (REPO / facts["web"]).glob("*.js"))
            have = [w for w in want if any(str(e).endswith("/" + w) for e in (exts or []))]
            rep.add("web", "the pack's scripts in /extensions: " + ", ".join(want),
                    "served: " + (", ".join(have) or "none"), have == want)

        for (consent, adult), sentence in sorted(sentences.items()):
            case = f"gate-consent-{'on' if consent else 'off'}-adult-{'on' if adult else 'off'}"
            code, resp = http(base, "/prompt", {"prompt": gate_prompt(facts["gate"], consent, adult),
                                                "client_id": str(uuid.uuid4())})
            said = error_text(resp)
            ok = code == 400 and sentence in said
            rep.add(case, f"refused with: {sentence}", f"HTTP {code}: {said[:300]}", ok)

        code, resp = http(base, "/prompt", {"prompt": gate_prompt(facts["gate"], True, True),
                                            "client_id": str(uuid.uuid4())})
        if code != 200:
            rep.add("gates-on", "queued and ran", f"HTTP {code}: {error_text(resp)[:300]}", False)
        else:
            status = wait_history(base, resp["prompt_id"], 120)
            done = bool(status) and status.get("status_str") == "success"
            rep.add("gates-on", "queued and ran to success",
                    (status or {}).get("status_str", "no history after 120 s"), done)
        return rep, where, version
    finally:
        if proc is not None:
            proc.terminate()
            try:
                proc.wait(30)
            except subprocess.TimeoutExpired:
                proc.kill()
        if log is not None:
            log.close()
            if not rep.passed or a.show_log:
                print("---- ComfyUI log (tail) ----")
                print("\n".join(pathlib.Path(log.name).read_text(encoding="utf-8", errors="replace")
                                .splitlines()[-60:]))
        if scratch is not None and not a.keep:
            shutil.rmtree(scratch, ignore_errors=True)


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    where = p.add_mutually_exclusive_group(required=True)
    where.add_argument("--comfyui", help="a ComfyUI source folder to start a scratch server from")
    where.add_argument("--server", help="the URL of a running server that already has the pack")
    p.add_argument("--python", default=sys.executable, help="the Python that runs ComfyUI (its venv's)")
    p.add_argument("--zip", help="the node.zip from `comfy node pack` (default: build the same thing here)")
    p.add_argument("--port", type=int, help="the scratch server's port (default: a free one)")
    p.add_argument("--desktop-flags", action="store_true", help="add the two flags Comfy Desktop launches with")
    p.add_argument("--venue", default="ci", help="the report's venue: ci, desktop, cloud-parity")
    p.add_argument("--timeout", type=int, default=600, help="seconds to wait for the server to answer")
    p.add_argument("--json", help="write the report here")
    p.add_argument("--log", help="write the scratch server's log here")
    p.add_argument("--keep", action="store_true", help="keep the scratch base directory")
    p.add_argument("--show-log", action="store_true", help="print the log tail even when every row is green")
    a = p.parse_args()
    if a.server:
        a.server = a.server.rstrip("/")
    rep, where, version = run(a)
    md = rep.markdown(where, version)
    print(md)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write(md)
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(rep.document(where, version), indent=1), encoding="utf-8")
    return 0 if rep.passed else 1


if __name__ == "__main__":
    sys.exit(main())
