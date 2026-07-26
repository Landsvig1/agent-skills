---
name: excalidraw
description: >
  Excalidraw JSON format reference and generation patterns for workflow diagrams.
  Trigger when: asked to create a flowchart, process map, decision tree, swim lane,
  or any workflow/process diagram as an Excalidraw file.
  Do NOT trigger when: the task is code generation, text writing, or non-diagram work.
---

# Excalidraw Diagram Generation

You generate valid `.excalidraw` JSON files. The output opens directly in
excalidraw.com, the VS Code Excalidraw extension, or Obsidian Excalidraw.

## File structure

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "claude-code",
  "elements": [],
  "appState": {
    "viewBackgroundColor": "#ffffff",
    "gridSize": 20
  },
  "files": {}
}
```

All diagram content goes in `elements`. Each element needs a unique `id` —
use short alphanumeric strings (8 chars, e.g. `"aB3kQ9xZ"`). Generate a
different id for every element.

## Element types

### Shared properties (all elements)

```json
{
  "id": "aB3kQ9xZ",
  "type": "rectangle",
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 80,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "roundness": { "type": 3 },
  "seed": 12345,
  "version": 1,
  "versionNonce": 1,
  "isDeleted": false,
  "boundElements": null,
  "updated": 1700000000000,
  "link": null,
  "locked": false,
  "groupIds": []
}
```

Generate a random integer for `seed` (1–999999). Set `updated` to current
Unix timestamp in milliseconds.

### Rectangle

Use for process steps, actions, and containers.

```json
{ "type": "rectangle", "roundness": { "type": 3 } }
```

### Ellipse

Use for start/end nodes.

```json
{ "type": "ellipse", "roundness": { "type": 2 } }
```

### Diamond

Use for decision points (yes/no, if/else).

```json
{ "type": "diamond", "roundness": { "type": 2 } }
```

### Text

Standalone text for annotations, titles, or arrow labels.

```json
{
  "type": "text",
  "text": "Your text here",
  "fontSize": 20,
  "fontFamily": 1,
  "textAlign": "center",
  "verticalAlign": "middle",
  "autoResize": true,
  "lineHeight": 1.25,
  "containerId": null,
  "originalText": "Your text here"
}
```

`fontFamily`: 1 = Virgil (hand-drawn), 2 = Helvetica, 3 = Cascadia (code).
Always use 1 for diagrams.

**Width/height for standalone text:** estimate `width ≈ text.length × fontSize × 0.6`
and `height ≈ fontSize × lineHeight × numberOfLines`.

### Arrow

Connects elements. Defined by `points` array (offsets from element x,y).

```json
{
  "type": "arrow",
  "points": [[0, 0], [200, 0]],
  "startArrowhead": null,
  "endArrowhead": "arrow",
  "startBinding": null,
  "endBinding": null,
  "elbowed": true,
  "fixedSegments": null
}
```

Set `elbowed: true` for right-angle connector lines (recommended for workflows).
Set `elbowed: false` for straight or curved arrows.

### Line

Like arrow but no arrowheads. Use for borders, dividers, swim lane separators.

```json
{
  "type": "line",
  "points": [[0, 0], [400, 0]],
  "startArrowhead": null,
  "endArrowhead": null
}
```

## CRITICAL: Labeling shapes (container binding)

**Excalidraw does NOT have a `label` property on shapes.** To put text inside a
shape, you must use container binding — a two-element pattern:

### Step 1: The shape declares its bound text

```json
{
  "id": "shape1",
  "type": "rectangle",
  "x": 100, "y": 100, "width": 200, "height": 80,
  "boundElements": [
    { "id": "text1", "type": "text" }
  ]
}
```

### Step 2: A text element references the container

```json
{
  "id": "text1",
  "type": "text",
  "x": 130, "y": 120,
  "width": 140, "height": 25,
  "text": "Process Step",
  "fontSize": 20,
  "fontFamily": 1,
  "textAlign": "center",
  "verticalAlign": "middle",
  "containerId": "shape1",
  "originalText": "Process Step",
  "autoResize": true,
  "lineHeight": 1.25
}
```

**Rules:**
- The text element's `containerId` must match the shape's `id`
- The shape's `boundElements` array must include `{ "id": "<text-id>", "type": "text" }`
- Excalidraw auto-centers the text on load, but set text x/y roughly centered
- Text width should be ≈ shape width minus 40px padding
- ALWAYS emit the shape BEFORE its bound text in the elements array

### Shapes that also have arrow bindings

When a shape has both a label AND arrows, its `boundElements` includes all of them:

```json
{
  "id": "shape1",
  "type": "rectangle",
  "boundElements": [
    { "id": "text1", "type": "text" },
    { "id": "arrow1", "type": "arrow" },
    { "id": "arrow2", "type": "arrow" }
  ]
}
```

## CRITICAL: Arrow bindings

To connect an arrow to shapes, use `startBinding` and `endBinding`:

```json
{
  "id": "arrow1",
  "type": "arrow",
  "x": 300, "y": 140,
  "width": 60, "height": 0,
  "points": [[0, 0], [60, 0]],
  "startBinding": {
    "elementId": "shape1",
    "focus": 0,
    "gap": 1,
    "fixedPoint": [1, 0.5]
  },
  "endBinding": {
    "elementId": "shape2",
    "focus": 0,
    "gap": 1,
    "fixedPoint": [0, 0.5]
  },
  "elbowed": true
}
```

### fixedPoint coordinates (normalized 0–1)

```
         [0.5, 0]        ← top center
            ↑
[0, 0.5] ← ■ → [1, 0.5]   left / right center
            ↓
         [0.5, 1]        ← bottom center
```

Common connection patterns:
- **Left to right flow:** start `[1, 0.5]` → end `[0, 0.5]`
- **Top to bottom flow:** start `[0.5, 1]` → end `[0.5, 0]`
- **Decision "Yes" (right):** start `[1, 0.5]` → end `[0, 0.5]`
- **Decision "No" (down):** start `[0.5, 1]` → end `[0.5, 0]`

### Arrow positioning

The arrow's `x,y` should be at the start connection point. The arrow's `width`
and `height` should match the total offset of `points`. For a horizontal arrow
going 200px right: `width: 200, height: 0, points: [[0,0],[200,0]]`.

**The target shape must also list the arrow in its `boundElements`.**

## Z-ordering

Elements render in array order (first = back, last = front). Emit elements in
this order for each node:

1. Shape (rectangle/ellipse/diamond)
2. Its bound text
3. Its outgoing arrows

This ensures text renders on top of shapes, and arrows on top of everything.

## Color palette

Use these pastel fills for visual distinction. Always pair with `strokeColor: "#1e1e1e"`.

| Role | backgroundColor | Use for |
|------|----------------|---------|
| Process step | `"#a5d8ff"` | Regular actions, tasks |
| Decision | `"#ffec99"` | Yes/no, if/else diamonds |
| Start/End | `"#b2f2bb"` | Terminal nodes (ellipses) |
| Error/Exception | `"#ffc9c9"` | Error states, failures |
| External system | `"#d0bfff"` | APIs, services, databases |
| Annotation | `"transparent"` | Notes, comments |

## Standard dimensions and spacing

### Element sizes

| Element | Width | Height |
|---------|-------|--------|
| Process box | 200 | 80 |
| Decision diamond | 160 | 160 |
| Start/End ellipse | 160 | 80 |
| Swim lane header | 200 | 50 |

### Spacing

| Between | Gap (px) |
|---------|----------|
| Nodes horizontally | 80 |
| Nodes vertically | 100 |
| Arrow to node edge | 1 (gap property) |
| Swim lane rows | 200 |

## Layout patterns

### Top-down flowchart (default)

Place start node at top. Each row is y += (node height + 100).
Decision diamonds branch: "Yes" goes right (+280, 0), "No" continues down (0, +260).

```
      [Start]           y=0
         ↓
    [Process A]         y=180
         ↓
    <Decision?>         y=360
     ↓        →
[Process B]  [Process C]
     ↓
     [End]
```

X positions: center column at x=200. Branch column at x=480.

### Left-to-right process

Place start node at left. Each column is x += (node width + 80).
All nodes share the same y coordinate.

```
[Start] → [Step 1] → [Step 2] → [Step 3] → [End]
  x=0      x=280      x=560      x=840     x=1120
```

### Swim lanes

Horizontal lanes separated by lines. Lane header on the left, process nodes
to the right. Each lane is 200px tall.

```
┌──────────┬──────────────────────────────────────┐
│  User    │  [Action A] → [Action B]             │  y=0
├──────────┼──────────────────────────────────────┤
│  System  │  [Process C] → [Process D]           │  y=200
├──────────┼──────────────────────────────────────┤
│  DB      │  [Query E] → [Store F]               │  y=400
└──────────┴──────────────────────────────────────┘
```

## Generation protocol

1. **Read the request.** Identify the process, its steps, decisions, and actors.
2. **Choose layout.** Top-down for flowcharts with decisions. Left-to-right for
   linear processes. Swim lanes when multiple actors are involved.
3. **Plan the grid.** Sketch x,y positions for each node before writing JSON.
   Use the standard dimensions and spacing above.
4. **Generate elements in order.** For each node: shape → bound text → outgoing arrows.
5. **Cross-check bindings.** Every arrow's `startBinding.elementId` and
   `endBinding.elementId` must appear in those shapes' `boundElements` arrays.
   Every text's `containerId` must match its shape's `boundElements`.
6. **Write the file.** Output valid JSON to the specified path.

## Decision branch labels

For "Yes/No" labels on arrows leaving a decision diamond, add standalone text
elements near the arrow midpoint:

```json
{
  "type": "text",
  "x": 320, "y": 420,
  "text": "Yes",
  "fontSize": 16,
  "fontFamily": 1,
  "textAlign": "center",
  "verticalAlign": "middle",
  "containerId": null,
  "originalText": "Yes"
}
```

Position "Yes" near the right-exit arrow and "No" near the down-exit arrow.

## Output conventions

- File extension: `.excalidraw`
- Write the `.excalidraw` file in the current project directory
- Also write a companion markdown describing what was generated and how to open it
- Name: `{task-slug}.excalidraw` — lowercase, hyphens, no spaces (e.g. `user-registration.excalidraw`)
