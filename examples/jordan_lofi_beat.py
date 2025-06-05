#!/usr/bin/env python3
"""
Jordan's Lo-Fi Beat Creation - Example of ResonantGen MVP

This example demonstrates the exact user story Jordan described:
generating a lo-fi hip-hop beat with selective regeneration.
"""

from resonantgen import MusicWorkstation

def jordan_workflow():
    """
    Demonstrate Jordan's complete workflow from the user story.
    """
    print("🎵 Jordan's Lo-Fi Beat Creation with ResonantGen")
    print("="*60)
    
    # Initialize the workstation
    print("\n1. Initializing ResonantGen Music Workstation...")
    maw = MusicWorkstation(model_size="small")  # Use small model for speed
    
    # Jordan's initial prompt
    prompt = "Give me a chill lo-fi hip-hop beat at 72 BPM with jazzy chords, a lazy swing to the drums, and warm analog bass"
    
    print(f"\n2. Jordan's request: '{prompt}'")
    print("\n   Generating multi-track arrangement...")
    
    # Generate the initial tracks
    tracks = maw.generate(prompt, duration=8.0)
    
    print("\n✅ Initial generation complete!")
    tracks.status()
    
    # Play the initial result
    print("\n3. Jordan listens to the initial result...")
    tracks.play()
    
    # Jordan loves the bass but wants to change the drums
    print("\n4. Jordan's feedback: 'I love the bass, but make the drums more organic'")
    
    # Lock the bass track
    tracks.lock('bass')
    
    # Regenerate drums with new description
    print("\n   Regenerating drums with organic feel...")
    new_drums = maw.regenerate('drums', 'more organic feel, live drum samples, less quantized')
    
    print("\n✅ Drums regenerated!")
    tracks.status()
    
    # Play the updated result
    print("\n5. Jordan listens to the updated version...")
    tracks.play()
    
    # Export the final result
    print("\n6. Jordan exports his creation...")
    tracks.export("jordan_lofi_beat.wav", stems=True)
    
    print("\n🎉 Success! Jordan has his lo-fi beat in under 60 seconds")
    print("   - Professional multi-track arrangement")
    print("   - Selective control over individual elements") 
    print("   - Ready to import into his DAW")
    
    return tracks

def demonstrate_selective_regeneration():
    """
    Show the power of selective regeneration with multiple iterations.
    """
    print("\n" + "="*60)
    print("🔄 Demonstrating Selective Regeneration Power")
    print("="*60)
    
    maw = MusicWorkstation()
    
    # Start with a basic prompt
    tracks = maw.generate("upbeat electronic dance track")
    print("\n1. Initial generation:")
    tracks.status()
    
    # Lock drums and bass, regenerate harmony
    tracks.lock('drums')
    tracks.lock('bass')
    print("\n2. Locking rhythm section, changing harmony...")
    maw.regenerate('harmony', 'darker, more atmospheric pads')
    tracks.status()
    
    # Now change melody while keeping everything else
    tracks.lock('harmony')  # Lock the new harmony too
    print("\n3. Adding dramatic melody...")
    maw.regenerate('melody', 'dramatic lead synth, powerful hook')
    tracks.status()
    
    # Final result
    print("\n✅ Final result: Same rhythm section, new harmony and melody")
    tracks.play()
    
    return tracks

def show_performance_potential():
    """
    Show how this could work in live performance mode (conceptual).
    """
    print("\n" + "="*60)
    print("🎛️ Live Performance Mode Concept")
    print("="*60)
    
    print("""
    In live performance mode, Jordan could:
    
    🎤 Voice commands during performance:
    "Make the bass more aggressive"
    "Add some reverb to the melody" 
    "Switch to minor chords"
    "Drop the drums for 8 bars"
    
    🎚️ Scene-based control (like Yamaha Motif):
    Scene 1: Full arrangement
    Scene 2: Just drums and bass  
    Scene 3: Atmospheric breakdown
    Scene 4: Build-up with all elements
    
    🔄 Real-time regeneration:
    - Generate variations on the fly
    - Never play the same set twice
    - Audience requests via natural language
    
    This is the future of AI-assisted live performance!
    """)

if __name__ == "__main__":
    # Run Jordan's workflow
    tracks = jordan_workflow()
    
    # Show additional capabilities
    demonstrate_selective_regeneration()
    show_performance_potential()
    
    print("\n🎯 ResonantGen MVP: Proving the concept works!")
    print("Ready for full development and GitHub repo launch 🚀")