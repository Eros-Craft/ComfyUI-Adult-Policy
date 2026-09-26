"""ComfyUI-Qwen21-Adult-Policy: ErosCraft's content policy for the Qwen Image 2.1 Image Creator.

Five nodes. Two are the gates a person sees on the form, ✅ Consent and 🔞 18+; three check the words, the photos,
the prompt enhancer's rewrite and the finished image against the rules those gates do not override; and one is the
➕ Civitai Red LoRA picker. The policy engine (`qwen21_adult_policy/policy.py`) is generated into this pack at build
time from the shared one, so every ErosCraft product judges a request the same way.

The questions are asked through the stock Qwen3-VL 8B text encoder the workflow already loads, so this pack needs no
model of its own.
"""
from .qwen21_adult_policy import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

WEB_DIRECTORY = "./js"          # the ➕ Civitai Red picker

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
