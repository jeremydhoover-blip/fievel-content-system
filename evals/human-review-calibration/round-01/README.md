# Human rubric calibration round 1

Status: prepared, not_run
Date prepared: 2026-10-21

Purpose: find whether two people can locate evidence, apply the refund rubric and
explain disagreements without access to mutable project files. This is a small
formative exercise, not an estimate of general reviewer reliability.

## Distribution

Give reviewer A only reviewer-a and reviewer B only reviewer-b. Both receive the
same three authored cases and frozen evidence. Do not distribute organizer files
or provisional answer expectations until independent judgments are collected.
The Markdown sheets support reading; JSON files are authoritative review records.
No participant outreach or sharing has been performed.

## Run

1. Ask two people who agree to participate to review independently. They should
   follow their folder's README. Record their declared identities and observations;
   do not manufacture reviewer metadata or complete their judgments for them.
2. Preserve original pending files and collect edited copies. Validate each with
   validate-review. Require actual rationale and response excerpts; record failed
   validation and ask the reviewer to repair the record without coaching judgments.
3. Only after collection, compare statuses and rationales for the six check/case
   pairs in organizer/comparison.json. Keep independent originals unchanged.
4. Discuss disagreements, source-navigation difficulties and ambiguous wording.
   Compare with provisional author notes afterward. Expected labels do not override
   reviewer evidence. Record whether the issue is the rubric, evidence or response.
5. Revise the rubric in a new round. Preserve this round's hashes and failures.
   Rerun affected cases plus a stable comparison case. Do not silently replace old
   criteria or count discussion-derived consensus as independent agreement.

## Decision criteria

Technical input preparation is complete: six review files validate, each with two
pending judgments. The organizer retains hashes and preparation-validation.json.
No human review or agreement measurement is complete. Case-level agreement counts
stay null until actual judgments exist. Borderline and insufficient_evidence are
informative observations, not pass results. Do not invent a numeric success target
or generalize from three authored responses.

The human gate remains open until both reviewers can locate the evidence and the
organizer records their independent outcomes, disagreements and proposed changes.
No model calls or downloads are needed. Clean dependency installation, native agent
activation and live consumer behavior remain separate open gates.
