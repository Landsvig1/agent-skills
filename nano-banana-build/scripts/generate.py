#!/usr/bin/env python3
"""
Nano Banana image generation and editing script.
Wraps the google-genai SDK to support text-to-image, style transfer, outpainting,
and character consistency workflows.
"""

import argparse
import io
import os
import sys
from pathlib import Path
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv

def get_client() -> genai.Client:
    """Get authenticated Gemini client, loading .env if needed."""
    if not os.environ.get("GEMINI_API_KEY") and not os.environ.get("GOOGLE_API_KEY"):
        # Attempt to load nearest .env
        for path in (Path.cwd(), Path.home() / ".claude", Path.home()):
            env_path = path / ".env"
            if env_path.exists():
                load_dotenv(env_path)
                break
                
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        print("Error: GEMINI_API_KEY environment variable not set.", file=sys.stderr)
        print("Get your API key at: https://aistudio.google.com/apikey", file=sys.stderr)
        sys.exit(1)
        
    return genai.Client(api_key=key)

def load_image_part(path: str) -> types.Part:
    """Loads an image file and wraps it as a types.Part for multimodal input."""
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
    parser = argparse.ArgumentParser(description="Programmatic Nano Banana Generator")
    parser.add_argument("prompt", help="The text instruction or generation prompt")
    parser.add_argument("-r", "--reference", nargs="+", help="Paths to reference images for subject/style consistency")
    parser.add_argument("-e", "--edit", help="Path to base image for inpainting/outpainting/editing")
    parser.add_argument("-a", "--aspect-ratio", choices=["1:1", "16:9", "9:16", "4:3", "3:4", "2:3", "3:2"], help="Aspect ratio for image generation")
    parser.add_argument("-s", "--size", default="1K", choices=["1K", "2K", "4K"], help="Resolution target")
    parser.add_argument("-g", "--grounded", action="store_true", help="Enable Google Search grounding for real-world context")
    parser.add_argument("-m", "--model", default="gemini-3.1-flash-image-preview", help="Gemini Image model name")
    parser.add_argument("-o", "--output", default="output.png", help="Path to save the generated image")
    
    args = parser.parse_args()
    client = get_client()
    
    # 1. Build Generation Config
    image_config_kwargs = {"image_size": args.size}
    if args.aspect_ratio:
        image_config_kwargs["aspect_ratio"] = args.aspect_ratio
        
    config_kwargs = {
        "response_modalities": ["IMAGE"],
        "image_config": types.ImageConfig(**image_config_kwargs),
    }
    
    if args.grounded:
        config_kwargs["tools"] = [types.Tool(google_search=types.GoogleSearch())]
        
    config = types.GenerateContentConfig(**config_kwargs)
    
    # 2. Build Contents list
    contents = []
    
    # Add edit base image if present
    if args.edit:
        contents.append(load_image_part(args.edit))
        
    # Add reference images if present
    if args.reference:
        for ref_path in args.reference:
            contents.append(load_image_part(ref_path))
            
    # Append final prompt
    contents.append(args.prompt)
    
    print(f"[*] Calling model: {args.model}")
    print(f"[*] Prompt: '{args.prompt}'")
    if args.reference:
        print(f"[*] Reference images count: {len(args.reference)}")
    if args.edit:
        print(f"[*] Editing base image: {args.edit}")
        
    try:
        response = client.models.generate_content(
            model=args.model,
            contents=contents,
            config=config
        )
        
        # 3. Extract and Save Image
        saved = False
        candidates = response.candidates or []
        for candidate in candidates:
            parts = candidate.content.parts or []
            for part in parts:
                if part.inline_data:
                    img_data = part.inline_data.data
                    image = Image.open(io.BytesIO(img_data))
                    
                    # Create parent dirs if not existing
                    out_path = Path(args.output)
                    out_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    image.save(out_path)
                    print(f"[+] Successfully saved generated image to: {args.output}")
                    saved = True
                    break
            if saved:
                break
                
        if not saved:
            print("Error: No image content found in the API response candidates.", file=sys.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"API Error during generation: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
