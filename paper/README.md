# WWW '27 paper

LaTeX source for the ACM Web Conference 2027 submission (ACM `acmart`, `sigconf`).

## Layout

```
paper/
├── main.tex            driver: class options, metadata, \input of every section
├── preamble.tex        packages + macros (\sys, \corpus, \todo, \term, \ttype, \src)
├── sections/
│   ├── 0_abstract.tex
│   ├── 1_introduction.tex   <- MUST contain the "Relevance to the Web" paragraph
│   ├── 2_related_work.tex
│   ├── 3_problem.tex
│   ├── 4_method.tex
│   ├── 5_experiments.tex
│   ├── 6_discussion.tex     limitations, ethics, reproducibility
│   ├── 7_conclusion.tex     ends with \balance
│   └── 8_appendix.tex       optional; after references
├── references.bib      seeded from literature review/ and legal/ (TODO verify flags)
├── figures/            PDF/PNG figures (\graphicspath set)
├── tables/             optional standalone table .tex files to \input
├── scripts/check_pages.sh
├── latexmkrc           pdflatex + bibtex, output in build/
└── Makefile
```

## Build

```bash
make            # -> build/main.pdf
make pages      # page budget report (body <= 8, total <= 12)
make watch      # recompile on save
make camera     # camera-ready variant (no line numbers, authors shown)
make clean
```

Review vs camera-ready is a single switch in `main.tex`: `\camerareadyfalse` / `\camerareadytrue`.
In review mode `\todo{}` renders red, `\note{}` blue; both vanish in camera-ready.

## Page budget (WWW '27 CFP)

| Item | Limit |
|------|-------|
| Main body (long paper) | 8 pages, self-contained |
| Body + references + appendix | 12 pages |
| Short paper | 4 pages incl. references + appendix |

Suggested body allocation: intro 1.25 · related 0.75 · problem 0.5 · method 2 · experiments 2.5 · discussion 0.5 · conclusion 0.25 · figures/tables ~0.25.

## Parked for the next version

Human expert validation is deferred (decided 2026-10-26); the paper states this in the
conclusion instead of carrying red placeholders for it:

- expert judgement of a sample of ~100 is-a edges on a 1-3 scale with inter-annotator agreement
  (RQ2);
- expert review of a slice of the tags for precision and recall (RQ3);
- relevance judgements on a query sample for the retrieval ranking (RQ4).

## Submission checklist (from the CFP)

- [ ] `\documentclass[sigconf, anonymous, review]{acmart}` (default here)
- [ ] First page states how the work relates to the Web **and names the track**
- [ ] No author names/affiliations; own prior work cited in third person; no identifying acks
- [ ] Ethics paragraph on data use (public legal texts, no personal data; IRB ref if annotators)
- [ ] Reproducibility: anonymised code/data link; apply for "Artifacts Available" badge
- [ ] CCS concepts + keywords filled (https://dl.acm.org/ccs)
- [ ] `\acmSubmissionID` set to the OpenReview number
- [ ] All `TODO verify` entries in `references.bib` checked
- [ ] `make pages` reports body <= 8 and total <= 12
- [ ] Single PDF, fonts embedded (`pdffonts build/main.pdf` shows no Type 3)
- [ ] LLMs used only for rephrasing; authors responsible for all text (CFP policy)

Candidate tracks: *Semantics and Knowledge* (taxonomy/ontology induction) or
*Web Economics and Digital Society* (regulation of Web-native finance).

Key dates (WWW 2027, Dublin): abstract 18 Oct 2026, full paper 25 Oct 2026 (AoE),
rebuttal 15–20 Dec 2026, notification 4 Jan 2027, camera-ready 31 Jan 2027.
