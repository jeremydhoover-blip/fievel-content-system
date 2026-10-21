# Landing page revision plan

Date 2026-10-21

Status superseded by the subsequent user correction

This plan responds to the user's review of the first landing page. The first
iteration is a foundation, not an accepted content or design direction. Keep the
current page intact until this revision plan is confirmed. No page code, graphics
or animation is changed in this planning increment.

## Writing rules

These are explicit user requirements for future Fievel writing and interface work.

- Never use eyebrow text above a heading.
- Never use punctuation in titles or headings. Use words instead of ampersands,
  slashes, decorative arrows, quotation marks or terminal punctuation in titles.
- Never use em dashes in writing.
- Use direct descriptions of the user's work and the resulting artifacts.
- Replace generic promotional claims with concrete examples and useful outcomes.

Ordinary punctuation remains appropriate in body copy and dialogue. Essential
syntax in URLs, code, filenames and commands is preserved. Entity type labels,
edge labels and visible control names must identify real information or behavior;
do not recreate eyebrow text under another CSS class. The rules apply to the page
title metadata as well as visible headings. Existing historical evidence remains
unchanged.

## What the first iteration needs to fix

| Feedback | Revision decision | Review evidence |
|---|---|---|
| Copy does not sound right | Rewrite the page around a content designer's actual decisions and deliverables | Draft copy below for approval before layout implementation |
| Graph is not logical | Replace category sequence with one concrete example and explicitly named relationships | Entity and edge model below; every connector explainable in a sentence |
| Conversation is a static wall | Animate a short exchange with typing dots and gradual reveals | Timed storyboard and playback contract below |
| Foundation section is generic | Show an inspectable miniature content-system artifact | Concrete standards, behavior, evidence and check samples |
| Evaluations need stronger content and design | Show a rule becoming a scenario and a review question, separate from results | Consistent example and truthful state labels |
| Sections lack a designed experience | Give each section a distinct composition and role within one visual system | Section-specific art direction and interactions below |
| Setup and agent concepts work | Preserve their purpose while revising copy and presentation | Clear repo route and working copy controls |

## Content direction for review

These are proposed words, not an attempt to infer the user's complete house style.
Target 450 to 600 words excluding dialogue, controls and setup commands. Avoid
repeating the same pitch in several sections. Keep one main GitHub destination.

| Section | Proposed heading | Proposed supporting copy |
|---|---|---|
| Hero | Build the content system behind your AI experience | Bring your product knowledge and writing guidance. Fievel helps you turn them into content standards, AI behavior and quality checks you can inspect and maintain. |
| Guided process | Work through it with Fievel | Start with one task or an existing style guide. Fievel asks focused questions, helps you make decisions and saves the system in your repository. |
| Foundation | See what your system is made of | Keep your product context, writing rules, sources and AI behavior connected. Add scenarios and checks, then use the dashboard to explore what you have created. |
| Evaluations | Make quality part of the system | Decide what a good response should do. Connect each rule to a realistic situation and a check. Try saved responses and review the questions that need human judgment. |
| Agents | Use your coding agent | Fievel supplies repository instructions and skills for Claude Code, GitHub Copilot in VS Code and Codex. Follow the setup guidance for your environment. |
| Setup | Start with one product task | Clone the repository, open it in your agent and tell Fievel what you are building. Bring your own guidelines or explore the fictional example. |

Primary CTA stays **Get Fievel on GitHub**. Secondary hero CTA **Watch the example**
scrolls to the demonstration and starts it only after that explicit activation.
Keep early prototype status and compatibility caveats near the relevant details,
without turning them into heading decorations. No claim that every host workflow
has been verified. Ordinary ChatGPT chat does not automatically load the repo.

## A map with a clear meaning

The hero should answer one question: how does a piece of guidance become something
you can check? Show one fictional booking example, not an abstract product
architecture or numbered workflow. Four entities are enough.

| Entity | Example content | Meaning |
|---|---|---|
| Source | Booking change policy | An explicitly fictional policy with the passage “A change request needs the booking reference and preferred date” |
| Rule | Ask for missing booking details | A draft AI behavior interpretation linked to that source |
| Scenario | A guest asks to change a booking without providing details | A realistic situation in which the rule matters |
| Check | Does the response ask for the missing reference and date | A human review question that assesses the rule in that scenario |

Use this edge model, not a chain with invented dependency or execution meaning.

| From | Relationship label | To |
|---|---|---|
| Source | Informs | Rule |
| Check | Assesses | Rule |
| Scenario | Provides context for | Check |

Desktop composition: source and rule on the upper row, scenario and check on the
lower row. Source points to rule. Scenario points to check. Check points upward
to rule. Place relationship labels beside the actual connectors. No step numbers,
anonymous branching lines or arrows that suggest the source produces a scenario.

Selecting an entity reveals a short detail beneath the diagram: the source
passage, rule wording/status, scenario text or review question/method. Each node
is a keyboard-operable button; retain a meaningful reading order and a text
relationship description. On mobile, use a compact vertical layout with the same
three labeled relationships, not a tiny scaled desktop drawing. Support no-JS
reading through the static description.

Label the whole example as fictional in a figure caption, not as an eyebrow.
The diagram does not claim actual executed results or verified policy grounding.
The source passage is an authored illustration. Real package links in the current
schema record source IDs, not exact supporting passages, so this explanatory
view must not imply that passage-level provenance already exists in the product.

## Conversation storyboard

Use the same booking example so visitors do not have to learn a second domain.
Proposed transcript with three messages from each side follows.

1. Designer: “I'm building a support assistant for booking changes.”
2. Fievel: “What should it do when a guest leaves out the booking details?”
3. Designer: “Ask for the booking reference and the date they want.”
4. Fievel: “I'll draft that behavior. Do you have a policy we can link it to?”
5. Designer: “Yes, our change policy lists both as required.”
6. Fievel: “We'll link it and keep the rule as a draft. Next, let's define how to check it.”

This is an illustrative script for approval, not a transcript or evidence that an
agent followed it. Side artifact shows the draft rule and a pending check, never
an approved source or successful run. Selecting the illustrated policy is a
storyboard event, not a real file upload or live agent interaction.

Playback treatment: a fixed-height chat viewport with message entrance and brief
three-dot typing indicator before Fievel replies. Show complete message text when
revealed rather than slow character-by-character typing. Keep two or three recent
messages visible so the example reads as a conversation rather than a transcript
laid out in full. Move the internal viewport only, never the page.

Proposed timing: 1 to 1.5 seconds for each typing indicator and 3 to 4 seconds of
reading time after each reply. Target 20 to 25 seconds total, subject to legibility
review. Play once, end on a readable final state, and offer replay. No endless
automatic looping. Pause freezes message and dot timers; resume continues without
skipping. Provide Play, Pause, Replay and Read transcript controls with accurate
labels and keyboard support. Do not announce every typing dot to screen readers.

Recommended format: HTML/CSS/JS animation with a GIF-like presentation. It keeps
text crisp at every width and permits playback controls. This is a recommendation
for confirmation, not a silent substitution for the requested moving example. An
actual GIF export can be an additional shareable asset later, but is not required
for the page to convey the experience.

When reduced motion is requested, show the finished static conversation and
transcript with no typing or motion. Without JavaScript, show a readable static
fallback. Avoid initiating motion merely because the section enters the viewport.

## Section specific design

Keep the accepted neutral palette as the base, with strong typography, deliberate
spacing and restrained surface contrast. Do not add a new decorative logo. The
site's wordmark can remain a plain text home link. No eyebrows anywhere.

| Section | Composition | Useful behavior |
|---|---|---|
| Hero | Large direct heading and short copy beside a legible relationship map | Select entities to inspect the example; watch CTA leads to the demo |
| Guided process | Animated chat as the main visual, with a small synchronized artifact beside it on desktop | Playback controls; draft rule appears at the relevant message; transcript available |
| Foundation | A miniature system explorer, not four generic marketing cards | Three tabs named Standards, Behavior and Checks reveal a short concrete artifact; source and product context remain visible alongside |
| Evaluations | One comparison surface with rule, scenario and review question, plus a visually separate result area | Select Defined or Example result; authored result marked fictional and human review stays pending |
| Agents | Compact environment strip with equal visual weight and setup detail underneath | Select a host to reveal its existing setup path and evidence boundary; no invented installation command |
| Setup | Two-step command and first-prompt panel beside one final GitHub CTA | Existing copy buttons with accessible status and manual-copy fallback |

The foundation's tabs should show actual illustrative fields and short wording,
not long JSON blocks. The evaluation example should demonstrate a literal check
separately from human judgment. If an example result is included, use the existing
authored fixture and explain its limits; do not manufacture a semantic pass or
imply the site executes evaluations. A static result disclosure is sufficient if
the comparison would make the page too long or busy.

All controls must reveal or operate meaningful content. No decorative tabs, fake
chat input, pretend uploads, redundant hover animation or scroll effects.

## Research and implications

The following primary documentation was inspected for this revision on 2026-10-21.
It informs accessibility and implementation choices, not the user's writing style
or proven marketing effectiveness.

| Source | Relevant observation | Adaptation |
|---|---|---|
| [W3C pause stop hide](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html) | Explains controls for qualifying automatic motion and auto-updating content | Visible playback controls; prefer explicit start; no unending loop |
| [W3C animation from interactions](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html) | Discusses disabling nonessential interaction animation and honoring motion preferences | Static reduced-motion state; no forced movement |
| [MDN matchMedia](https://developer.mozilla.org/en-US/docs/Web/API/Window/matchMedia) | Supports querying and monitoring media preferences in JavaScript | Keep playback behavior consistent with preference changes, not CSS alone |
| [W3C complex images](https://www.w3.org/WAI/tutorials/images/complex/) | Describes text alternatives for information-rich diagrams | Diagram and text relationship description convey the same model |

The original complex-images URL returned an error; the canonical complex path
above was inspected instead. No usability study or new host compatibility test
was performed. Product relationships come from WORKFLOW and the schema/renderer,
not an external graph library or a generic marketing diagram.

## Execution after confirmation

1. Preserve first-iteration assets and screenshots as a baseline. Implement only
   after the user confirms this plan, including copy and the animation approach.
2. Replace page copy and remove all eyebrow elements/styles. Add a content lint
   check for heading punctuation and em dashes, including metadata and generated
   demo labels. Keep command and URL syntax valid.
3. Implement the four-entity diagram and inspectable detail. Verify its edge
   directions against the model above before polishing appearance.
4. Implement the timed conversation and synchronized draft artifact. Test pause,
   resume, replay, transcript, no-JS and reduced-motion behavior explicitly.
5. Implement section compositions and meaningful controls. Keep the page short,
   reuse one example and avoid introducing dependencies without need.
6. Run browser checks at 320, 390, 768, 1024 and 1440 pixels. Verify keyboard access,
   diagram label legibility, tabs, focus, no overflow, copy fallback and Pages
   subpaths. Inspect screenshots at actual reading size. Record bundle weight.
7. Present the revised page for user review. Do not publish as part of this
   revision unless requested. Preserve current GitHub Pages and repo setup.

Acceptance questions: Can a visitor explain each map relationship? Can they tell
what the conversation saves? Can they distinguish a rule, a scenario, a defined
check and a result? Can they find their agent setup and clone the repo? Automated
checks do not substitute for observing people answer these questions.

## Confirmation requested

Confirm the proposed copy direction, the concrete four-entity map and the
controlled animated chat approach. These are the substantive decisions before
implementation. The user can revise any of them without approving the whole
plan. No production website files have been modified by this planning work.


## Implementation record

The user confirmed this plan with proceed. The revision is implemented locally.
See [results and preserved evidence](evidence/landing-page-02/RESULTS.md).
The prior confirmation and execution sections are retained as planning history.
No deployment was performed. The moving example uses controlled HTML animation
as proposed, not a binary GIF. User review of the resulting page remains open.


## Subsequent user correction

The user rejected the booking-based interpretation and instructed execution of
a Fievel-focused page. The map now explains the seven major concepts of a content
system and their relationships. The conversation introduces Fievel and guides
setup without a domain example or file artifact. The earlier four-entity model,
dialogue and artifact specifications are historical and superseded. See
[correction evidence](evidence/landing-page-03/RESULTS.md).
