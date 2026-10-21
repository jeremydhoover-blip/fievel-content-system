# Adapter ownership results

Date: 2026-10-21
Scope: F-05 / WP-05, TR-05 and PORT-01

Implemented ADR-004: versioned manifest, first-migration exact-match adoption,
retired-output detection, local-edit conflicts and output-path confinement.
Sync preflights before writes and never deletes files or directories.

Eight new isolated tests cover canonical updates, missing-output restoration,
retirement, rename/manual resolution, unrelated and modified files, legacy
adoption, unowned conflicts and unsafe manifest paths. Full suite: 56 tests pass.
The production migration adopted eight matching adapters. sync --check passes.
No model calls, external requests, native host activation or behavioral trials ran.

Migration cannot identify orphan skills from before ownership was recorded.
No actual user skill was removed. The removal and rename experiments occur only
inside temporary test fixtures. Concurrent editing and disk-failure atomicity are
not guaranteed. New tests were added with implementation; no failing-first result
is claimed. Existing baseline logs and frozen behavioral trial inputs are preserved.

Next: source provenance validation and conflict/freshness visibility. Host behavior
and historical orphan review remain separate acceptance tasks.
