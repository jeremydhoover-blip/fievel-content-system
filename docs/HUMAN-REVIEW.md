# Human review evidence

The legacy `review` command still creates the original pending sheet. The opt-in
format below adds saved context and an independent completion validator. Neither
format performs human review for you or certifies response quality.

## Prepare a review

Create a review configuration with version, rubrics, source_evidence and
response_origins. The fictional example in examples/review-evidence-config.json
shows the complete shape. Its rubrics are draft teaching/test material, not approved
company standards. They have not been calibrated with independent human reviewers.

For the unchanged fictional Wayfarer example:

```sh
python scripts/fievel.py review examples/wayfarer --responses examples/responses-good.json --evidence-config examples/review-evidence-config.json --out my-content-system/results/evidence-review-01.json
python scripts/fievel.py validate-review my-content-system/results/evidence-review-01.json
```

Use new output names; preparation refuses overwrites. No network requests occur.
Source locations in sources.json are not opened automatically. Include only excerpts
you have authorization to copy. Saving or sharing the review shares its embedded
project data, response text, source metadata and excerpts.

Each human check needs one rubric identified by scenario_id and check_id, with why,
pass, fail and borderline criteria. Check IDs are scoped to their scenario. Each
supplied response needs a declared origin kind and description. Origin can be
unknown with a null description, but cannot support completed pass/fail decisions.
For each source excerpt supply source_id, locator and excerpt. Missing evidence
can remain missing while preparation and discussion continue.

## Inspect the saved context

The review remains readable without the current package:

- system_snapshot/product holds product context.
- system_snapshot/evaluation/scenarios holds the situation, context, question and
  requirement_id for each scenario/check pair.
- Find that requirement_id in system_snapshot/standards/rules or behavior/rules
  to inspect the exact instruction, its draft/approved status and source IDs.
- system_snapshot/sources contains declared authority, ownership and permissions.
- review_config/source_evidence contains supplied passages and locators.
- review_config/rubrics contains the agreed or proposed assessment criteria.
- responses and review_config/response_origins identify the actual saved target.

Metadata is not verified authority. A quoted source can still be outdated or wrong.
A valid review does not approve a draft rule. Confirm rubric interpretation with
reviewers before depending on it for decisions.

## Record a human judgment

Keep the original pending file and edit a copy for the reviewer. Change only
reviewer, reviewed_at and the judgment fields. Keep reviewer_kind as human. Enter
the reviewer's declared identity and a timezone-aware timestamp such as
2026-10-21T14:30:00+03:00. Do not manufacture this metadata on someone's behalf.

For each available response:

- pass or fail: apply the saved rubric, record a substantive rationale and copy an
  exact response excerpt into response_evidence. For absence-based checks, quote
  enough of the response to explain the omission. The validator checks the quote,
  not whether the rationale is correct or complete.
- borderline: record the ambiguity, response excerpt and rationale for discussion.
- insufficient_evidence: record the missing evidence and response excerpt without
  inventing facts or silently converting uncertainty to pass.
- pending: no judgment has been made; rationale and response_evidence stay empty.

A missing response stays not_run with empty judgment fields. It cannot be judged.
Each expected human check must appear exactly once. Referenced source IDs need
supplied evidence for pass/fail, and response origin must be recorded. Source-free
rules remain reviewable against their saved instruction and scenario context;
this does not invent organizational approval.

```sh
python scripts/fievel.py validate-review my-content-system/results/completed-review-01.json --require-complete
python scripts/fievel.py validate-review my-content-system/results/completed-review-01.json --folder examples/wayfarer --require-complete
```

The first validates against frozen context. Adding --folder also rejects a stale
review when any current package document differs, including progress changes.
Both commands are read-only. Exit 0 means the requested record checks passed;
exit 2 indicates invalid or incomplete evidence. A fully completed review can
contain failures. There is no overall quality pass label.

## Migration and boundaries

Legacy sheets and deterministic execution reports retain their original shapes.
The new validator accepts only human_review_evidence version 1.0. To move an old
sheet forward, prepare a new evidence package and have a human review it. Do not
copy old results onto changed context. No package schema migration is required.
The viewer still supports deterministic reports only. AI suggestions must be kept
separate and cannot declare reviewer_kind ai in a human evidence package.

Hashes detect mismatched inputs, not malicious replacement or authenticated identity.
The validator cannot prove that a person wrote the judgments, verify source accuracy,
or assess the usefulness of a rubric. Two independent human reviewers and recorded
disagreement are still needed before claiming calibrated review quality.


## Provisional refund rubric examples

These are authored examples for discussing the no-refund-promise rubric, not
executed human judgments or observed model outputs:

| Draft classification | Saved response example | Why |
|---|---|---|
| Pass candidate | I cannot see your refund status or confirm a date. Contact booking support for an update. | Keeps the date unknown and names a next step |
| Fail candidate | All refunds arrive within 48 hours. | Introduces a universal deadline absent from the fictional handbook |
| Borderline candidate | Your refund should arrive soon. | Vague timing language could imply a promise; reviewers need to discuss that boundary |

Ask two reviewers to judge independently using only the saved evidence. Record
agreement and disagreement before revising the rubric. These proposed labels
must not be copied into a completed human review as observed decisions.


## Review in a local page

Create a read-only evidence snapshot with editable judgment fields:

```sh
python scripts/fievel.py review-page path/to/pending-review.json --out path/to/new-review.html
```

Open the HTML locally. The page shows the scenario, response, rule and source
status, excerpts and criteria beside the judgment fields. Enter reviewer identity,
a review time including timezone, status, rationale and exact response excerpt.
Use current time only when that is the actual time of your review. Missing-response
checks remain disabled and not_run. Source content is displayed as text.

Download review JSON requests a new browser download. It does not write back to
the original JSON or HTML and cannot confirm that your browser saved the file.
Keep original pending files and choose a distinct name/location for downloaded
copies. Browser file-saving behavior is controlled by the browser. There is no
autosave or local-storage persistence; closing/reloading can lose unsaved edits.
The page warns before navigation after edits when the browser supports it.

Run validate-review on the downloaded file. Browser checks are convenience checks;
the Python validator remains authoritative. Unresolved records can be downloaded
with valid metadata/evidence, but cannot satisfy --require-complete. A download
never turns pending work into a human pass. Open a downloaded JSON in a newly
exported page to resume; original snapshots remain unchanged.

No server, fonts, analytics or external requests are needed. Hash-based CSP blocks
external resources and all user text is escaped. Without JavaScript, evidence stays
readable and forms are disabled. The snapshot embeds its evidence; share only with
authorized reviewers. This is technical browser coverage, not accessibility certification.
