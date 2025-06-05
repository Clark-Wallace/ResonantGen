#!/usr/bin/env python3
"""Generate sample tracks for repository showcase."""

import json
from pathlib import Path
from datetime import datetime
from resonantgen import MusicWorkstation

def generate_showcase_samples():
    """Generate diverse sample tracks to showcase ResonantGen capabilities."""
    
    print("🎵 ResonantGen - Generating Repository Samples")
    print("=" * 60)
    
    # Create samples directory
    samples_dir = Path("examples/samples")
    samples_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize workstation
    print("\n1. Initializing MusicWorkstation...")
    maw = MusicWorkstation(model_size="small")
    print("✅ MusicWorkstation ready")
    
    # Define sample tracks to generate
    sample_tracks = [
        {
            "name": "lofi_chill",
            "prompt": "relaxing lo-fi hip hop beat, warm vinyl sound, soft drums, jazzy chords, 75 BPM, peaceful morning vibes",
            "description": "Chill lo-fi hip-hop with warm analog character"
        },
        {
            "name": "upbeat_electronic", 
            "prompt": "upbeat electronic dance music, energetic synths, four-on-the-floor kick, bright leads, 128 BPM, festival energy",
            "description": "High-energy electronic dance track"
        },
        {
            "name": "acoustic_folk",
            "prompt": "gentle acoustic folk, fingerpicked guitar, warm and intimate, organic feel, 95 BPM, coffeehouse atmosphere",
            "description": "Intimate acoustic folk with fingerpicked guitar"
        },
        {
            "name": "jazzy_swing",
            "prompt": "swing jazz, walking bass, brushed drums, warm piano chords, sophisticated harmony, 120 BPM, late night club",
            "description": "Classic swing jazz with sophisticated harmony"
        },
        {
            "name": "ambient_pad",
            "prompt": "ambient soundscape, lush reverb, evolving pad textures, ethereal atmosphere, slow movement, meditation music",
            "description": "Ethereal ambient soundscape for relaxation"
        }
    ]
    
    # Generate each sample
    sample_info = []
    
    for i, track_info in enumerate(sample_tracks, 1):
        print(f"\n{i}. Generating: {track_info['name']}")
        print(f"   Prompt: {track_info['prompt']}")
        print("   🎼 Creating multi-track session...")
        
        # Generate session
        session = maw.generate(track_info['prompt'])
        
        # Create track directory
        track_dir = samples_dir / track_info['name']
        track_dir.mkdir(exist_ok=True)
        
        # Save individual stems
        print("   💾 Saving individual stems...")
        for track_name, track in session.tracks.items():
            stem_path = track_dir / f"{track_name}.wav"
            track.export(str(stem_path))
            print(f"      ✅ {track_name}.wav ({track.duration:.1f}s)")
        
        # Save mixed version
        mixed_path = track_dir / "mixed.wav"
        session.export(mixed_path, stems=False)
        print(f"   🎵 Saved mixed.wav ({session.duration:.1f}s)")
        
        # Save metadata
        metadata = {
            "name": track_info['name'],
            "description": track_info['description'],
            "prompt": track_info['prompt'],
            "duration": session.duration,
            "tracks": list(session.tracks.keys()),
            "generated_at": datetime.now().isoformat(),
            "model_info": {
                "engine": "MusicGen",
                "size": "small",
                "parameters": {
                    "guidance_scale": 1.5,
                    "temperature": 1.2,
                    "top_k": 250,
                    "top_p": 0.95
                }
            }
        }
        
        with open(track_dir / "info.json", "w") as f:
            json.dump(metadata, f, indent=2)
        
        sample_info.append(metadata)
        print(f"   📋 Saved metadata")
    
    # Create samples index
    index_data = {
        "title": "ResonantGen Sample Tracks",
        "description": "Showcase of AI-generated music using ResonantGen",
        "generated_at": datetime.now().isoformat(),
        "total_samples": len(sample_tracks),
        "samples": sample_info
    }
    
    with open(samples_dir / "index.json", "w") as f:
        json.dump(index_data, f, indent=2)
    
    # Create README for samples
    readme_content = f"""# ResonantGen Sample Tracks

This directory contains sample tracks generated with ResonantGen to showcase the system's capabilities.

## Samples Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

"""
    
    for track_info in sample_tracks:
        readme_content += f"""### {track_info['name'].replace('_', ' ').title()}

**Description**: {track_info['description']}

**Prompt**: "{track_info['prompt']}"

**Files**:
- `{track_info['name']}/mixed.wav` - Final mixed track
- `{track_info['name']}/drums.wav` - Drum track 
- `{track_info['name']}/bass.wav` - Bass track
- `{track_info['name']}/harmony.wav` - Harmony track
- `{track_info['name']}/melody.wav` - Melody track
- `{track_info['name']}/info.json` - Generation metadata

"""
    
    readme_content += """## Technical Details

All samples generated using:
- **Model**: MusicGen Small
- **Parameters**: guidance_scale=1.5, temperature=1.2, top_k=250, top_p=0.95
- **Multi-track**: Each sample contains 4 individual stems plus mixed version
- **Duration**: ~5 seconds each (loop-based generation)

## Usage

These samples demonstrate ResonantGen's ability to:
1. Generate diverse musical styles from text prompts
2. Create multi-track arrangements with drums, bass, harmony, and melody
3. Produce coherent, musical-sounding output (not distorted/scary)
4. Maintain stylistic consistency within each track

Play the mixed.wav files to hear the complete tracks, or individual stems to hear how each layer contributes to the overall sound.
"""
    
    with open(samples_dir / "README.md", "w") as f:
        f.write(readme_content)
    
    print(f"\n\n🎉 Sample generation complete!")
    print(f"📁 Samples saved to: {samples_dir.absolute()}")
    print(f"🎵 Generated {len(sample_tracks)} diverse tracks")
    print(f"📋 Created README and metadata files")
    print("\n🔍 Sample overview:")
    
    for track_info in sample_tracks:
        print(f"  - {track_info['name']}: {track_info['description']}")
    
    return samples_dir

if __name__ == "__main__":
    samples_dir = generate_showcase_samples()