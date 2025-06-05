# ResonantGen Technical Specification

## Core Technology Stack

### Backend (Python 3.11+)
- **PyTorch 2.0+**: Core ML framework (CUDA 12.1 for RTX 3090)
- **FastAPI**: High-performance async API server
- **EnCodec**: Audio compression/tokenization (extracted from MusicGen)
- **librosa**: Audio analysis and feature extraction
- **Redis**: Track state and caching (optional)

### Model Architecture
- **Base Model Size**: ~500M parameters per track type (vs MusicGen's 3.3B)
- **Quantization**: INT8 inference for real-time performance
- **Attention**: Efficient attention (Flash Attention 2)

### Audio Specifications
- **Sample Rate**: 44.1kHz (professional standard)
- **Bit Depth**: 24-bit
- **Format**: WAV (lossless) with MP3 export option
- **Latency Target**: <100ms for real-time preview

## Detailed Component Specifications

### 1. NLP Prompt Analyzer

```python
class PromptAnalyzer:
    """
    Extracts musical intent from natural language.
    Uses small local LLM (e.g., Phi-3) for understanding.
    """
    
    def analyze(self, prompt: str) -> MusicContext:
        return MusicContext(
            genre="techno",
            mood=["dark", "driving"],
            tempo=128,
            key="Am",
            time_signature="4/4",
            instruments={
                "drums": ["kick", "hihat", "clap"],
                "bass": ["analog", "sub"],
                "lead": ["saw", "pluck"]
            },
            structure="intro-buildup-drop-breakdown-outro",
            energy_profile=[0.3, 0.5, 0.9, 0.4, 0.6]
        )
```

### 2. Track Generator Specifications

#### DrumGen Model
- **Input**: Tempo, genre, energy profile
- **Output**: Multi-channel drum patterns (kick, snare, hihat, etc.)
- **Special Features**: Microtiming, swing, humanization

#### BassGen Model  
- **Input**: Key, chord progression, drum pattern
- **Output**: Monophonic bass line with articulation
- **Special Features**: Note sliding, filter automation

#### HarmonyGen Model
- **Input**: Key, progression, genre context
- **Output**: Polyphonic pad/chord tracks
- **Special Features**: Voice leading, tension/release

#### MelodyGen Model
- **Input**: Key, harmony, rhythmic context
- **Output**: Lead melodies, hooks, arpeggios
- **Special Features**: Call-response patterns, motivic development

### 3. Audio Processing Pipeline

```python
class AudioPipeline:
    def __init__(self):
        self.encoder = EnCodecModel.encoder
        self.decoder = EnCodecModel.decoder
        
    def process_audio(self, raw_audio: np.array) -> torch.Tensor:
        # 1. Normalize and prepare
        audio = self.normalize(raw_audio)
        
        # 2. Encode to tokens
        tokens = self.encoder(audio)
        
        # 3. Process through model
        generated_tokens = self.model(tokens)
        
        # 4. Decode back to audio
        output_audio = self.decoder(generated_tokens)
        
        return output_audio
```

### 4. Context-Aware Generation

```python
class ContextManager:
    """Manages musical context across tracks"""
    
    def __init__(self):
        self.harmonic_context = HarmonicAnalyzer()
        self.rhythmic_context = RhythmAnalyzer()
        self.spectral_context = SpectralAnalyzer()
    
    def analyze_locked_tracks(self, tracks: Dict[str, AudioTrack]):
        context = {
            'tempo': self.rhythmic_context.estimate_tempo(tracks),
            'key': self.harmonic_context.estimate_key(tracks),
            'chord_progression': self.harmonic_context.extract_chords(tracks),
            'rhythmic_pattern': self.rhythmic_context.extract_pattern(tracks),
            'frequency_space': self.spectral_context.analyze_spectrum(tracks)
        }
        return context
```

### 5. Performance Specifications

#### Generation Speed Targets
- **Single Track (8 seconds)**: 2-3 seconds
- **Full Arrangement (4 tracks)**: 5-8 seconds
- **Regeneration (1 track with context)**: 1-2 seconds

#### Memory Requirements
- **Model Loading**: ~2GB per track type
- **Generation Buffer**: ~500MB
- **Context Cache**: ~200MB

#### GPU Utilization (RTX 3090)
- **VRAM Usage**: 8-12GB during generation
- **Compute**: 70-80% utilization target
- **Batch Size**: 4-8 parallel generations

### 6. API Endpoints

```python
# Core Generation
POST /api/generate
POST /api/regenerate/{track_id}
POST /api/generate/preview  # Quick low-quality preview

# Track Management  
GET  /api/tracks
POST /api/tracks/{id}/lock
POST /api/tracks/{id}/unlock
PUT  /api/tracks/{id}/params

# Context and Analysis
GET  /api/analyze/prompt
GET  /api/analyze/audio/{track_id}
POST /api/context/save
GET  /api/context/{id}

# Export and Rendering
POST /api/export/stems
POST /api/export/mix
POST /api/render/realtime  # WebSocket endpoint
```

### 7. Data Flow Architecture

```
User Input (NL Prompt)
    ↓
Prompt Analysis
    ↓
Context Building ← Locked Tracks Analysis
    ↓
Parallel Track Generation
    ├── DrumGen
    ├── BassGen  
    ├── HarmonyGen
    └── MelodyGen
    ↓
Audio Assembly & Mixing
    ↓
Output (Multi-track Audio)
```

### 8. Training Data Requirements

- **Drum Stems**: 100k+ isolated drum tracks
- **Bass Stems**: 100k+ bass lines with genre labels
- **Harmony Stems**: 50k+ chord progressions
- **Melody Stems**: 50k+ lead lines
- **Full Mixes**: 200k+ for context learning

### 9. Model Training Pipeline

```python
class TrackModelTrainer:
    def __init__(self, track_type: str):
        self.model = TrackGenerator(track_type)
        self.dataset = StemDataset(track_type)
        
    def train_phase_1(self):
        # Isolated track generation
        pass
        
    def train_phase_2(self):
        # Context-aware generation
        pass
        
    def train_phase_3(self):
        # Selective regeneration optimization
        pass
```

### 10. Quality Metrics

- **Audio Quality**: PESQ score > 4.0
- **Musical Coherence**: Human evaluation score > 8/10
- **Generation Speed**: <10s for full arrangement
- **Context Accuracy**: 90%+ key/tempo matching
- **User Satisfaction**: "Regeneration Count" < 3 average

## Implementation Phases

### Phase 1: Core Audio Generation (Weeks 1-4)
- Extract and adapt EnCodec
- Build basic DrumGen model
- Prove e2e audio generation

### Phase 2: Multi-Track System (Weeks 5-8)
- Add remaining track generators
- Implement context system
- Basic API and track management

### Phase 3: Intelligence Layer (Weeks 9-12)
- Advanced NLP understanding
- Musical theory enforcement
- Performance optimizations

### Phase 4: Production Ready (Weeks 13-16)
- Full API implementation
- Performance mode
- Export and rendering features

---

*These specifications are designed for practical implementation while maintaining musical quality and system performance.*