---
name: human-prose-academic
description: Draft, review, and edit academic prose while preserving the author's voice and technical precision. Use for papers, theses, abstracts, literature reviews, research proposals, peer reviews, and responses to reviewers, or when the user asks to make scholarly writing sound less like AI.
metadata:
  short-description: Clear academic prose in the author's own voice
---

# Human prose for academic writing

Write so that a reader can follow the argument and judge the evidence. Preserve the author's voice, use plain language where it carries the same meaning, and remove habits that make prose sound mechanically assembled. Academic formality comes from precision and care with claims.

## Two modes

Choose the mode from the user's request before touching the text.

**Drafting.** The user asks for new text or explicitly requests a rewrite. Apply the principles below from the first sentence. Write only what the argument needs. Preserve supplied results, assumptions, notation, and citations. If necessary evidence is missing, identify the gap or mark a placeholder instead of inventing it.

**Reviewing a draft.** The user asks for feedback, a review, or whether the writing reads well. Quote the troublesome sentence or identify the passage, name the problem, and explain its effect when needed. Leave the wording to the author unless they ask for edits or replacements. An explicit request to edit, polish, or rewrite authorizes changes within that scope.

Skip praise and encouragement as preambles to feedback. Report concrete problems. Useful catches include passive voice that hides responsibility, buried verbs, repeated phrases, filler, paragraphs in the wrong order, redundant sentences, and sentences that require a second reading. Distinguish a prose problem from a question about the research that requires the author's judgment.

For a draft longer than a paragraph, run `python3 scripts/tells.py <file>` from this skill's directory on an available plain-text or Markdown copy. The checker flags mechanical patterns and reports line numbers; it does not establish authorship or decide whether a sentence is wrong. Review each hit in context. It skips Markdown code and frontmatter, but does not parse LaTeX, equations, citations, or bibliographies. Treat hits in those passages as noise; use an existing prose export when available.

## The tells

1. **Describing a claim through an unnecessary negation.** "This is not about accuracy; it is about efficiency." State the contribution directly. Keep contrasts that distinguish hypotheses, methods, or interpretations the reader could reasonably confuse. Remove the rhetorical setup when it adds no information.

2. **Repeated colon splits.** "The explanation is simple: the estimator is biased." Repeated sentence splits become a tic. Use a direct sentence where possible. Colons that introduce definitions, equations, or necessary lists can stay.

3. **Em dashes.** Avoid them in drafted prose. Rebuild the sentence with a direct clause, a separate sentence, or parentheses for an aside. Preserve punctuation inside quotations and source titles.

4. **Invented compound adjectives.** Replace promotional or vague compounds with the property they claim. Preserve conventional technical terms and hyphens that prevent ambiguity, such as "double-blind", "finite-dimensional", or "zero-knowledge". Do not damage a term merely to remove a hyphen.

5. **Words the author would not use.** Prefer "use" to "utilize" and "compare" to "perform a comparison of". Avoid fashionable metaphors and inflated vocabulary. Read [references/tells.md](references/tells.md) for academic examples and consult [references/wordlist.txt](references/wordlist.txt) for common candidates. These are prompts for review. Keep terms with a precise disciplinary meaning, including "robust", "significant", "orthogonal", and "well-defined", when used in that meaning.

6. **Closing restatements.** Cut a paragraph's final sentence when it merely repeats the result in broader language. End on the last useful fact or inference. Keep a conclusion that synthesizes several results, states a limitation, or answers the research question; required abstracts and conclusions still serve a purpose.

7. **Lists where prose would do.** Use connected prose for an argument. Use lists for genuinely parallel assumptions, contributions, research questions, or procedural steps. Preserve a venue's required format. Do not force every paragraph into bullets.

8. **Generic recommendations and future work.** "Further research is needed" and "More experiments should be conducted" add little on their own. Name the unresolved question, the evidence needed, and why it matters when those details are supported. In peer review, connect each requested change to a specific defect or uncertainty.

9. **The rule of three.** Do not invent a third contribution, adjective, or example to complete a rhythm. Use the number the content supports.

10. **Excess structure in short passages.** An abstract, review comment, or short response rarely needs internal headings or bold text. A full paper needs navigable sections. Follow the document's scale and venue conventions.

11. **Throat clearing.** Delete "It is worth noting that", "Importantly", "Crucially", and similar introductions when the sentence stands without them. Begin with the claim, observation, or question. Keep reviewer responses courteous and specific without repetitive thanks or exaggerated deference.

12. **Stacked hedges and unsupported certainty.** Replace "may potentially suggest a possible effect" with the uncertainty the evidence warrants. Preserve substantive qualifications, confidence intervals, assumptions, and limits of generalization. Do not strengthen "is associated with" into "causes", an empirical observation into a proof, or a failure to reject a hypothesis into evidence that it is true.

## Academic precision

Make each claim as specific as the evidence permits. Say what was measured, under which conditions, and against which comparison when those facts are available. Words such as "novel", "optimal", "significant", and "state-of-the-art" need an explicit basis. Avoid claiming priority or superiority from style alone.

Preserve the distinction between prior work, the author's result, and interpretation. Keep citations attached to the claims they support. Never invent references, quotations, experimental results, or proof steps. If rewriting changes a claim's scope, check whether its citation still supports it; flag unresolved support instead of implying verification.

Prefer verbs that name the action. Active voice often clarifies who did what; passive voice is useful when the procedure or object matters more than the actor. Follow disciplinary and venue conventions for first person. Do not force conversational informality or replace necessary terminology with a less accurate synonym.

Preserve notation, quantities, units, logical conditions, and distinctions between related terms. Consistent repetition of a technical term is often clearer than varying it for style. Retain definitions, assumptions, and methodological detail needed to evaluate or reproduce the work.

## The reader test

Read twice before returning text. First follow the argument as a reader in the intended field: can they distinguish the question, evidence, inference, and limits? Then read for prose: does any sentence repeat a point, hide its verb, or make the reader go back?

Match the audience. A specialist paper may rely on shared terminology; an interdisciplinary abstract may need a brief definition. Ask whether the author could explain the idea to a colleague in these words, while keeping the level of formality the document requires.

## When the user wants to retain authorship

Offer this workflow when the user wants help thinking and reviewing while writing the sentences themselves:

1. Organize the author's points or identify gaps in the argument.
2. Let the author write the paragraphs.
3. Review the draft by quoting problems and explaining them, without replacement wording or praise.
4. Let the author revise the flagged passages.

Use this workflow when requested. If the user asks for drafting or rewriting, provide it under the same standards for clarity, evidence, and voice.
