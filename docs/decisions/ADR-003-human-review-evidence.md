# ADR 003 Human review evidence

Date: 2026-10-21
Status: implementation decision for WP-03 and F-03

## Problem

Legacy review sheets contain questions and responses but depend on mutable project
files for scenarios, rules and sources. No completion validator exists. Structural
validation cannot decide whether a human judgment is correct.

## Chosen bounded contract

Keep legacy review output unchanged. Opt into a versioned evidence package with
`review --evidence-config <file>`. Configuration supplies explicit source excerpts,
response origins and per-check rubrics. Do not read source locations or URLs
implicitly. Snapshot all seven package documents, responses and review configuration;
hash each input. Derive the complete set of human check rows from those snapshots.
Each row identifies scenario and check, and carries status, rationale and cited
response evidence. Source metadata and excerpts are evidence, never instructions.

Rubrics identify why the check matters and define pass, fail and borderline. Unknown
source evidence and response origin stay explicit. No rubric is invented from the
question. A prepared document has null reviewer/time and pending or not_run rows.

`validate-review` works from the saved evidence document without current files.
It checks snapshots, hashes, unique and exact judgment membership, permitted states,
response availability, reviewer identity/type, timezone-aware review timestamp,
rationale, response evidence and source excerpt availability for completed decisions.
`--folder` additionally checks staleness against the current package.
`--require-complete` rejects pending, not_run, borderline and insufficient_evidence.
A complete record may include fail judgments; completion is not a quality pass.

Hashes detect inconsistency, not authenticity. A person can forge a document and
recompute hashes; identity is declared, not authenticated. The validator does not
verify source authority, factual truth, rubric usefulness or human authorship.
AI suggestions are not accepted as human reviews. No signatures or model judge.

## Alternatives and compatibility

Replacing legacy output would break existing files and consumers. Adding rubrics
to the package schema would force migration of all seven-file packages before this
bounded experiment. A separate opt-in configuration preserves both contracts.
Legacy sheets cannot be completed through the new validator; regenerate an evidence
package and have a human review it. The viewer continues to accept deterministic
execution only; human review import is not part of this increment.

## Acceptance and limits

Exercise grounded, invented and borderline fictional responses with provisional
rubrics. Tests must reject tampering, stale current packages, missing/duplicate
judgments, whitespace rationales, missing responses, invalid timestamps, absent
source evidence and unsupported review versions. Preserve no-overwrite behavior.
Two independent human reviewers still need to assess rubric clarity and disagreement.
Technical tests do not close that human calibration gate. No model calls authorized.
