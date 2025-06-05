#!/usr/bin/env python3
"""Test with better MusicGen parameters to avoid scary/evil sounds."""

import torch
from pathlib import Path
from resonantgen.core.musicgen_engine import MusicGenEngine
from resonantgen.core.track_session import AudioTrack

def test_better_musicgen():
    """Test MusicGen with optimized parameters for musical output."""
    
    print("🎵 Testing MusicGen with Better Parameters")
    print("=" * 60)
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
    output_dir = Path(f"outputs/tests/parameter_optimization_{timestamp}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize engine
    engine = MusicGenEngine(model_size="small")
    
    # Best configuration based on your feedback
    best_config = {
        "guidance_scale": 1.5,  # Lower is more natural
        "temperature": 1.2,     # Slightly higher for variety
        "do_sample": True,
        "top_k": 250,          # Limit choices for coherence
        "top_p": 0.95          # Nucleus sampling
    }
    
    print("\nUsing optimized parameters:")
    for k, v in best_config.items():
        print(f"  {k}: {v}")
    
    # Test various musical styles with positive, clear prompts
    test_tracks = [
        {
            "name": "lofi_chill",
            "prompt": "relaxing lo-fi hip hop beat, warm vinyl sound, soft drums, jazzy chords, 75 BPM, peaceful and calm",
            "duration": 8.0
        },
        {
            "name": "happy_pop",
            "prompt": "upbeat happy pop song, major key, bright piano, cheerful melody, 120 BPM, feel-good vibes",
            "duration": 8.0
        },
        {
            "name": "smooth_jazz",
            "prompt": "smooth jazz, warm saxophone, soft brushed drums, walking bass, 90 BPM, late night relaxation",
            "duration": 8.0
        },
        {
            "name": "acoustic_folk",
            "prompt": "gentle acoustic guitar, fingerpicking pattern, warm and intimate, 100 BPM, coffeehouse atmosphere",
            "duration": 8.0
        },
        {
            "name": "ambient_pad",
            "prompt": "ambient pad, lush reverb, warm synthesizer, peaceful meditation music, slow evolution, calming",
            "duration": 8.0
        }
    ]
    
    for track_info in test_tracks:
        print(f"\n🎼 Generating: {track_info['name']}")
        print(f"   Prompt: {track_info['prompt']}")
        
        # Process prompt
        inputs = engine.processor(
            text=[track_info['prompt']],
            padding=True,
            return_tensors="pt"
        ).to(engine.device)
        
        # Generate with optimized parameters
        tokens_needed = int(track_info['duration'] * 32)
        
        with torch.no_grad():
            audio_values = engine.model.generate(
                **inputs,
                max_new_tokens=tokens_needed,
                guidance_scale=best_config['guidance_scale'],
                temperature=best_config['temperature'],
                do_sample=best_config['do_sample'],
                top_k=best_config['top_k'],
                top_p=best_config['top_p']
            )
        
        audio = audio_values[0].cpu()
        
        # Create track and save
        track = AudioTrack(
            data=audio,
            sample_rate=engine.sample_rate,
            duration=audio.shape[1] / engine.sample_rate,
            track_type=track_info['name']
        )
        
        output_path = output_dir / f"{track_info['name']}.wav"
        track.export(str(output_path))
        print(f"   ✅ Saved: {output_path.name}")
        print(f"   Duration: {track.duration:.1f}s")
    
    # Also create a quick A/B test with the problematic parameters
    print("\n\n📊 A/B Test: Good vs Bad Parameters")
    print("-" * 40)
    
    test_prompt = "happy upbeat music, major scale, bright and cheerful, 120 BPM"
    
    # Bad parameters (original)
    print("\n❌ Bad parameters (guidance=3.0, temp=1.0):")
    inputs = engine.processor(
        text=[test_prompt],
        padding=True,
        return_tensors="pt"
    ).to(engine.device)
    
    with torch.no_grad():
        bad_audio = engine.model.generate(
            **inputs,
            max_new_tokens=128,  # 4 seconds
            guidance_scale=3.0,
            temperature=1.0,
            do_sample=True
        )
    
    bad_track = AudioTrack(
        data=bad_audio[0].cpu(),
        sample_rate=engine.sample_rate,
        duration=bad_audio[0].shape[1] / engine.sample_rate,
        track_type="bad_params"
    )
    bad_track.export(str(output_dir / "test_bad_params.wav"))
    
    # Good parameters
    print("✅ Good parameters (guidance=1.5, temp=1.2):")
    with torch.no_grad():
        good_audio = engine.model.generate(
            **inputs,
            max_new_tokens=128,  # 4 seconds
            guidance_scale=1.5,
            temperature=1.2,
            do_sample=True,
            top_k=250,
            top_p=0.95
        )
    
    good_track = AudioTrack(
        data=good_audio[0].cpu(),
        sample_rate=engine.sample_rate,
        duration=good_audio[0].shape[1] / engine.sample_rate,
        track_type="good_params"
    )
    good_track.export(str(output_dir / "test_good_params.wav"))
    
    print(f"\n\n✅ All generations complete!")
    print(f"📁 Output directory: {output_dir.absolute()}")
    print("\n🎧 Listen and compare:")
    print("   - The main tracks should sound musical and pleasant")
    print("   - test_bad_params.wav should sound dark/scary")
    print("   - test_good_params.wav should sound normal")
    print("\n💡 Key insights:")
    print("   - Lower guidance_scale (1.5) = more natural sound")
    print("   - Higher temperature (1.2) = more musical variety")
    print("   - Clear positive prompts help avoid dark tones")
    print("   - top_k and top_p help with coherence")

if __name__ == "__main__":
    test_better_musicgen()