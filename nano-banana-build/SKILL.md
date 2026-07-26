---
name: nano-banana-build
description: Generate and edit high-quality images using Gemini 2.5 Flash Image and Gemini 3 Pro Image (Nano Banana / Nano Banana 2). Make sure to use this skill whenever the user mentions generating images, product photography, graphic design, social media assets, ad creatives, image editing, style replication, visual DNA, character consistency across storyboards, outpainting, or resizing graphics, even if they don't explicitly name 'Nano Banana'.
---

# Nano Banana Image Generation & Editing Skill

This skill equips the agent with direct programmatic capabilities to generate images, extract design styles (Visual DNA), edit visual elements, and maintain character/subject consistency using Gemini's native image models (codename: Nano Banana).

## Quick Start (Deterministic Scripts)

The skill includes two pre-bundled scripts located in `scripts/`:

1. **`generate.py`**: High-performance image generator supporting text-to-image, editing, style references, aspect ratios, and search grounding.
2. **`extract_style.py`**: Visual DNA extractor using Gemini's multimodal window to extract style parameters from images into a structured JSON file.

### Commands

```bash
# Generate image from prompt
python3 scripts/generate.py "A minimal modern workspace with wood textures" -a 16:9 -o output.png

# Generate image with subject/style consistency
python3 scripts/generate.py "The same subject wearing a suit" -r base_ref.png style_ref.png -a 4:3 -o output.png

# Inpaint/Outpaint/Edit an image
python3 scripts/generate.py "Add a retro poster to the wall" -e base_image.png -o output_edited.png

# Extract visual DNA from an Instagram feed / set of references
python3 scripts/extract_style.py post1.png post2.png post3.png -o style_dna.json
```

---

## Core Generation Workflow

Always structure prompts and call configuration using the unified `google-genai` Python SDK pattern:

```python
from google import genai
from google.genai import types

client = genai.Client()

config = types.GenerateContentConfig(
    response_modalities=["IMAGE"],
    image_config=types.ImageConfig(
        aspect_ratio="16:9",
        image_size="1K" # Nano Banana supports 1K, Nano Banana 2 supports up to 4K
    )
)

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=["A futuristic city skyline at sunset"],
    config=config
)
```

---

## Workflow 1: Visual DNA Replication & Prompt Cloning
Replicating any visual style from reference images (such as an Instagram feed) involves extracting style parameters as structured JSON data first:

1. **Extract DNA:** Pass reference images to `extract_style.py` or call Gemini 2.5/3 with:
   > *"Help me extract the entire visual effect of these images as a Prompt in JSON format. Include color palette, lighting, composition, stylistic effects, camera lens, and character details."*
2. **Generate Styled Prompts:** Pass the resulting style JSON and new content ideas to Gemini to generate fully aligned Nano Banana prompts.
3. **Generate Image:** Run `generate.py` with the newly synthesized prompt.

---

## Workflow 2: Character/Subject Consistency (Asset Graphs)
For comic strips, storyboards, or multi-scene ads, maintain subject consistency by chaining reference inputs:
* **Flash Limit:** Maintain character resemblance for up to **5 characters** and object fidelity for up to **14 reference objects**.
* **Fidelity Optimization:** Keep references to **$\le$ 10** for Flash, and **$\le$ 6** for Pro.
* Pass reference images as early elements in the `contents` list, followed by the target scene prompt.

---

## Consistency & Detail Preservation Guidelines

When generating complex images containing small details, text, or exact geometries, follow these strict rules to prevent stochastic drift:

### 1. Programmatic Masked Editing (Inpainting)
* **Rule:** If an image is 90%+ correct but has minor shape or spelling issues, do **not** run a full text-to-image regeneration.
* **Workflow:** Call the `generate.py` script with the `-e` (edit base) parameter. Provide the target image and describe only the region to modify, instructing the model to leave the rest of the canvas untouched.

### 2. Anchor Prompting (Geometric Overspecification)
* **Rule:** Avoid vague nouns ("a logo", "a container"). Specify the exact geometry, materials, and placement coordinates.
* **Formula:** `[Base Subject] + [Specific Geometry (e.g. sharp 90-degree corners, rectangular cylinder)] + [Material finish (e.g. matte black metallic, brushed steel)] + [Locked text/label specification (e.g. 'AIAUTO' in uppercase bold sans-serif font)]`.
* Duplicate this exact anchor phrase verbatim across all scene prompt variations.

### 3. Lens & Aperture Configuration (Deep Focus)
* **Rule:** Standard portrait parameters (e.g., `f/1.8 aperture`, `cinematic bokeh`) blur out text rendering and distort small object shapes.
* **Workflow:** Override with deep focus parameters: `f/4.0` to `f/8.0` aperture, `sharp focus across the entire frame`, `macro product photography lens settings`.

### 4. Single Reference Image Hygiene
* **Rule:** To match the exact shape/text of a specific product or logo, use a **single, high-resolution straight-on reference**.
* **Rationale:** Feeding multiple angles or inconsistent references forces the model to average the geometries, causing shape distortions.

---

## Guidelines for Developers
* **Grounding:** To generate contextually accurate images (e.g., weather, landmarks, real-world products), enable Google Search Grounding using `types.GoogleSearch()`.
* **Thought Inspection:** Inspect the `part.thought` text/image blocks returned by Pro models to debug visual reasoning composition issues before final output generation.
* **SynthID:** All generated images natively contain a digital watermark.
