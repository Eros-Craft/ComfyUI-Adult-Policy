# Security

This pack enforces an adult content policy: two gates, two background rules no toggle overrides, and checks that fail
closed. A way around any of them is a security issue, and so is anything that lets another website use a ComfyUI
server this pack runs on, or lets a Civitai key reach a page.

## Report one privately

Use GitHub's private vulnerability reporting:
[Report a vulnerability](https://github.com/Eros-Craft/ComfyUI-Qwen21-Adult-Policy/security/advisories/new) (the Security tab of this
repository). Please do not open a public issue for it.

Say which version (the `version` in `pyproject.toml`, or what ComfyUI-Manager shows), what you did, and what passed
that should have stopped. Describe a prompt in words. Never attach an explicit image, and never an image of a minor or
of anyone who could be one: a report that needs a picture needs only a safe-for-work stand-in.

## What happens next

The report is read by the maintainer. A fix ships as a new version on the Comfy Registry (a published version can
never change), and the advisory is published once the fixed version is available. Only the newest version is
supported.
