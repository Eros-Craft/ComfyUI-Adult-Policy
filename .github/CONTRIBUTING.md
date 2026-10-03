# Contributing

Thank you for looking. Two things about this repository first.

**It is an export.** The pack is developed and tested inside a private workflow repository, and each released version
is exported here as one commit and tag. A pull request is read, and a change that is accepted is made in the source
and arrives in the next exported version, credited to you; the pull request itself is then closed rather than merged.

**Except `policy/`.** The adult policy every ErosCraft workflow shares lives in `policy/` here and nowhere else, so a
pull request that changes it is reviewed and merged in this repository, and each workflow adopts the new words from
here. `python3 policy/test_policy.py` has to pass, and the checks run it on every pull request. A change may make a
rule stricter or its message clearer; one that weakens a rule is declined ([policy/POLICY.md](../policy/POLICY.md)).

**Testing in ComfyUI.** How a change is tested in ComfyUI Desktop and on Comfy Cloud, safe-for-work prompts only, is
in [testing/TESTING.md](testing/TESTING.md).

**Every test is safe for work.** Issues, pull requests, examples and tests carry no explicit content and never an
image of a minor or of anyone who could be one. The gates and the two background rules are not up for removal; a
change that weakens a check is declined however it is framed.

Every pull request runs the [checks](https://github.com/Eros-Craft/ComfyUI-Adult-Policy/actions/workflows/checks.yml): the Comfy
Registry's security rules, every file parses, and nothing the export would refuse (an em dash, a key, a local path).

A bug is an [issue](https://github.com/Eros-Craft/ComfyUI-Adult-Policy/issues/new/choose). A way around a gate or a rule is a
[private security report](https://github.com/Eros-Craft/ComfyUI-Adult-Policy/security/advisories/new), never an issue
([SECURITY.md](SECURITY.md)).
