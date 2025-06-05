#!/usr/bin/env python3
"""Test different approaches to improve audio quality."""

import torch
from pathlib import Path
from resonantgen.core.musicgen_engine import MusicGenEngine
from resonantgen.core.track_session import AudioTrack

def test_musicgen_direct():
    """Test MusicGen directly with different prompts and settings."""
    
    print("🎵 Testing MusicGen Audio Quality")
    print("=" * 60)
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
    output_dir = Path(f"outputs/tests/quality_comparison_{timestamp}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize engine
    engine = MusicGenEngine(model_size="small")
    
    # Test different guidance scales
    print("\n1. Testing different guidance scales...")
    guidance_tests = [1.5, 2.0, 2.5, 3.0, 3.5]
    
    for guidance in guidance_tests:
        print(f"\n   Testing guidance_scale={guidance}")
        
        # Temporarily modify the generation config
        engine.model.generation_config.guidance_scale = guidance
        
        # Use a very explicit positive prompt
        prompt = "happy upbeat pop music, major key, bright cheerful melody, professional studio quality, radio hit, 120 BPM"
        
        # Generate
        audio = engine.generate(prompt, duration=4.0)
        
        # Save
        track = AudioTrack(
            data=audio,
            sample_rate=engine.sample_rate,
            duration=audio.shape[1] / engine.sample_rate,
            track_type=f"guidance_{guidance}"
        )
        
        output_path = output_dir / f"guidance_{guidance}.wav"
        track.export(str(output_path))
        print(f"   ✅ Saved {output_path.name}")
    
    # Test different prompt styles
    print("\n2. Testing different prompt styles...")
    
    prompt_tests = [
        # Original style
        ("original", "chill lo-fi hip-hop beat at 72 BPM with jazzy chords"),
        
        # More explicit positive
        ("positive", "happy cheerful music, upbeat and bright, major key, 120 BPM"),
        
        # Professional quality emphasis
        ("quality", "high quality professional music production, clean mixing, 100 BPM"),
        
        # Genre-specific with quality
        ("genre_quality", "smooth jazz music, warm and relaxing, professional recording, 90 BPM"),
        
        # Very simple
        ("simple", "pop music"),
        
        # Detailed technical
        ("technical", "4/4 time signature, C major, quarter note = 110 BPM, verse-chorus structure")
    ]
    
    # Reset to default guidance
    engine.model.generation_config.guidance_scale = 2.5
    
    for name, prompt in prompt_tests:
        print(f"\n   Testing: {name}")
        print(f"   Prompt: {prompt}")
        
        audio = engine.generate(prompt, duration=4.0)
        
        track = AudioTrack(
            data=audio,
            sample_rate=engine.sample_rate,
            duration=audio.shape[1] / engine.sample_rate,
            track_type=name
        )
        
        output_path = output_dir / f"prompt_{name}.wav"
        track.export(str(output_path))
        print(f"   ✅ Saved {output_path.name}")
    
    # Test temperature variations
    print("\n3. Testing temperature settings...")
    
    temp_tests = [0.8, 1.0, 1.2]
    
    for temp in temp_tests:
        print(f"\n   Testing temperature={temp}")
        
        # Create a custom generation with temperature
        prompt = "uplifting electronic dance music, energetic and positive, 128 BPM"
        
        inputs = engine.processor(
            text=[prompt],
            padding=True,
            return_tensors="pt"
        ).to(engine.device)
        
        with torch.no_grad():
            audio_values = engine.model.generate(
                **inputs,
                max_new_tokens=256,  # 4 seconds
                do_sample=True,
                guidance_scale=2.5,
                temperature=temp
            )
        
        audio = audio_values[0].cpu()
        
        track = AudioTrack(
            data=audio,
            sample_rate=engine.sample_rate,
            duration=audio.shape[1] / engine.sample_rate,
            track_type=f"temp_{temp}"
        )
        
        output_path = output_dir / f"temperature_{temp}.wav"
        track.export(str(output_path))
        print(f"   ✅ Saved {output_path.name}")
    
    print(f"\n✅ All tests complete! Check {output_dir.absolute()}/")
    print("\nListen to the files and see which settings produce better quality.")
    print("\nKey insights:")
    print("- Lower guidance_scale (1.5-2.5) often sounds more natural")
    print("- Explicit positive descriptors help avoid dark sounds")
    print("- 'Professional quality' and 'studio recording' keywords may help")

if __name__ == "__main__":
    test_musicgen_direct()