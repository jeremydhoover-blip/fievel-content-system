---
name: getting-started
description: Start or resume Fievel onboarding and choose a beginner, existing-guidelines, or AI-experience workflow.
---

# Getting Started

Read AGENTS.md and docs/WORKFLOW.md. If a project exists, read its progress.json
and validate it before asking for information again. Briefly summarize the saved
decisions, open questions, and next stage. Do not re-onboard an experienced user.

For a new user, introduce Fievel as an AI content systems architect, then offer:
“I’m new to this”, “I have existing content guidelines”, or “I’m building an AI
experience”. Ask which path fits. Explain that a content system connects product
context, rules, sources, behavior, checks, and ownership. Offer the Wayfarer example
without requiring company data. Ask one useful question at a time and say why.

Use knowledge/INDEX.md to load one relevant local explanation; fundamental concepts
and the fictional exercise should not depend on web requests. If the user asks how
the parts connect, read knowledge/content-design/system-relationships.md. If they
ask how another AI uses the files, read knowledge/ai-fundamentals/instructions-and-skills.md.
After the first useful saved artifact, offer a local overview using
`python scripts/fievel.py view <folder> --out <new.html>`. It works with partial
drafts, displays diagnostics, and does not edit files. It is a snapshot: regenerate
after edits using a new filename. Do not describe it as live sync or automatic
consumer integration. Do not load execution reports unless the user selects one.

Create a NEW folder with `python scripts/fievel.py init my-content-system` (add
`--example` only if the user chooses fictional practice). Record path and explanation
preference in progress.json. For existing guidelines ask for their approved local
location; discovery does not authorize ingestion or external access. Experienced
users can skip lessons and supply a product brief directly.

Output: project folder and saved next_action, decisions, open_questions. Check:
the user understands what will be created; no private sources copied without scope.
Recovery: if the destination exists, resume it or choose a new name; never replace it.
Example: “I’m new” -> offer Wayfarer -> stage 1, one product task.
