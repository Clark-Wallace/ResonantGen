# ResonantGen Modular System Design

## Core Philosophy: Composable Music Generation

ResonantGen is built as a collection of specialized, interoperable modules rather than a monolithic system. Each module excels at one thing and communicates through well-defined interfaces.

## Module Hierarchy

```
ResonantGen Core
├── Language Understanding Layer
│   ├── Prompt Parser
│   ├── Musical Intent Extractor
│   └── Parameter Mapper
├── Generation Layer  
│   ├── Track Generators
│   │   ├── DrumGen
│   │   ├── BassGen
│   │   ├── HarmonyGen
│   │   └── MelodyGen
│   └── Context Manager
├── Audio Processing Layer
│   ├── EnCodec Interface
│   ├── Feature Extractors
│   └── Mix Engine
└── API Layer
    ├── REST Endpoints
    ├── WebSocket Streams
    └── State Manager
```

## Module Specifications

### 1. Language Understanding Layer

#### Prompt Parser Module
```python
class PromptParser:
    """Converts natural language to structured music descriptors"""
    
    def parse(self, prompt: str) -> ParsedPrompt:
        # "dark techno with driving bass at 128 bpm"
        return ParsedPrompt(
            genre=["techno"],
            mood=["dark", "driving"],
            tempo=128,
            instruments=["bass"],
            structure_hints=[]
        )
```

#### Musical Intent Extractor
```python
class MusicalIntentExtractor:
    """Understands deeper musical meaning"""
    
    def extract_intent(self, parsed: ParsedPrompt) -> MusicalIntent:
        # Interprets "driving bass" → specific bass characteristics
        return MusicalIntent(
            bass_pattern="four_on_floor",
            bass_timbre="aggressive",
            bass_processing=["distortion", "compression"]
        )
```

### 2. Track Generator Modules

Each generator is a self-contained module with:
- Its own model weights
- Specialized preprocessing
- Track-specific optimizations

#### DrumGen Module
```python
class DrumGen(BaseTrackGenerator):
    """Specialized drum and percussion generation"""
    
    def __init__(self):
        self.model = DrumTransformer()
        self.pattern_library = DrumPatterns()
        self.humanizer = MicroTimingEngine()
    
    def generate(self, context: GenerationContext) -> DrumTrack:
        # Generates multi-channel drum track
        # Kick, snare, hihat, etc. as separate channels
        pattern = self.pattern_library.get(context.genre)
        tokens = self.model.generate(pattern, context)
        audio = self.decode_drums(tokens)
        return self.humanizer.process(audio)
```

#### BassGen Module  
```python
class BassGen(BaseTrackGenerator):
    """Bass line generation with harmonic awareness"""
    
    def __init__(self):
        self.model = BassTransformer()
        self.harmony_analyzer = HarmonicContext()
        self.groove_matcher = GrooveLock()
    
    def generate(self, context: GenerationContext, 
                 locked_drums: Optional[DrumTrack] = None) -> BassTrack:
        # Locks to drum groove if provided
        if locked_drums:
            groove = self.groove_matcher.extract(locked_drums)
            context.groove_template = groove
        
        return self.model.generate(context)
```

### 3. Context Management System

#### Cross-Track Context Manager
```python
class ContextManager:
    """Maintains musical coherence across tracks"""
    
    def __init__(self):
        self.harmonic_state = HarmonicState()
        self.rhythmic_state = RhythmicState()
        self.spectral_state = SpectralState()
        self.arrangement_state = ArrangementState()
    
    def update_from_track(self, track: AudioTrack, track_type: str):
        """Updates context when a track is locked"""
        self.harmonic_state.analyze(track)
        self.rhythmic_state.analyze(track)
        self.spectral_state.update_frequency_allocation(track, track_type)
    
    def get_generation_context(self, track_type: str) -> GenerationContext:
        """Provides context for generating new tracks"""
        return GenerationContext(
            key=self.harmonic_state.current_key,
            chord_progression=self.harmonic_state.progression,
            tempo=self.rhythmic_state.tempo,
            groove=self.rhythmic_state.pattern,
            available_frequencies=self.spectral_state.get_range(track_type)
        )
```

### 4. Audio Processing Pipeline

#### EnCodec Interface Module
```python
class EnCodecInterface:
    """Abstraction over audio tokenization"""
    
    def __init__(self, model_path: str):
        self.encoder = self.load_encoder(model_path)
        self.decoder = self.load_decoder(model_path)
        self.sample_rate = 44100
    
    def tokenize(self, audio: np.ndarray, 
                 track_type: str = "general") -> torch.Tensor:
        # Track-specific tokenization strategies
        if track_type == "drums":
            return self.tokenize_percussive(audio)
        elif track_type == "bass":
            return self.tokenize_low_freq(audio)
        else:
            return self.encoder(audio)
```

#### Feature Extraction Suite
```python
class FeatureExtractors:
    """Modular audio analysis tools"""
    
    @staticmethod
    def tempo(audio: np.ndarray) -> float:
        return TempoExtractor().process(audio)
    
    @staticmethod  
    def key(audio: np.ndarray) -> str:
        return KeyExtractor().process(audio)
    
    @staticmethod
    def rhythm_pattern(audio: np.ndarray) -> RhythmPattern:
        return RhythmExtractor().process(audio)
```

### 5. Integration Modules

#### Track Lock Manager
```python
class TrackLockManager:
    """Handles the killer feature - selective regeneration"""
    
    def __init__(self):
        self.locked_tracks = {}
        self.track_features = {}
        self.generation_history = []
    
    def lock_track(self, track_id: str, audio_data: AudioTrack):
        self.locked_tracks[track_id] = audio_data
        self.track_features[track_id] = self.extract_features(audio_data)
        
    def get_locked_context(self) -> LockedContext:
        return LockedContext(
            tracks=self.locked_tracks,
            features=self.track_features,
            constraints=self.derive_constraints()
        )
```

#### Scene System Module
```python
class SceneManager:
    """Performance-oriented state management"""
    
    def save_scene(self, name: str) -> SceneID:
        scene = Scene(
            prompt=self.current_prompt,
            tracks=self.current_tracks,
            settings=self.current_settings,
            context=self.context_manager.snapshot()
        )
        return self.store.save(scene)
    
    def load_scene(self, scene_id: SceneID):
        scene = self.store.load(scene_id)
        self.restore_state(scene)
```

## Module Communication

### Event Bus System
```python
class EventBus:
    """Loose coupling between modules"""
    
    def __init__(self):
        self.subscribers = defaultdict(list)
    
    def publish(self, event: str, data: Any):
        for callback in self.subscribers[event]:
            callback(data)
    
    def subscribe(self, event: str, callback: Callable):
        self.subscribers[event].append(callback)

# Usage
bus = EventBus()
bus.subscribe("track.generated", context_manager.update_from_track)
bus.subscribe("track.locked", track_lock_manager.lock_track)
```

### Standardized Interfaces

All modules communicate through typed interfaces:

```python
@dataclass
class AudioTrack:
    data: np.ndarray
    sample_rate: int
    duration: float
    track_type: str
    metadata: Dict[str, Any]

@dataclass
class GenerationRequest:
    prompt: str
    duration: float
    locked_tracks: Dict[str, AudioTrack]
    parameters: Dict[str, Any]

@dataclass  
class GenerationResponse:
    tracks: Dict[str, AudioTrack]
    generation_time: float
    context: GenerationContext
```

## Extensibility Points

### Adding New Track Types
```python
class VocalGen(BaseTrackGenerator):
    """Example: Adding vocal generation"""
    
    def __init__(self):
        super().__init__("vocal")
        self.phoneme_mapper = PhonemeMapper()
        self.voice_synthesizer = VoiceSynth()
    
    def generate(self, context: GenerationContext, 
                 lyrics: Optional[str] = None) -> VocalTrack:
        # New track type with minimal changes to core
        pass

# Register with system
track_registry.register("vocal", VocalGen)
```

### Custom Processing Modules
```python
class VinylEmulator(AudioProcessor):
    """Add vintage processing"""
    
    def process(self, audio: AudioTrack) -> AudioTrack:
        audio = self.add_noise(audio)
        audio = self.add_crackle(audio) 
        audio = self.frequency_limit(audio)
        return audio

# Chain processors
pipeline.add_processor("vinyl", VinylEmulator())
```

## Module Dependencies

```yaml
# module_deps.yaml
core:
  - pytorch>=2.0
  - numpy
  - librosa

track_generators:
  base:
    - core
    - encodec_interface
  drums:
    - base
    - rhythm_analysis
  bass:
    - base  
    - harmonic_analysis
    
audio_processing:
  - core
  - scipy.signal
  - pyaudio (optional, for preview)

api:
  - fastapi
  - redis (optional)
  - all_generators
```

## Testing Strategy

Each module has isolated tests:

```python
# test_drumgen.py
def test_drum_generation_isolated():
    drumgen = DrumGen()
    context = GenerationContext(genre="techno", tempo=128)
    
    drums = drumgen.generate(context)
    assert drums.duration == 8.0
    assert has_kick_pattern(drums)
    assert tempo_matches(drums, 128)

# test_integration.py  
def test_bass_follows_drums():
    drums = DrumGen().generate(context)
    bass = BassGen().generate(context, locked_drums=drums)
    
    assert rhythmic_coherence(drums, bass) > 0.8
    assert frequency_separation(drums, bass) > 0.9
```

## Benefits of Modular Design

1. **Independent Development**: Teams can work on different modules
2. **Easy Testing**: Each module can be tested in isolation
3. **Flexible Deployment**: Use only what you need
4. **Progressive Enhancement**: Add features without breaking core
5. **Clear Interfaces**: Well-defined contracts between components
6. **Performance**: Load only active modules
7. **Maintainability**: Bugs isolated to specific modules

---

*This modular architecture ensures ResonantGen remains flexible, maintainable, and extensible as it grows from prototype to production system.*