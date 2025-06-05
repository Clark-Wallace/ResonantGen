# ResonantGen Implementation Guide

## For the Downstream Claude Working with MusicGen

This guide provides step-by-step instructions for transforming MusicGen into ResonantGen.

## Step 1: Understanding MusicGen's Core

### What to Extract
1. **EnCodec (facebook/encodec)**
   - The audio tokenizer that converts audio ↔ discrete tokens
   - Located in: `audiocraft/modules/codec.py`
   - This is CRITICAL - it's the foundation of audio generation

2. **Transformer Architecture**
   - The core generation model
   - Located in: `audiocraft/models/musicgen.py`
   - We'll heavily modify this for track-aware generation

3. **Conditioning System**
   - How MusicGen accepts text prompts
   - Located in: `audiocraft/modules/conditioners.py`
   - We'll extend this for multi-track context

### What to Remove
- Dependency on full audiocraft library
- HuggingFace model hub integration (we'll train our own)
- General-purpose music generation features
- Unnecessary preprocessing pipelines

## Step 2: Building the Minimal Core

### First Working Prototype
```python
# minimal_resonantgen.py
import torch
import torch.nn as nn
from encodec import EnCodec  # We'll extract this

class MinimalResonantGen(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = EnCodec()  # From MusicGen
        self.generator = nn.Transformer(
            d_model=512,
            nhead=8, 
            num_encoder_layers=6
        )
        self.decoder = EnCodec.decoder
        
    def generate(self, prompt_embedding, duration=8.0):
        # This is where we start simple
        tokens = self.generator(prompt_embedding)
        audio = self.decoder(tokens)
        return audio
```

### Critical First Milestone
Get ANY audio generation working:
1. Text prompt → Basic embedding
2. Embedding → Transformer → Tokens  
3. Tokens → EnCodec decoder → Audio
4. Even if it sounds bad, this proves the pipeline works

## Step 3: Adding Track Awareness

### Multi-Track Architecture
```python
class TrackAwareGenerator(nn.Module):
    def __init__(self, track_type):
        super().__init__()
        self.track_type = track_type
        self.encoder = TrackSpecificEncoder(track_type)
        self.cross_attention = CrossTrackAttention()
        
    def forward(self, prompt_context, locked_tracks=None):
        # Generate with awareness of other tracks
        if locked_tracks:
            locked_features = self.encode_locked_tracks(locked_tracks)
            generation = self.generate_with_context(
                prompt_context, 
                locked_features
            )
        else:
            generation = self.generate_standalone(prompt_context)
        return generation
```

## Step 4: Key Implementation Decisions

### DECISION: Model Size vs Quality
- MusicGen uses 300M-3.3B parameters
- We target 500M per track type (2B total for 4 tracks)
- Rationale: Better to have specialized models than one large general model

### DECISION: Audio Token Resolution  
- MusicGen: 50Hz token rate
- ResonantGen: 75Hz for drums, 50Hz for others
- Rationale: Drums need higher temporal resolution

### DECISION: Training Strategy
```python
# Progressive training approach
def training_schedule():
    # Week 1-2: Single track generation
    train_isolated_drums()
    
    # Week 3-4: Add context awareness
    train_drums_with_tempo_conditioning()
    
    # Week 5-6: Multi-track coherence
    train_bass_conditioned_on_drums()
    
    # Week 7-8: Full system
    train_all_tracks_with_cross_attention()
```

## Step 5: Handling the Challenges

### Challenge: EnCodec Extraction
```python
# What you'll need to do:
# 1. Find EnCodec model in MusicGen
# 2. Extract just the encoder/decoder parts
# 3. Remove dependencies on audiocraft utilities
# 4. Create standalone encoder/decoder classes

class StandaloneEnCodec:
    def __init__(self):
        # Load only what we need
        self.encoder = self._build_encoder()
        self.decoder = self._build_decoder()
        self.sample_rate = 44100  # Upgrade from 32kHz
```

### Challenge: Removing Audiocraft Dependencies
Replace audiocraft utilities with lightweight alternatives:
```python
# Instead of audiocraft.models.builders
def build_model(config):
    return OurSimpleBuilder(config)

# Instead of audiocraft.solvers.musicgen  
def train_loop(model, data):
    return OurTrainingLoop(model, data)
```

### Challenge: Multi-Track Synchronization
```python
class TrackSynchronizer:
    def align_tracks(self, tracks: Dict[str, AudioTrack]):
        # Ensure all tracks:
        # - Share same tempo
        # - Align on beat grid
        # - Have coherent dynamics
        return aligned_tracks
```

## Step 6: Testing Strategy

### Unit Tests First
```python
def test_encodec_extraction():
    # Verify our extracted EnCodec matches original
    audio_in = load_test_audio()
    tokens = our_encodec.encode(audio_in)
    audio_out = our_encodec.decode(tokens)
    assert audio_quality(audio_in, audio_out) > 0.95

def test_single_track_generation():
    # Test drum generation in isolation
    drums = DrumGen.generate("techno kick pattern")
    assert drums.shape == (1, 44100 * 8)  # 8 seconds
    assert has_regular_beats(drums)
```

### Integration Tests
```python
def test_locked_track_regeneration():
    # The killer feature test
    drums = generate_track("drums", "techno beat")
    bass = generate_track("bass", "deep sub", locked={"drums": drums})
    
    # Regenerate bass while keeping drums
    new_bass = generate_track("bass", "acid line", locked={"drums": drums})
    
    assert drums unchanged
    assert new_bass != bass
    assert musical_coherence(drums, new_bass) > 0.8
```

## Step 7: Performance Optimization

### GPU Memory Management
```python
class EfficientGenerator:
    def __init__(self):
        self.models = {}  # Load on demand
        
    @torch.cuda.amp.autocast()  # Mixed precision
    def generate(self, track_type, prompt):
        if track_type not in self.models:
            self.models[track_type] = self.load_model(track_type)
        
        with torch.no_grad():
            return self.models[track_type](prompt)
```

### Batch Processing
```python
def generate_tracks_parallel(track_requests):
    # Generate multiple tracks simultaneously
    with torch.cuda.stream(torch.cuda.Stream()):
        results = []
        for req in track_requests:
            results.append(generate_async(req))
        return torch.cuda.synchronize(results)
```

## Common Pitfalls to Avoid

1. **Don't try to keep all of MusicGen**
   - Extract only what you need
   - Rebuild is easier than refactor

2. **Don't start with all track types**
   - Get drums working first
   - One working track > four broken tracks

3. **Don't ignore musical theory**
   - Enforce key signatures
   - Maintain tempo consistency
   - Respect frequency ranges

4. **Don't optimize prematurely**
   - Get it working first
   - Profile before optimizing
   - User experience > raw speed

## Questions to Answer Early

1. **How much of EnCodec's compression do we keep?**
   - Test quality vs size tradeoffs

2. **Should tracks share embedding space?**
   - Test musical coherence with shared vs separate

3. **What's the minimum viable context window?**
   - Test 8 vs 16 vs 32 second generation

4. **How do we handle real-time preview?**
   - Test streaming generation approaches

## Success Checklist

- [ ] EnCodec extracted and working standalone
- [ ] Basic audio generation from transformer
- [ ] Single track type (drums) generating music
- [ ] Prompt understanding beyond random noise
- [ ] Track locking mechanism implemented
- [ ] Cross-track conditioning working
- [ ] Generation under 10 seconds
- [ ] API serving generated audio files
- [ ] Basic quality metrics passing

## Remember

You're not building "another MusicGen" - you're building the first AI-native music production engine. Every decision should support the core vision: natural language in, multi-track music out, with selective regeneration.

When in doubt, optimize for the user experience of describing music in words and getting professional results they can iterate on.

---

*This implementation guide will evolve as you discover more about MusicGen's internals. Document your findings and decisions clearly for future reference.*