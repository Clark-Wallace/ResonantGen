#!/usr/bin/env python3
"""Generate a better quality audio loop with improved prompts and parameters."""

import os
from pathlib import Path
from resonantgen import MusicWorkstation
from resonantgen.core.prompt_processor import PromptProcessor

# Better prompt templates for MusicGen
BETTER_TRACK_TEMPLATES = {
    "drums": "drums only, {genre} drums, {tempo} BPM, crisp and clear, professional mixing, high quality recording",
    "bass": "bass only, {genre} bass line, {tempo} BPM, warm and deep, professional mixing, high quality recording", 
    "harmony": "chords only, {genre} chord progression, {tempo} BPM, smooth and musical, professional mixing, high quality recording",
    "melody": "lead melody only, {genre} melodic line, {tempo} BPM, catchy and musical, professional mixing, high quality recording"
}

def main():
    print("🎵 ResonantGen - Generating Better Quality Audio Loop")
    print("=" * 60)
    
    # Create output directory
    output_dir = Path("output/better_loop_001")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize with custom parameters
    print("\n1. Initializing with improved settings...")
    
    # Temporarily patch the prompt templates
    original_templates = PromptProcessor.TRACK_TEMPLATES.copy()
    PromptProcessor.TRACK_TEMPLATES = BETTER_TRACK_TEMPLATES
    
    # Initialize workstation
    maw = MusicWorkstation(model_size="small")
    
    # Also patch the guidance scale for less extreme generation
    original_guidance = maw.engine.model.generation_config.guidance_scale
    maw.engine.model.generation_config.guidance_scale = 2.0  # Lower for more natural sound
    
    print("✅ MusicWorkstation ready with improved settings")
    
    # Try different prompts for better results
    prompts_to_try = [
        "upbeat pop music at 120 BPM, happy and bright, professional quality",
        "smooth jazz at 90 BPM, relaxed and warm, high quality recording",
        "energetic rock at 140 BPM, powerful and clear, studio quality"
    ]
    
    print("\n2. Testing different musical styles...")
    
    for i, prompt in enumerate(prompts_to_try):
        print(f"\n--- Style {i+1}: {prompt.split(' at ')[0]} ---")
        
        session = maw.generate(prompt)
        
        # Save this style
        style_dir = output_dir / f"style_{i+1}"
        style_dir.mkdir(exist_ok=True)
        
        # Export individual tracks
        for track_name, track in session.tracks.items():
            output_path = style_dir / f"{track_name}.wav"
            track.export(str(output_path))
        
        # Export mixed version
        mixed_path = style_dir / "mixed.wav"
        session.export(mixed_path, stems=False)
        
        print(f"✅ Saved to {style_dir}/")
    
    # Restore original settings
    PromptProcessor.TRACK_TEMPLATES = original_templates
    maw.engine.model.generation_config.guidance_scale = original_guidance
    
    print(f"\n🎉 Generated 3 different styles with better prompts!")
    print(f"Output saved to: {output_dir.absolute()}")
    print("\nThese should sound more musical and less 'horror film'!")
    
    # Also generate with explicit positive descriptors
    print("\n3. Generating one more with very explicit positive prompts...")
    
    explicit_prompt = "happy uplifting music, major key, bright and cheerful, 110 BPM, professional studio recording, radio-ready quality"
    session = maw.generate(explicit_prompt)
    
    final_dir = output_dir / "explicit_positive"
    final_dir.mkdir(exist_ok=True)
    
    for track_name, track in session.tracks.items():
        track.export(str(final_dir / f"{track_name}.wav"))
    
    session.export(final_dir / "mixed.wav", stems=False)
    
    print(f"✅ Final version saved to {final_dir}/")
    print("\n🎵 Try these files - they should sound much better!")

if __name__ == "__main__":
    main()