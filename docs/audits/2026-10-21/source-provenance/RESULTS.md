# Source provenance audit results

Date: 2026-10-21
Scope: SRC-01, SYS-01, EX-04/06; ADR-005

Implemented read-only sources-audit with explicit audit date, optional freshness
window, optional provenance input, structured findings, strict warning gate and
exclusive output creation. Existing package schema and user files are unchanged.
Updated canonical source-discovery instructions and generated adapters.

Nine new tests exercise metadata gaps, invalid/future/old dates, absence of an
expiry policy, missing/unknown/duplicate/undeclared evidence, declared conflicts,
resolution records, input errors, source-location non-ingestion, CLI status codes,
input preservation and report overwrite refusal. Full suite: 65 tests passed.
Eight adapter checks passed. Example strict coverage and blank template validation
passed. New tests were implemented alongside the feature; no failing-first claim.

Actual CLI evidence: metadata-only.json reports missing evidence locators and an
unspecified age window. with-evidence.json reports zero metadata findings using
explicit passages from the fictional handbook and a supplied 365-day demonstration
window. Neither result verifies original source accuracy, organization policy,
reviewer approval, semantic grounding or undisclosed contradictions.

No model calls, network access, automatic source ingestion or human judgments ran.
No source locations were opened by the audit. Supplied excerpts in the example
were copied deliberately from the authorized fictional exercise, not fetched by
the command. Source meaning and authority still need human review.

Next offline candidates: source/rule consumer export contracts and malformed-input
hardening. Guided-authoring trials remain prepared but not executed. Human rubric
calibration also remains open.
