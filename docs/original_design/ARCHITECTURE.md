# ResonantGen Architecture Design

## System Overview

ResonantGen is a ground-up rebuild of MusicGen's core concepts, designed specifically for multi-track, natural language-driven music production with selective regeneration capabilities.

## Core Architecture Principles

### 1. Modular Track-Aware Generation
Instead of generating a single stereo mix, ResonantGen generates individual tracks that are musically aware of each other.

```
Natural Language Input → Context Analyzer → Track Generators → Audio Output
                                              ↑
                                    Locked Track Context
```

### 2. Track Types and Specialized Models

Each track type has its own specialized generation model:

- **DrumGen**: Rhythm and percussion patterns
- **BassGen**: Bass lines that lock to drum patterns  
- **HarmonyGen**: Chords, pads, atmospheric elements
- **MelodyGen**: Lead lines, hooks, melodic content
- **VocalGen**: Vocal synthesis and processing (future)

### 3. Context-Aware Generation Pipeline

```python
class GenerationPipeline:
    def generate(self, prompt: str, locked_tracks: Dict[str, AudioTrack]):
        # 1. Analyze prompt for musical intent
        context = self.nlp_analyzer.analyze(prompt)
        
        # 2. Extract features from locked tracks
        locked_features = self.extract_musical_features(locked_tracks)
        
        # 3. Generate each track with awareness of others
        tracks = {}
        for track_type in context.required_tracks:
            if track_type not in locked_tracks:
                tracks[track_type] = self.generators[track_type].generate(
                    context=context,
                    locked_context=locked_features,
                    duration=context.duration
                )
        
        return tracks
```

## Technical Components

### 1. Audio Tokenization (from MusicGen)
- Keep EnCodec for audio tokenization
- Modify for track-specific frequency ranges
- Optimize for real-time encoding/decoding

### 2. Transformer Architecture
- Smaller, specialized transformers per track type
- Shared embedding space for musical coherence
- Cross-attention mechanism for track interactions

### 3. Musical Feature Extraction
```python
class MusicalFeatureExtractor:
    def extract(self, audio: AudioTrack):
        return {
            'tempo': self.estimate_tempo(audio),
            'key': self.estimate_key(audio),
            'energy': self.calculate_energy_profile(audio),
            'rhythmic_pattern': self.extract_rhythm(audio),
            'harmonic_progression': self.analyze_harmony(audio)
        }
```

### 4. NLP Music Understanding
Enhanced prompt analysis that understands:
- Genre specifications ("techno", "jazz", "ambient")
- Mood descriptors ("dark", "uplifting", "aggressive")
- Technical parameters ("140 bpm", "minor key", "4/4 time")
- Instrument preferences ("analog synth bass", "808 drums")

## Model Architecture Details

### Base Model Structure
```python
class TrackGenerator(nn.Module):
    def __init__(self, model_size='small'):
        super().__init__()
        self.encoder = EnCodecEncoder(track_specific=True)
        self.transformer = nn.Transformer(
            d_model=512,
            nhead=8,
            num_encoder_layers=6,
            num_decoder_layers=6
        )
        self.decoder = EnCodecDecoder(track_specific=True)
        self.context_attention = CrossTrackAttention()
```

### Training Strategy
1. **Phase 1**: Train individual track models on isolated stems
2. **Phase 2**: Fine-tune with multi-track context
3. **Phase 3**: Optimize for selective regeneration scenarios

## API Design

### Core Generation Endpoint
```python
@app.post("/generate")
async def generate(request: GenerationRequest):
    """
    request = {
        "prompt": "dark techno with driving bassline",
        "duration": 8.0,
        "locked_tracks": {
            "drums": "file_hash_xyz.wav",
            "bass": null  # Will be regenerated
        },
        "params": {
            "tempo": 128,
            "key": "Am"
        }
    }
    """
```

### Track Management
```python
class TrackManager:
    def lock_track(self, track_id: str)
    def unlock_track(self, track_id: str)
    def regenerate_track(self, track_id: str, new_context: dict)
    def get_track_features(self, track_id: str)
```

## Performance Optimizations

### GPU Utilization (RTX 3090)
- Batch processing across track types
- Mixed precision training (FP16)
- Optimized attention mechanisms
- Parallel track generation where possible

### Memory Management
- Stream processing for long compositions
- Efficient caching of locked track features
- On-demand model loading per track type

## File Structure
```
ResonantGen/
├── core/
│   ├── models/
│   │   ├── base_generator.py
│   │   ├── drum_generator.py
│   │   ├── bass_generator.py
│   │   ├── harmony_generator.py
│   │   └── melody_generator.py
│   ├── audio/
│   │   ├── encodec_wrapper.py
│   │   ├── feature_extractor.py
│   │   └── audio_processor.py
│   ├── nlp/
│   │   ├── prompt_analyzer.py
│   │   └── music_vocabulary.py
│   └── pipeline/
│       ├── generation_pipeline.py
│       └── context_manager.py
├── training/
│   ├── dataset_builder.py
│   ├── train_track_model.py
│   └── evaluate.py
├── api/
│   ├── server.py
│   ├── models.py
│   └── track_manager.py
└── tests/
    ├── test_generation.py
    ├── test_context_awareness.py
    └── test_performance.py
```

## Integration Points

### With DAW Frontend
- WebSocket for real-time generation updates
- Progressive audio streaming
- Track metadata and feature APIs

### With Scene System
- Save/load generation contexts
- Quick switching between configurations
- Performance mode optimizations

## Next Steps for Implementation

1. **Extract EnCodec from MusicGen**
   - Understand compression/decompression pipeline
   - Create standalone implementation

2. **Build Minimal Generator**
   - Single track type first (drums)
   - Basic transformer architecture
   - Prove audio generation works

3. **Add Context System**
   - Musical feature extraction
   - Cross-track attention
   - Locked track conditioning

4. **Scale to Multi-Track**
   - Add remaining track types
   - Implement full pipeline
   - Optimize performance

---

*This architecture is designed to be implemented incrementally. Start with core audio generation, then add sophistication.*