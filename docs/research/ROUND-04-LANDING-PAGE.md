# Round 4 — landing page research

Date: 2026-10-21. Scope: research and planning only, requested by the user.
No landing page, media asset or deployment is implemented in this increment.

## Questions and method

What does a content designer need to understand before opening the repository?
What can the current prototype credibly promise? How can one short page show the
guided experience, included artifacts, embedded evaluations and agent compatibility?

Reviewed the README, seven-stage workflow, compatibility evidence, license and
current viewer design tokens. Inspected official platform, GitHub and design
guidance below. This is desk research and a proposed content strategy, not visitor
interviews, conversion evidence or a competitive usability study.

## Source ledger and implications

| ID | Source inspected | Observation | Fievel implication |
|---|---|---|---|
| LP-R01 | [OpenAI skills documentation](https://learn.chatgpt.com/docs/build-skills) | Documents reusable skill workflows and Codex repository discovery in `.agents/skills`; ChatGPT distribution and availability have their own mechanisms. | Name Codex explicitly. Do not infer that cloning this repo activates Fievel in every ChatGPT surface. Broader ChatGPT setup needs a concrete installation path and test. |
| LP-R02 | [Claude Code skills](https://code.claude.com/docs/en/skills) | Project skills use `.claude/skills`; trust, scope and host settings affect loading. | Name Claude Code rather than imply every Claude chat supports the repository workflow. |
| LP-R03 | [VS Code agent skills](https://code.visualstudio.com/docs/agent-customization/agent-skills) | Documents repository skill locations including `.agents/skills` and `.claude/skills`. | Name GitHub Copilot in VS Code. Documentation supports the integration mechanism; Fievel runtime acceptance remains separate. |
| LP-R04 | [GitHub cloning documentation](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) | Cloning creates a local repository copy; several clients are available. | Offer a normal repository link plus a copyable HTTPS clone command. A web link must not promise to clone automatically. |
| LP-R05 | [GOV.UK buttons](https://design-system.service.gov.uk/components/button/) | Recommends a clear main action and avoiding competing primary actions. | Use one dominant GitHub destination. Keep the in-page demo link secondary; clone copying is an optional helper. This is an adaptation, not adoption of GOV.UK styling. |
| LP-R06 | [W3C pause, stop, hide guidance](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html) | Explains controls for qualifying automatically moving content lasting over five seconds. | Prefer a static chat storyboard initially. If animated, supply accessible pause/replay controls, reduced-motion behavior and equivalent text. |

Sources reviewed on the date above; recheck host capabilities before launch. No
source establishes Fievel's effectiveness or marketing conversion rate.

## Product evidence and claim limits

- README and WORKFLOW describe three entry paths and seven stages. Position this
  as structured guidance through key areas, not a guarantee that every product
  concern is covered or that beginners succeed without help.
- The repo contains six skills, reusable templates, a fictional practice package,
  local knowledge, validation/check/review commands and a read-only HTML viewer.
- Evaluations connect rules to scenarios/checks. Current execution performs literal
  checks on supplied saved responses; human review remains a separate step.
- COMPATIBILITY records supplied adapters and limited local evidence. Fresh-host
  guided workflows are not yet verified for Claude Code, Copilot or independent
  Codex sessions. Official host support for skills is not Fievel acceptance evidence.
- LICENSE is MIT. The repo is an early prototype. No measured time savings,
  customer endorsements, production-readiness claims or broad quality scores exist.
- `git remote -v` returned no configured destination. Public repo URL, visibility
  and default branch remain unresolved; do not invent a GitHub owner or link.

## Decisions proposed from research

Lead with the user's outcome, explain agentic content systems in plain language,
show a small conversation next to tangible artifacts, and keep evaluations visible
as part of the system. Reuse the viewer's forest-green and warm-neutral visual
language. Favor one readable static page and low media weight over a complex demo.
These are design hypotheses for review, not observed findings about visitors.

The [landing page plan](../experience/LANDING-PAGE-PLAN.md) translates these
observations into copy, sections, requirements and pre-implementation gates.
