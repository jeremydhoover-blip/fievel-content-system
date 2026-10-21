# Fievel visual redesign plan

Status: implementation authorized and locally verified
Date: 2026-10-21
Scope: website/dist landing page

## Problem

Recent revisions applied accent colors piecemeal, then removed most colored
surfaces after feedback. The result lacks a coherent palette and visual depth.
Tiny terracotta outlines cannot carry the entire visual identity. The next pass
must treat color, gradients, contrast and elevation together across the page.
This plan supersedes the contradictory palette experiments in DESIGN-GUIDE.md.
The proposal was authorized and implemented after this planning step.

## Proposed palette

| Role | Color | Use |
|---|---|---|
| Canvas | #FAF7F3 | Warm off-white page background |
| Paper | #FFFFFF | Reading panels and graph nodes |
| Ink | #24201E | Headlines and primary text |
| Supporting text | #665A54 | Secondary text on light surfaces |
| Terracotta | #BF765B | Broad decorative color and surface gradients |
| Deep terracotta | #984832 | Primary actions with white labels |
| Peach clay | #E8B79D | Lighter gradient end and supporting surfaces |
| Pale clay | #F4E2D7 | Selected panels and chat chrome |
| Warm border | #D7C5BA | Panel separation |
| Dark earth | #30231F | Evaluation background |

These are proposed values. Verify text contrast on the actual gradients and
states before finalizing. Mid-tone terracotta is a surface color, not a default
small-text color. Selection also uses borders, weight and aria state.

## Visual approach

Make terracotta visible in meaningful areas of the page. Alternate open neutral
space with colored visual components. Use broad, soft gradients rather than
painting every card beige. White reading surfaces should sit clearly above the
colored backdrop. Keep typography and existing content intact.

## Section treatments

| Area | Proposed treatment |
|---|---|
| Header | Warm-white background, dark wordmark, restrained terracotta link feedback |
| Hero | Broad peach-to-transparent radial gradient behind the graph, fading into the canvas rather than washing over the text |
| Hero actions | Deep terracotta primary button with white label and subtle warm shadow; plain dark secondary link |
| Relationship map | Visible pale-clay-to-peach diagonal panel gradient, white nodes and warm connecting lines; selected node gets pale-clay fill and deep terracotta border |
| Graph detail | White inset reading panel with warm border; explanation stays visually quieter |
| Conversation | White chat body inside a warm bordered frame; pale-clay header and footer; user bubbles use peach-clay fill with dark text; agent bubbles stay white |
| Included topics | Open canvas, deep terracotta numbers, warm dividers; expanded topic gets a very light clay surface |
| Evaluations | Dark-earth-to-deep-terracotta diagonal gradient; translucent light node surfaces, clear light text and visible branching connectors |
| Agent choices | White raised options; selected option has a pale-clay surface and terracotta border; accompanying detail panel uses a faint warm gradient |
| Getting started | Neutral reading area, pale-clay step markers, white command fields; copy controls stay distinct from primary actions |
| Footer | Quiet warm neutral surface and divider |

## Gradients

Use three related treatments with different jobs:

- Hero atmosphere: radial gradient from #E8B79D at roughly 35 percent opacity
  into transparent, located behind the graph.
- Light component surface: linear gradient at 135 degrees from #FAF0E9 to
  #E8B79D. Keep white graph nodes above it so relationships remain legible.
- Evaluation band: linear gradient at 120 degrees from #30231F to #854A38.
  Validate the light labels against the brighter end as well as the darker end.

Avoid unrelated purple or green hues, glow effects, and gradients on body text.

## Shadows and hierarchy

- Major visual panels: 0 20px 48px rgba(75, 40, 27, .12), plus a subtle border.
- Graph nodes: 0 3px 8px rgba(75, 40, 27, .10).
- Interactive cards: 0 4px 12px rgba(75, 40, 27, .06), slightly deeper on hover.
- Primary action: 0 5px 12px rgba(152, 72, 50, .18).
- Reading text, topic rows and ordinary links need no shadow.

Depth must identify grouping and interaction. Avoid giving every element the
same floating-card treatment. Preserve existing reduced-motion behavior.

## Implementation sequence after review

1. Preserve current assets as baseline evidence.
2. Consolidate palette and elevation tokens. Remove superseded color overrides
   rather than appending another conflicting patch.
3. Apply the hero and graph direction first, including gradients and selected states.
4. Carry the same palette through chat, evaluation, agent selection and setup.
5. Inspect full-page desktop and mobile screenshots together for overall balance.
6. Verify text contrast, hover, focus, selection, playback, copy fallback,
   reduced motion, no-JS reading and page overflow at existing five test widths.
7. Record observed results and any departures from this plan before handing back
   the local file preview. Keep publishing separate.

## Review decision

Proposed direction: visible terracotta and peach surfaces, warm gradients,
white reading panels, dark-earth contrast and selective warm shadows.
Next action: user reviews the implemented local preview.
