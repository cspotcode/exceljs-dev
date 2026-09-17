---
name: rewrite-terse
description: Rewrite a plan, document, or file into terse, concise style inspired by Simplified Technical English and GOV.UK content design. Use when the user runs /rewrite-terse.
disable-model-invocation: true
---

# Rewrite Terse

Rewrite the target content in a terse, plain style. Do not change its meaning, scope, or technical accuracy — only its wording and structure.

## Target

The argument names what to rewrite: "this plan", "these docs", "this file", a file path, or a pasted block of text. Resolve it from context:

- "this plan" → the plan currently under discussion (e.g. an active ExitPlanMode draft, or the most recent plan-shaped text in the conversation).
- "this file" / "these docs" → the file(s) the user has open, selected, or just referenced.
- If ambiguous, ask which file or text to rewrite rather than guessing.

## Style rules

Apply these rules, drawn from Simplified Technical English (STE) and the GOV.UK content style guide:

1. **One idea per sentence.** Split compound and multi-clause sentences.
2. **Short sentences.** Aim for under 20 words. Under 25 is a hard ceiling.
3. **Active voice, imperative for instructions.** "Click Save", not "Save should be clicked" or "You should click Save".
4. **Common, everyday words.** Replace jargon and formal words with plain ones: "use" not "utilize", "help" not "facilitate", "start" not "commence", "about" not "approximately". Keep necessary technical terms, but don't decorate them.
5. **Cut hedges, filler, and throat-clearing.** Remove "in order to", "it should be noted that", "please note", "basically", "essentially", "simply", "just", "really", "very", "in general", "at this point in time".
6. **Cut redundant qualifiers and intensifiers.** No "very unique", "quite important", "extremely fast" — pick the direct word.
7. **No nominalizations.** Prefer verbs over noun forms: "we decided" not "we made a decision", "check" not "perform a check on".
8. **Consistent terminology.** Use one term per concept throughout. Don't vary vocabulary for style.
9. **Front-load the point.** Lead each sentence, paragraph, and section with its conclusion or instruction, not background.
10. **Prefer lists and tables over prose** when content is enumerable (steps, options, criteria).
11. **Short paragraphs.** 3–4 sentences max. One topic per paragraph.
12. **Concrete over abstract.** Name the actual thing ("the config file", "the API key") instead of vague nouns ("the aforementioned item", "said resource").
13. **No decorative adjectives or adverbs.** Cut words that don't change meaning or action.
14. **Keep numbers, names, code, commands, and technical facts exact.** Terseness never trims precision — don't drop units, versions, flags, or conditions.

## What NOT to cut

- Do not remove information, caveats, or edge cases — only the words around them.
- Do not compress warnings, security notes, or "why" explanations that justify a non-obvious decision. Shorten their wording, keep their substance.
- Do not merge distinct steps into one to save lines — each actionable step stays separate.

## Process

1. Read the full target content before rewriting.
2. Rewrite it in place, section by section, applying the rules above.
3. Preserve structure that already works (headings, code blocks, existing lists) — reshape prose, don't reformat things that are already terse.
4. Show the user a diff or before/after, don't just silently overwrite unless they're mid-flow on a plan draft (e.g. rewriting an ExitPlanMode plan before presenting it).
5. If the rewrite would remove a claim or caveat that isn't purely stylistic, flag it instead of silently dropping it.
