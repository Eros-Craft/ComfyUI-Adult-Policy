# Qwen 2.1 Adult Policy

**18+ only.** This pack is for adult content and is off until both gates are turned on.

ErosCraft's content policy for a Qwen Image 2.1 workflow, and the only place adult text exists in this package.

| Node | What it does |
|---|---|
| 🔞 ErosCraft policy | The two gates, ✅ Consent and 🔞 18+, and the policy they unlock. Both ship off. |
| 🔞 ErosCraft gate | Before anything samples: checks the words and every photo. The request and the photos pass through it, so the sampler cannot be reached around it. |
| 🔞 ErosCraft rewrite check | Checks the words the prompt enhancer wrote, like words the person typed. |
| 🔞 ErosCraft output check | Before anything is saved: checks the image that was actually made. |
| ➕ Civitai Red LoRA | A LoRA fetched from Civitai Red for Qwen Image 2.1, and its strength. The ➕ button searches and downloads with the machine's own token. |

## Install

In ComfyUI-Manager, search for "Qwen 2.1 Adult Policy". Or, with comfy-cli:

    comfy node install comfyui-qwen21-adult-policy

## The rules

The two gates are attestations. Turning them on is the person's statement about their own age and about anyone
real in a photo, and it moves responsibility to them. With either one off, nothing samples.

Behind them, two rules that no toggle overrides:

1. **Nobody under 18.** Asked of the words, of the enhancer's rewrite, of every photo, and of the finished image.
2. **No famous real person named.**

**Every check fails closed.** An error, a missing answer, an unparseable answer, or a reply whose thinking never
closed all count as the unsafe answer, so an unreliable check stops a run rather than passing it.

The questions are asked through the stock Qwen3-VL 8B text encoder the workflow loads, whichever encoder the person
chose for the picture.

## The picker

It lists Qwen Image 2.1 LoRAs from Civitai Red and never offers a resource flagged as a real person's likeness, a
minor, or SFW-only, nor one whose name or tags suggest a minor, a likeness or non-consent. It checks again on the
server before any download. Downloads need `CIVITAI_TOKEN` on the machine, and never reach the page.

Examples: https://civitai.red/user/Generate-AI-1

MIT licensed, Copyright (c) 2026 Generate-AI-1.
