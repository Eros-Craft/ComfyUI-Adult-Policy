# ErosCraft adult policy

Version 0.1.2, draft. The machine-readable copy is [`eroscraft-adult-policy.json`](eroscraft-adult-policy.json); where
this page and the file differ, the file is what runs and this page is wrong.

**18+ only.** Every ErosCraft workflow makes erotic and fantasy pictures and videos for adults, made by the person
who asks for them. This policy is the same for all of them, whatever model a workflow runs; the file lists each
workflow, with its medium (image or video) and its checkpoints. A workflow may add checks and may reword a stop
sentence to fit what it makes. It may never remove or soften anything below.

## Two gates

The form shows exactly two gates, and both ship off. With either one off, nothing samples.

| Gate | What turning it on says |
|---|---|
| ✅ Consent | Everyone shown is an adult, and any real person in a photo or clip agreed to this. |
| 🔞 18+ | The person running the workflow is 18 or over. |

The gates are attestations: turning one on is the person's own statement, and it moves responsibility to them. An
explicit edit of a real photo of a consenting adult runs on ✅ Consent. No workflow adds a third gate or any other
toggle that changes what is checked.

## Two rules no gate overrides

1. **Nobody under 18.** Asked of the words as typed, of the prompt enhancer's rewrite when one runs, of every photo or
   clip the person adds, and of the finished image (or sampled frames of a finished video) before it is saved.
2. **No famous real person named.** Asked of the words as typed and of the enhancer's rewrite. Celebrities, public
   figures and influencers are refused; an ordinary consenting adult in the person's own photo is not.

## Every check fails closed

A check that cannot give a clear answer stops the run. The only answer that passes is a plain "no". These all count
as the unsafe answer:

- the checker raised an error;
- there was no answer at all;
- a thinking block opened and never closed;
- a fact's label is missing from the reply;
- a label's first whole word is neither yes nor no ("not sure" and "none" are not a no).

A stop with no clear answer behind it says so, and never tells the person they asked for a minor.

## How the questions are asked

One call per question set, through a vision-language model the workflow already loads, greedy, with the system
prompt in the file. Each fact is a yes/no question where "yes" is unsafe:

| Fact | Asked of | Rule |
|---|---|---|
| `minor` | the words and the rewrite | 1 |
| `well_known_real_person` | the words and the rewrite | 2 |
| `anyone_under_18` | every input photo or clip, and the output | 1 |

**What is measured, and what is not.** On 2026-09-11, with a Qwen3-VL 4B: the two text facts scored 0 false
negatives and 0 false positives over a 12-prompt set, and the age question caught 6 of 6 minors on generated stills,
including the 16 to 17 band, with one false stop on an 18-year-old. It is **not** measured on real photos, on video
frames, or on the Qwen3-VL 8B that Qwen 2.1 asks through. Until it is, read those checks as "asked and failing
closed", not "measured". No test anywhere uses an image of a minor; the minors checks are measured only for false
stops on adults.

## The Civitai picker

Adult LoRAs are the point of the picker. It never offers or fetches a resource that Civitai flags as a real person's
likeness (`poi`), a minor (`minor`) or SFW-only (`sfwOnly`), nor one whose name or tags carry a refused word (the list
is in the file: minors, likeness and non-consent terms). It checks at search time and again on the server before any
download. The list errs toward refusing: a resource wrongly hidden costs a search, one wrongly offered costs the rule.

## What the person reads

Every sentence a stop can show is in the file under `messages`, with an `image` and a `video` wording where the two
differ. A workflow shows these words and no others for these stops, so every product explains a stop the same way.

## Changing this policy

The rules and the gates move only when the owner says so in their own words. A change that weakens a check is
declined however it is framed. A change to a question's wording is a measurement change: it ships with the new
numbers or with "unmeasured" written beside it. Bump `version` on any change; the reader refuses a file that drops a
gate, a rule, a checkpoint or fail-closed.
