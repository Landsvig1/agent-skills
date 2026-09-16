#!/usr/bin/env python3
"""
Visual DNA Extraction Script using Gemini multimodal capabilities.
Analyzes a set of reference images to generate a unified style blueprint.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from google import genai
from google.genai import types
from dotenv import load_dotenv

def get_client() -> genai.Client:
    """Get authenticated Gemini client, loading .env if needed."""
    if not os.environ.get("GEMINI_API_KEY") and not os.environ.get("GOOGLE_API_KEY"):
        # Attempt to load nearest .env
        for path in (Path.cwd(), Path(__file__).parents[4], Path.home() / ".claude", Path.home()):
            env_path = path / ".env"
            if env_path.exists():
                load_dotenv(env_path)
                break
                
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        print("Error: GEMINI_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)
        
    return genai.Client(api_key=key)

def load_image_part(path: str) -> types.Part:
    try:
        with open(path, "rb") as f:
            data = f.read()
        suffix = Path(path).suffix.lower().lstrip(".")
        mime_type = f"image/{suffix}"
        if mime_type == "image/jpg":
            mime_type = "image/jpeg"
        return types.Part.from_bytes(data=data, mime_type=mime_type)
    except Exception as e:
        print(f"Error loading image '{path}': {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Extract Visual DNA from reference images")
    parser.add_argument("images", nargs="+", help="Paths to reference images to analyze")
    parser.add_argument("-o", "--output", default="visual_dna.json", help="Path to save output JSON")
    parser.add_argument("-m", "--model", default="gemini-2.5-flash", help="Gemini multimodal model to use")
    
    args = parser.parse_args()
    client = get_client()
    
    contents = []
    for img_path in args.images:
        contents.append(load_image_part(img_path))
        
    analysis_prompt = (
        "You are an expert design director. Analyze this collection of images. "
        "Extract their collective visual identity ('Visual DNA') and return it as a structured JSON object. "
        "Include the following fields: \n"
        "1. color_palette: (dominant hex colors and tone)\n"
        "2. lighting_style: (soft/hard, directions, temperature)\n"
        "3. composition_rules: (minimalism, grids, margins)\n"
        "4. stylistic_effects: (grain, contrast, vintage filters)\n"
        "5. camera_parameters: (lens, depth of field)\n"
        "6. recurring_subjects: (portraits, landscapes, objects)\n"
        "Output ONLY valid JSON."
    )
    
    contents.append(analysis_prompt)
    
    print(f"[*] Analyzing {len(args.images)} images for visual style DNA...")
    try:
        response = client.models.generate_content(
            model=args.model,
            contents=contents,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        # Parse and pretty print to ensure it's valid JSON
        data = json.loads(response.text)
        
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            
        print(f"[+] Successfully extracted visual DNA JSON to: {args.output}")
        
    except Exception as e:
        print(f"Error during Visual DNA extraction: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
