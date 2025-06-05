#!/usr/bin/env python3
"""Generate quick sample tracks for repository showcase."""

import json
from pathlib import Path
from datetime import datetime
from resonantgen.core.musicgen_engine import MusicGenEngine
from resonantgen.core.track_session import AudioTrack

def generate_quick_samples():
    """Generate a few quick sample tracks using MusicGenEngine directly."""
    
    print("🎵 ResonantGen - Quick Sample Generation")
    print("=" * 50)
    
    # Create samples directory
    samples_dir = Path("examples/samples")
    samples_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize engine
    print("\n1. Loading MusicGen engine...")
    engine = MusicGenEngine(model_size="small")
    print("✅ Engine ready")
    
    # Quick sample prompts (shorter generation time)
    samples = [
        {
            "name": "lofi_demo",
            "prompt": "relaxing lo-fi hip hop, warm vinyl sound, soft drums, jazzy chords",
            "description": "Chill lo-fi hip-hop demonstrating improved audio quality"
        },
        {
            "name": "electronic_demo", 
            "prompt": "upbeat electronic music, bright synths, energetic beat, major key",
            "description": "Upbeat electronic track showcasing musical coherence"
        },
        {
            "name": "acoustic_demo",
            "prompt": "gentle acoustic guitar, fingerpicking, warm and peaceful",
            "description": "Acoustic guitar demonstration of natural sound generation"
        }
    ]
    
    # Generate samples
    for i, sample in enumerate(samples, 1):
        print(f"\n{i}. Generating: {sample['name']}")
        print(f"   Prompt: {sample['prompt']}")
        
        # Generate 4-second sample
        audio = engine.generate(sample['prompt'], duration=4.0)
        
        # Create track
        track = AudioTrack(
            data=audio,
            sample_rate=engine.sample_rate,
            duration=audio.shape[1] / engine.sample_rate,
            track_type="demo"
        )
        
        # Save to samples directory
        sample_path = samples_dir / f"{sample['name']}.wav"
        track.export(str(sample_path))
        
        print(f"   ✅ Saved: {sample['name']}.wav ({track.duration:.1f}s)")
        
        # Save metadata
        metadata = {
            "name": sample['name'],
            "description": sample['description'],
            "prompt": sample['prompt'],
            "duration": track.duration,
            "file": f"{sample['name']}.wav",
            "generated_at": datetime.now().isoformat(),
            "model": "MusicGen Small (optimized parameters)"
        }
        
        with open(samples_dir / f"{sample['name']}_info.json", "w") as f:
            json.dump(metadata, f, indent=2)
    
    # Create samples README
    readme_content = f"""# ResonantGen Audio Samples

Sample tracks demonstrating ResonantGen's improved audio quality.

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Before & After

These samples showcase the **audio quality improvements** made to ResonantGen:

✅ **Fixed**: "Evil dimension" distorted sound  
✅ **Improved**: Musical, coherent output  
✅ **Optimized**: MusicGen parameters (guidance_scale=1.5, temperature=1.2)

## Sample Tracks

"""
    
    for sample in samples:
        readme_content += f"""### {sample['name'].replace('_', ' ').title()}

- **File**: `{sample['name']}.wav`
- **Description**: {sample['description']}
- **Prompt**: "{sample['prompt']}"

"""
    
    readme_content += """## Technical Details

- **Model**: MusicGen Small
- **Duration**: ~4 seconds each
- **Sample Rate**: 32kHz
- **Parameters**: 
  - guidance_scale: 1.5 (reduced from 3.0)
  - temperature: 1.2 (increased from 1.0)
  - top_k: 250, top_p: 0.95

## Quality Comparison

Listen to these samples to hear the difference from the original "scary/evil" sounding output to proper musical generation. The parameter optimization resolved audio distortion issues and produces natural-sounding music.
"""
    
    with open(samples_dir / "README.md", "w") as f:
        f.write(readme_content)
    
    print(f"\n🎉 Quick samples generated!")
    print(f"📁 Location: {samples_dir.absolute()}")
    print(f"🎵 Files: {len(samples)} audio samples + metadata + README")
    
    return samples_dir

if __name__ == "__main__":
    samples_dir = generate_quick_samples()