# Fievel landing page plan

Status: second revision confirmed and implemented locally with publication pending. Date: 2026-10-21.
The original plan below is preserved; I-09 records execution and remaining gates.
User direction: one short page; clear value and GitHub CTAs; consistent design;
included capabilities and guided process; chat preview; embedded evaluations;
compatibility with Claude, Copilot, Codex/ChatGPT and other suitable agents.
Research and claim evidence: [round 4](../research/ROUND-04-LANDING-PAGE.md).
Implementation is a subsequent increment after this plan is reviewed.

## Audience, need and outcome

Primary audience: content designers, UX writers and AI experience designers who
have product knowledge and writing guidance but need help connecting them to AI
behavior and repeatable quality checks. Beginners need an approachable starting
point; experienced designers need a way to bring their existing standards.

The page should answer: What will this help me build? What do I get? What does
using it feel like? Where do checks fit? Can I use my agent? How do I start?
Success means a visitor can explain the outcome and find the repository and first
prompt. Conversion targets and claims about audience preferences await evidence.

## Positioning and draft hero

Eyebrow: **Your AI content systems architect**

Headline: **Turn your content standards into a system your AI can work with.**

Supporting copy: **Fievel guides you from product context and writing rules to AI
behavior, trusted sources and quality checks—in a repository you own. Start from
scratch or bring your existing guidelines.**

Primary link: **Get Fievel on GitHub** → verified public repository root.
Secondary link: **See how it works** → the chat/process section on this page.
Small context line: **Open source · Early prototype · Use with your coding agent**.

Use “agentic content system” in supporting explanation if useful; explain it as
connected instructions, knowledge, behavior and evaluations rather than lead with
unexplained terminology. Avoid claims of automatic integration into a production
agent: the current output still needs consumer-specific integration.

## Single-page structure and copy direction

Target approximately 500–650 words of visible marketing copy, excluding the short
demo transcript and optional setup details. Six compact sections; no separate
feature subpages, pricing, testimonials, newsletter or invented customer proof.

| Order | Section | Message and content | Desired action |
|---|---|---|---|
| 1 | Hero | Outcome, who it helps, ownership and early-prototype label. | Open GitHub; optionally jump to demonstration. |
| 2 | A guide, one useful decision at a time | Three steps: describe your product or bring guidelines; build connected rules, sources and behavior; check, review and improve. Pair with the chat storyboard below. | Understand what the conversation actually does. |
| 3 | What you build—and what comes with it | Four compact groups: product context and content standards; sources and AI behavior; scenarios/checks and ownership; guided skills, local lessons, templates, fictional example and overview viewer. | Recognize useful outputs and included support. |
| 4 | Build quality checks into the system | Rules connect to scenarios and checks. Run literal checks on saved responses, then use human review for meaning and judgment. Show a small rule → scenario → check example. | Understand evaluations are part of the workflow and results have limits. |
| 5 | Bring your coding agent | Claude Code, GitHub Copilot in VS Code, Codex; explain ChatGPT and other agents with precise setup/verification boundaries. Link to compatibility/setup documentation. | Find the relevant setup path. |
| 6 | Start with one product task | Repeat the same GitHub CTA; optional clone helper and one copyable first prompt. Short prerequisites and prototype note. | Open or clone the repo and begin. |

The three-step summary groups the seven stages; it does not replace them. A small
supporting line can name the full path: product → content → sources → behavior →
quality → improvement → maintenance. The snapshot viewer is an included companion,
while the conversation happens in the user's agent.

Draft evaluations copy: **Define good before you judge the output.** Connect your
rules to realistic situations and quality checks. Try saved responses, inspect
literal results and review the questions that need human judgment. Keep the
evidence with your system as it changes.

Use a caption such as **Illustrative connection—not an executed result** for a
diagram. No green “passed” badge unless tied to a real recorded run. No claims of
automatic semantic scoring, continuous monitoring or production coverage.

## Chat preview specification

Initial recommendation: a static, readable three-frame image/storyboard with the
same transcript available as page text. An optional short recording can follow
after a representative real session exists. Never present a mock as recorded use.

Suggested fictional storyboard (not a claim of an observed transcript):

1. Designer: “I have a style guide, but I'm not sure how to turn it into guidance
   for our support assistant.” Fievel: “Let's start with one task. What should the
   assistant help someone do?” Caption: **Start with your product and standards.**
2. Designer: “Help guests change a booking. It should ask when details are missing.”
   Fievel: “Let's draft that behavior, then link your approved change policy when
   you provide it.” Show a draft rule with source still needed. Caption:
   **Turn decisions into connected, reviewable files.**
3. Fievel: “How should we check it when the booking details are incomplete?” Show
   a scenario and a pending human question, then a small actual-viewer thumbnail.
   Caption: **Define checks and see how your system connects.**

Label the complete mock **Illustrative Fievel conversation · fictional example**.
Show conversation and artifacts distinctly. No fake live input, typing surface,
platform endorsement or fabricated approvals. Use generic chat framing rather than
copying a host's UI. Record an actual beginner/existing-guidelines session later,
verify behavior against the script, redact private data, and replace mock media
only when the evidence is real. Preserve legibility on narrow screens.

If motion is selected later: prefer a controlled short video or frame sequence
over an endlessly looping GIF; static poster, play/pause/replay, no autoplay audio,
reduced-motion fallback and text equivalent. Set an initial media budget of 1 MB
and validate legibility before optimizing to that proposed budget.

## Compatibility wording

Draft heading: **Use the agent you already work with.**
Draft supporting text: **Repository instructions and skills are supplied for
Codex, Claude Code and GitHub Copilot in VS Code. Open the repo in your agent and
follow the setup guide. Fresh-session workflows are still being validated.**

Use product names as text initially. Avoid partner/verified logos or a universal
“works everywhere” badge. [Compatibility evidence](../COMPATIBILITY.md) is the
authority for Fievel-specific testing.

| Requested name | Planned treatment before stronger evidence |
|---|---|
| Claude | Specify Claude Code; adapter supplied, end-to-end workflow pending. |
| GitHub Copilot | Specify VS Code environment; instructions/skills supplied, workflow pending. |
| Codex | Name supported repository mechanism; local engineering/catalog evidence only, fresh-session journey pending. |
| ChatGPT | Mention with a clear setup note: ordinary chat does not automatically load the cloned repo. Confirm a repository-capable environment or package/install path and test it before offering a separate “Start in ChatGPT” CTA. |
| More agents | “Other agents that can read and work with repository files may use the instructions; setup varies.” Link to manual entry prompt; no untested host badge list. |

## CTA and getting-started behavior

One dominant destination: the real GitHub repository. Repeat its label/destination
at the final section; do not introduce a competing signup action. Use anchor links
for navigation even when styled as a primary CTA. A clone helper copies a verified
HTTPS `git clone` command and confirms success accessibly; provide manual select/
copy if clipboard access fails. A click on the repo link opens GitHub, not an
automatic clone. No speculative custom protocol handlers.

First prompt: **Read AGENTS.md and start Fievel. I'm new to AI content systems.**
Alternative path: bring existing guidelines, without forcing a fictional tutorial.
Explain briefly that an agent account/access is separate. Local CLI commands use
Python 3.10+ and dependencies; link to README instructions rather than imply a
zero-setup browser app. Confirm a public repository URL and README anchors before
replacing planning placeholders. No fake link should ship.

## Visual and interaction direction

**Superseded palette proposal:** the user rejected the green viewer palette and
decorative branding in I-06. Use the revised neutral viewer as the starting point
for a later design review; the historical colors below are not approved for use.


Continue the actual viewer's visual language: warm background `#f5f6f1`, white
surfaces, forest text `#263d31`, primary green `#31583e`, muted text `#617065`, border
`#dde4da`. Serif display headings, system-font body, generous spacing, restrained
rounded surfaces. These are existing tokens, not newly user-tested branding.

One centered column with a wide hero/demo pairing on desktop; stack in meaningful
reading order on mobile. Short navigation: How it works, Evaluations, GitHub.
Limit card grids and decorative badges; use diagrams only to clarify connections.
Consistent CTA treatment and visible focus. Check contrast, 200% zoom, 320px
reflow, keyboard order, link names and media alternatives. No motion required to
understand the product, external fonts, mandatory trackers or live chat backend.

## Requirements and acceptance

| ID | Requirement | Planned acceptance evidence |
|---|---|---|
| LP-01 | Outcome and audience clear before feature detail | Intended visitors can paraphrase what they would build after viewing the hero. |
| LP-02 | Short one-page structure and clear GitHub route | Content review against word budget; working hero/footer links and clone fallback. |
| LP-03 | Included capabilities and guided process faithful to repo | Trace each claim to README/WORKFLOW or shipped files; no blanket completeness promise. |
| LP-04 | Representative chat preview | Labeled mock plus text equivalent, or provenance for a real recording; readable mobile frames. |
| LP-05 | Evaluations explained as embedded | Visitors distinguish definitions, executed literal checks and human review. |
| LP-06 | Compatibility precise | Each named environment has setup link/evidence label; unsupported one-click ChatGPT claim absent. |
| LP-07 | Consistent, accessible visual experience | Token review; browser/keyboard/reflow/contrast/media checks; independent review recorded separately. |
| LP-08 | Public destinations and deployment verified | Confirm repo URL/visibility/license, README anchors, hosting/base path and owner before launch. |

## Subsequent execution plan

1. Review this content/claims plan. Resolve public repo destination, hosting/owner,
   compatibility scope and static versus recorded demo. These do not block planning.
2. Refine copy and create one page layout with the approved content hierarchy.
   Keep page assets separate from the local project viewer. Do not add a framework
   or hosting dependency without a concrete need; choose implementation then.
3. Produce the labeled demo and validate text/artifacts against actual Fievel
   behavior. A real recording requires a real session, not a scripted success claim.
4. Implement one static responsive page in a later authorized increment. Test
   links, clone copy/fallback, motion controls if any, mobile, keyboard and budgets.
5. Observe 3–5 intended visitors as a small formative round (proposed, not run):
   explain Fievel, find what is included, describe evaluations, choose an agent,
   reach setup and explain the next step. Record confusion and revise; this sample
   does not establish conversion rates or general usability.
6. Recheck claims and destinations, review the concrete page, then publish only
   when deployment is authorized. No analytics collection is part of this plan.

## Unresolved decisions

Public repository owner/URL and visibility; hosting destination and domain;
representative user/session access for demo and comprehension checks; independently
verified host journeys; broader ChatGPT distribution path. No numerical benefit,
production readiness or “covers everything” claim is supported at this stage.


## Execution update — I-09

User authorized implementation and specified future GitHub Pages hosting. They
corrected the destination to `https://github.com/jeremydhoover-blip/fievel-content-system`.
Implemented a buildless page in `website/dist/`, a labeled static chat storyboard,
neutral visual styling, GitHub/clone controls and a manual-only Pages workflow.
[Implementation evidence](evidence/landing-page-01/RESULTS.md) records local checks.
No push, Pages configuration change or deployment was performed. Intended-visitor
comprehension, independent accessibility and real host/demo sessions remain open.


## Revision planning after user review

The user requested a new plan and confirmation before executing further changes.
The [second revision plan](LANDING-PAGE-REVISION-02.md) supersedes earlier copy,
eyebrow styling, abstract map and static conversation direction. It records the
writing rules, draft copy, logical example map, animated conversation storyboard
and individual section compositions. The live page remains the first iteration.


## Confirmed revision execution

The user confirmed the second revision plan. Implementation and verification are
recorded in [the revision results](evidence/landing-page-02/RESULTS.md). Earlier
planning-only statements are historical and superseded for this increment.
