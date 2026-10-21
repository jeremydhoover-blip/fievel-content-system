# Independent reviewer instructions

This folder contains three fictional response cases. No live model was run.
Review both checks for each case using only the supplied saved evidence. Work
independently before discussing the cases. Do not inspect the other reviewer folder
or organizer notes, author expectations, or comparison worksheet first.

For each case, read its Markdown sheet and JSON evidence file. The JSON includes
complete frozen context, declared source metadata, exact rule text, supplied source
excerpt, rubric and response origin. Rules and rubric remain draft exercise material.

Keep the original pending files. Make a completed copy in your own output folder.
In each JSON copy enter your declared reviewer identity and a timezone-aware
reviewed_at timestamp. For each judgment, enter pass, fail, borderline or
insufficient_evidence, explain your rationale and quote an exact response excerpt
in response_evidence. Do not change context, rules, hashes or rubrics. Record the
actual time; do not copy an example timestamp as a claim about your review.

Use borderline when the response's interpretation is ambiguous, and
insufficient_evidence when the saved context cannot support a decision. Do not
force either to pass or fail just to complete a form. Assess the two checks
independently: a useful next step does not erase an unsupported factual claim.

Check each saved copy with:

```sh
python scripts/fievel.py validate-review <your-completed-copy.json>
```

The normal validator permits documented borderline/insufficient_evidence. The
--require-complete gate intentionally rejects unresolved judgments. Calibration
can still use unresolved states to discover weak criteria. Validation confirms
record structure, not that your interpretation is correct.

Also record separately: could you find the relevant rule and evidence, what rubric
wording was unclear, and what information you needed but could not find? Do not
edit the shared rubric until both independent sets of judgments are saved.


## Local form option

Open C01.html, C02.html and C03.html to review without editing JSON by hand.
These pages contain the same pending evidence, with editable judgment fields and
a Download review JSON button. Rename each download to keep the case ID and your
reviewer ID, then validate it with the CLI as above. The browser does not save
changes into the page, and edits are lost on reload unless downloaded first.
No human judgments have been entered in the supplied pages.
