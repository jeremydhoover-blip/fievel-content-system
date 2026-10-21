# Fievel site design guide

Maintained 2026-10-21. Scope is the public landing page in website/dist.
This records the current foundation and the next visual-depth pass. The first color-depth draft is implemented locally for user review and is not approved branding.

## Purpose

Explain Fievel and help someone start their content system in their own agent.
Show how the parts connect and what the guided experience feels like. Use the
content-system model rather than a domain-specific booking example. The companion
dashboard visualizes saved work; it is separate from the guided conversation.

## Writing

- No eyebrow text above headings.
- No punctuation in titles or headings, including metadata titles.
- No em dashes in prose.
- Use Fievel consistently. Prefer direct descriptions of actions and outcomes.
- Keep each section to one clear job and avoid repeated heading/subheading stacks.
- Keep filenames and implementation details out of marketing explanations unless
  needed for setup. Preserve valid command and URL syntax.
- Explain actual capabilities without invented results, endorsements or host tests.
- Graph labels describe relationships. Do not turn the ontology into numbered steps.
- Use numbers for setup steps. Use expandable detail when there is useful depth.

## Current colors

| Token | Value | Role |
|---|---|---|
| --bg | #f6f6f7 | Page background |
| --paper | #ffffff | Primary panels and input surfaces |
| --ink | #24252a | Main text |
| --muted | #62646c | Supporting text |
| --line | #dedee3 | Dividers and neutral borders |
| --soft | #ebebf0 | Selected and supporting surfaces |
| --dark | #252631 | Primary CTA and evaluation band |
| Focus accent | #64618b | Visible keyboard focus |

The green palette was rejected. Keep the neutral base. Color must not be the only
way to convey selection, state or a relationship. Check contrast on actual paired
surfaces, including hover and focus states, before adding new colors.

## Typography and spacing

System sans serif throughout. System monospace only for commands and small step
numbers. No remote font requirement. Headings generally use weight 600, body 400.
Current desktop hero scales to 60px, section headings 38px, body 14 to 17px.
Small labels use 11 to 13px. Avoid further shrinking essential reading text.
Mobile hero is 40px and section headings 33px; verify wrapping at 320px.

The desktop content width is capped at 1160px. Use the existing 8px-based rhythm
with 12, 16, 24 and 32px internal gaps. Section spacing is typically 64px desktop
and 48px mobile. Avoid reserved minimum height for short descriptive paragraphs.
Use a divider only when it separates meaningful groups, not around a lone link.

## Components

- Hero CTAs are Get started and Learn more. Both navigate to sections; neither
  starts playback. Learn more has a downward arrow.
- Graph uses connected elliptical bubbles with directional arrows and readable
  relationship labels. Preserve the graph on narrow screens with local scrolling.
  Selection exposes its explanation and highlights actual incident connections.
- Chat has one control for play, pause, resume and play again. The greeting is
  visible initially. Do not autoplay the conversation on scroll.
- Setup topics have numbered expandable summaries. Detailed content earns its space.
- Evaluations use a branching flow for literal checks and human review, with no
  invented success state. Keep explanation short and visible.
- Agent choices retain selected borders and show setup details.
- Getting started is five numbered steps. Clone is fourth; prompt is fifth.
  The full instructions link belongs below the prompt, not between standalone rules.

## Motion and interaction

| Behavior | Timing | Boundaries |
|---|---|---|
| Hover and press feedback | 160ms | Lift controls 1 to 2px on fine pointers only |
| Arrow and underline feedback | 240ms | Small directional cue without changing layout |
| Section and disclosure entrance | 420ms | At most 10px vertical travel, no repeat on scrolling back |
| Graph connection highlight | 160ms | Only edges belonging to the focused or selected entity |
| Chat | Existing controlled timeline | Explicit play, cancellable timers, pause and replay |

Shared easing is cubic-bezier(.2,.7,.2,1). No bouncing, parallax, cursor followers,
continuous decorative loops or scroll hijacking. Hover feedback must not imply
that a static diagram element is an executable action. Keyboard users receive
visible focus and graph highlighting. Touch does not depend on hover.

Respect prefers-reduced-motion on initial load and when changed. Cancel active
decorative animations and remove movement transitions. Keep all content visible
without JavaScript or animation support. Section entrances never set a persistent
hidden state. The chat has its existing static reduced-motion fallback.

Motion choices build on the inspected [W3C motion guidance](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html)
and [playback guidance](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html).
These references do not establish usability or accessibility certification.

## Next visual depth pass

Sequence requested by the user: first motion and interactions, then layered color
and visual depth. The following is a proposed next increment, not a completed one.

1. Consolidate the accumulated CSS into a single token and component structure
   before introducing new surface treatments. Preserve the tested layouts.
2. Develop three surface levels: neutral page, subtle tinted section, raised
   interactive panel. Use tonal contrast to group content rather than add cards.
3. Explore a restrained cool violet tint derived from the existing focus accent.
   Compare it with a purely neutral treatment before settling the palette.
4. Give the ontology stronger depth through node surfaces and line hierarchy,
   retaining readable labels and the same semantic relationships.
5. Refine the chat and evaluation visualizations as related components. Use modest
   border and shadow changes rather than decorative illustrations or glow effects.
6. Review screenshots at actual reading size across desktop and mobile. Record
   token changes, contrast checks and the user's chosen direction in this file.

## Verification

Use tests/browser_landing.cjs for meaningful interaction and layout checks.
Inspect hover, focus, selected and reduced-motion states visually. Verify copy
controls, graph keyboard selection, the single playback control and no-JS reading.
Check that entrance animations do not hide content or introduce page overflow.
Save evidence for material design passes; do not infer visitor comprehension from
automated tests. Keep publication separate from local design work.


## Local visual depth draft

2026-10-21. Implemented the next pass as a reviewable local draft. Shared color,
shadow and motion tokens now live in one foundation block. Neutral canvas remains
#f6f6f7; --tint #f0eff7 groups supporting surfaces, --tint-strong #e5e2f1 marks
selected nodes and user messages, and --line-accent #c4bfd8 separates raised panels.
The existing focus accent #64618b now also identifies selection. The dark evaluation
band transitions from #252631 to #343146. Graph nodes, chat and agent choices use
restrained shadows. Layout, content and playback behavior are preserved.

The earlier next-pass list records the proposal; this implements its first visual
iteration. Full removal of obsolete component CSS remains future maintenance.
User palette selection remains open. Desktop screenshot inspected; automated
checks cover five widths and reduced motion. Contrast measurements and screenshots
are in docs/experience/evidence/landing-depth-01. No accessibility certification
or visitor comprehension is inferred.


## Palette direction chosen by the user

2026-10-21. Black, white and terracotta supersede the violet exploration above.
The local site uses near-black #202020 text, white #ffffff panels, warm-white
#faf8f6 canvas and terracotta #9b4934 for focus and selection. Supporting surfaces
use #f8eee8 and #efd5c7 with #d8b6a4 borders. The evaluation band uses black with
a subtle warm dark transition. This is the current palette direction.


## Palette refinement after visual feedback

2026-10-21. User rejected the beige graph and chat treatment. Supersedes the warm
surface values above. Use white panels, neutral gray borders and pale gray chat
chrome. Remove the hero tint. Selected graph nodes remain white with terracotta
outlines; chat user bubbles use pale gray. Terracotta remains a restrained focus,
selection and numbering accent. Visual approval remains open.


## Stronger terracotta draft

2026-10-21. Further color feedback calls for a more deliberate accent. Use burnt
terracotta #ad432c on primary actions with white text and #913622 on hover.
Keep white graph nodes with terracotta selection outlines and selected text.
Agent selection uses a terracotta top inset. Chat remains neutral gray and white;
the evaluation band is solid near-black. This draft awaits visual review.


## Softer clay direction

2026-10-21. User rejected the burnt red treatment. Supersedes the preceding draft:
clay terracotta #b8735a for selected outlines and small decorative details, black
primary buttons, white surfaces, neutral body text. Use darker #874b38 for keyboard
focus visibility. No terracotta background wash or red primary actions. User
visual acceptance remains pending.


## Visual redesign planning reset

2026-10-21. User requested a documented plan before further changes.
VISUAL-REDESIGN-PLAN.md is the current proposed direction and supersedes the
contradictory palette trials above. Site implementation is paused for review.
The plan calls for visible terracotta surfaces, gradients and selective shadows,
rather than an almost entirely black and white page.


## Implemented terracotta surface system

2026-10-21. User authorized VISUAL-REDESIGN-PLAN.md. Implemented its full palette,
hero atmosphere, graph gradient, peach chat treatments, dark-earth evaluation
gradient and selective warm shadows. Removed the previous three conflicting
surface override blocks and consolidated foundation tokens. This is the current
implemented direction and supersedes prior palette experiments. Screenshot and
browser evidence is in docs/experience/evidence/landing-terracotta-01.
User visual acceptance remains pending.


## Graph correction proposal

2026-10-21. The user rejected the implemented graph after inspecting its layout
and color treatment. GRAPH-REDESIGN-PLAN.md records the proposed correction.
It proposes full-width placement, compact rectangular nodes, neutral diagram
surfaces, selective terracotta and a compact relationship view on mobile.
This supersedes earlier graph acceptance assumptions, not the user's request
for a colored site. No site assets changed in this planning step.


## Scoped hero correction

2026-10-21. User clarified that only hero and graph styling needed correction.
Preserved all wording and layout. Removed hero cream wash, replaced brown CTA
with a brighter terracotta gradient, reduced graph tint and border weight,
removed node shadows and removed the white explanation-card fill. All other
sections retain their existing treatments. Earlier full-width graph restructuring
proposal is not part of this scoped correction. Browser evidence: .scratch/hero-refinement.


User correction: node shadows were a positive part of the design. Restored the
previous node drop shadow. Preserve node shadows in subsequent refinements.
