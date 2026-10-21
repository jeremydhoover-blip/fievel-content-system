---
name: ai-behavior-designer
description: Define AI responsibilities, permissions, uncertainty and recovery rules for a Fievel content system.
---

# AI Behavior Designer

Read AGENTS.md and stage 4 of docs/WORKFLOW.md. Required inputs: product tasks,
actual available tools and the selected project's standards/sources. Ask what the
assistant should explain versus act on. Read knowledge/ai-experience-design/behavior.md
when explanation is useful. Define responsibility boundaries, clarification triggers,
confirmation for consequential actions, uncertainty, recovery and human handoff.

Write behavior.json with stable rule IDs and source links. Tool availability must
be verified; intended integrations are not working tools. The Wayfarer assistant
has no action tools, so must never claim to change or cancel bookings. Personalization
must use only provided context. Never infer hidden account information.

Output: draft behavior rules, linked human or deterministic checks in evaluation.json,
saved decisions/progress. Validate the package. If permissions are unclear, keep the
action unavailable and identify the decision needed. Example: “cancel now” with no
tool -> explain the limitation and give the booking confirmation next step.
