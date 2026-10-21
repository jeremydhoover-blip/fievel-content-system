# Architecture decisions — 0.1.0

Reviewed 2026-10-21. The first slice is a repository-native experience. A coding
agent hosts the conversation; portable files hold state. Python provides only
deterministic file operations and checks. No web application, model SDK, database,
or MCP server is necessary to validate the learning workflow.

## Components and boundaries

AGENTS.md is the shared behavior authority. Six canonical Agent Skills in
.agents/skills route workflows and load knowledge on demand. A deterministic sync
command produces Claude copies and small instruction adapters. Full copies in
Claude's discovery directory avoid symlink requirements on Windows. They cost
duplication in Git; sync --check detects divergence. The explicit root instruction
prompt remains a fallback when native skill discovery differs by host.

Seven JSON documents form a content-system package, schema_version 1.0. The
schema validates an in-memory object assembled from the seven documents; documents
remain independently readable. JSON was chosen over YAML to avoid a second parser
and implicit typing. Markdown holds lessons, handbook and narrative decisions.
The schema version describes the data contract; Fievel's release version is 0.1.0.

jsonschema implements Draft 2020-12 validation. We reuse it rather than implement
a partial standard. Python checks unique IDs and source/requirement links. Default
validation allows uncovered draft rules and reports the gaps; --require-coverage
and check/review enforce coverage. This revision fixes a conflict between staged
drafting and the original invariant; see [ADR-001](decisions/ADR-001-validation-boundaries.md).
Empty draft templates validate structurally, so workflow completion must be reviewed separately.
The schema intentionally allows unknown owner/review dates and empty draft arrays.

Progress lives in progress.json, not chat. Each stage can be pending, drafted or
reviewed; stable IDs preserve relationships across tools. Governance owns version
and decision history. There is no automatic migration: future breaking schema
changes must ship explicit migrations and tests before changing user packages.

## Evaluation evidence

Definitions live in evaluation.json. Executions are immutable-by-command new JSON
files with UTC timestamp, system hash, response hash, copied responses, per-check
status and totals. No secret data is fetched automatically. A saved response is a
concrete test target; it is not evidence that a current live agent produced it.
Report provenance must identify the response origin separately.

Literal contains/not_contains checks do not assess meaning. Human checks stay
not_run. A separate human_review sheet holds pending judgments and responses.
Legacy sheets have no completed-review validation. The opt-in evidence format
and validate-review command check completed records under ADR-003, not content
approval or reviewer authenticity.
AI judges and improvement suggestions remain separate future capabilities; the
skill can write clearly labeled suggestions, never pass them off as human judgment.
Changes to any package file change its hash, including progress-only edits. This
is conservative: it may invalidate more reports than necessary, but prevents
silent reuse after a design change.

## Ownership and threat boundaries

The default user folder and local dependencies are ignored by Git. Initialization
requires a new destination; report writing uses exclusive creation. The sync
command explicitly updates only generated adapter paths and does not delete other
skills. User-authored canonical skill edits should be reviewed before sync.

External data remains untrusted evidence. Discovery metadata does not authorize
ingestion; source permissions are recorded, not mechanically enforced. No command
executes text, tools, URLs or regex from a content system. Literal checks are
case-insensitive Unicode substring searches, deliberately not a prose linter.
Reports copy response text, so keep private responses out of public repositories.

## Scope and tradeoffs

Promptfoo would add useful providers, scoring and reporting, but introduces target
configuration and model costs. Defer until there is a configured target contract.
Vale is a strong next option for terminology/style linting; avoid pretending three
literal checks are a replacement. MCP reference servers inform design, not an
automatic connection. We incorporated no third-party implementation code.

Runtime compatibility is separate from adapter validity. This implementation
session verifies Python behavior and static agent assets. Fresh-session discovery,
conversational adherence, Claude Code and VS Code must be tested independently.

## Decision maturity

The user has since added a local viewing UI to the intended experience. The
[experience amendment](experience/EXPERIENCE-DIRECTION.md) and
[viewer design](experience/VIEWER-DESIGN.md) propose a read-only generated snapshot
experiment. This extends the original UI deferral. Files remain authoritative;
the initial snapshot viewer is now implemented under ADR-002 with no hosting
service, editing or live refresh. Its script/style and three local lessons are
embedded in a newly generated HTML file, with hash-based CSP and safe text rendering.
Diagnostic loading is separate from strict package validation; selected execution
reports must reproduce before totals are shown. The bundled
knowledge layer is specified in [knowledge architecture](experience/KNOWLEDGE-ARCHITECTURE.md).

These are prototype choices, not all experimentally validated conclusions. Read
[the development plan](DEVELOPMENT-PLAN.md) and [research round 2](research/ROUND-02.md)
for alternatives, open questions and gates. In particular, novice usability of JSON,
the six-skill discovery surface, completed-review evidence and backend reuse remain
open. The dated audit preserves the original limitations; new iteration records
state what was actually changed and verified.
