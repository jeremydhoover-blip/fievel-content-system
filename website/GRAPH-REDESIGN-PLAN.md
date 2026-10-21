# Fievel graph correction plan

Status: proposed for review
Date: 2026-10-21
Scope: hero relationship graph

## Evidence and problem

The user-supplied screenshot shows clipped right-hand nodes and labels, a dominant
horizontal scrollbar, a heavy beige gradient, repeated brown outlines and shadows
on every oval. Earlier browser checks accepted local scrolling by design. Those
checks did not establish that the composition looked good or fit the intended use.
The current graph is rejected. Passing interaction checks does not override that.

## Intended result

Show the seven entities and their actual relationships in a readable composition.
The diagram should feel like part of the site, not a framed flowchart pasted into
it. Keep the surrounding site palette question separate from this focused repair.

## Layout

- Stop placing the full diagram inside a narrow hero column. Put the interactive
  graph below the hero copy in a full-width composition within the existing wrapper.
- Desktop: arrange product context, knowledge sources and governance in the upper
  row; content standards, AI behavior and instructions and skills in the middle;
  evaluations below AI behavior. Preserve existing relationship directions.
- Fit every node and label inside the available area. Use compact rounded
  rectangles with enough width for Instructions and skills, replacing the ovals.
- Below 760px: switch to a vertical relationship view using the same underlying
  entities and edges. Show source, relationship and target in readable rows, with
  shared selection and explanation. This is a deliberate compact diagram view,
  not a horizontally clipped desktop canvas or an unconnected entity list.
- No horizontal scrolling for this component at the five supported test widths.
  Avoid shrinking the desktop SVG until labels become unreadable.

## Color and depth

- White diagram surface with a quiet neutral border. Remove the beige panel wash
  and individual node shadows.
- Neutral node borders and dark labels. Use a solid terracotta selection marker
  plus a restrained tinted selected surface, rather than brown outlines everywhere.
- Terracotta can remain visible in the surrounding site and primary actions.
  This correction does not remove the palette from the page.
- At most one subtle shadow on the overall diagram container. Keep edges flat.
- Use thin neutral connectors; make only the selected entity's incident edges
  terracotta. Use matching arrowheads so gray arrows do not terminate brown lines.
- Keep relationship labels dark enough to read on white, away from lines and nodes.

## Detail and interaction

- Keep one explanation area below the diagram, separated by spacing and a divider.
  Remove the nested rounded white card.
- Preserve button semantics, visible keyboard focus, selected state and actual
  incident-edge highlighting. Selection works by pointer, keyboard and touch.
- Do not rely on color alone. Selected nodes have a clear marker and stronger label.
- Preserve all seven entities and seven declared relationships. Add no invented links.
- Keep the existing always-visible explanation of the model concise and readable.

## Execution and verification after review

1. Save the current HTML, CSS and JavaScript as baseline evidence.
2. Update structure and responsive graph layout together. Remove obsolete graph
   styling instead of adding another contradictory override layer.
3. Inspect screenshots at 1440, 1024, 768, 390 and 320px. Verify no clipped labels,
   diagram overflow, crossing labels or tiny text. Inspect desktop and mobile at
   actual reading size, including selected and keyboard-focus states.
4. Update browser assertions to reject graph overflow and confirm each entity and
   relationship is available in the responsive presentation. Earlier assertions
   that require a scrollable desktop graph on mobile must change deliberately.
5. Verify selection synchronization, explanation text, arrow direction, contrast,
   no-JS reading and reduced motion. Recheck existing page interactions.
6. Record technical results separately from user visual acceptance. Open the same
   local index.html for review without creating extra preview tabs unnecessarily.

## Decision and next action

This proposes replacing the narrow scrollable oval graph with a full-width desktop
diagram and a readable compact relationship view. Site assets remain unchanged.
Next action: user reviews this correction before implementation.
