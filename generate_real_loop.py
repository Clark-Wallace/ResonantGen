#!/usr/bin/env python3
"""Generate a real audio loop using ResonantGen."""

import os
from pathlib import Path
from resonantgen import MusicWorkstation

def main():
    print("🎵 ResonantGen - Generating Real Audio Loop")
    print("=" * 60)
    
    # Create output directory with timestamp
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
    output_dir = Path(f"outputs/sessions/session_{timestamp}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize MusicWorkstation with small model for faster generation
    print("\n1. Initializing MusicWorkstation...")
    maw = MusicWorkstation(model_size="small")
    print("✅ MusicWorkstation ready")
    
    # Generate a chill lo-fi beat
    prompt = "chill lo-fi hip-hop beat at 72 BPM with jazzy chords and warm analog bass"
    print(f"\n2. Generating: {prompt}")
    print("   This will take a moment as MusicGen creates real audio...")
    
    session = maw.generate(prompt)
    print("✅ Audio generation complete!")
    
    # Show what was generated
    print("\n3. Generated tracks:")
    for track_name, track in session.tracks.items():
        print(f"   - {track_name}: {track.duration:.1f} seconds")
    
    # Save individual tracks
    print(f"\n4. Saving tracks to {output_dir}/")
    for track_name, track in session.tracks.items():
        output_path = output_dir / f"{track_name}.wav"
        track.export(str(output_path))
        print(f"   ✅ Saved {track_name}.wav")
    
    # Create and save mixed version
    print("\n5. Creating mixed version...")
    mixed_path = output_dir / "mixed.wav"
    session.export(mixed_path, stems=False)
    print(f"   ✅ Saved mixed.wav")
    
    # Also export stems package
    stems_path = output_dir / "stems_package.wav"
    session.export(stems_path, stems=True)
    print(f"   ✅ Saved stems_package.wav (all stems)")
    
    print(f"\n🎉 Success! Real audio loops saved to: {output_dir.absolute()}")
    print("\nYou can play these files with any audio player!")
    
    return session

if __name__ == "__main__":
    session = main()