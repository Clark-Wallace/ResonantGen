# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Installation & Setup
```bash
# Install package in development mode
pip install -e .

# Install with dev dependencies
pip install -e ".[dev]"

# Install requirements directly
pip install -r requirements.txt
```

### Testing
```bash
# Run MVP test to verify functionality
python test_mvp.py

# Run example workflows
python examples/jordan_lofi_beat.py

# Run pytest if available
pytest
```

### Code Quality
```bash
# Format code
black .

# Lint code
flake8 .

# Type checking
mypy resonantgen/
```

### Running the Application
```bash
# CLI interface (when implemented)
resonantgen

# API server (when implemented)
resonantgen-server
```

## Architecture Overview

ResonantGen is an AI-native music workstation built around **selective regeneration** - the ability to lock tracks you love and regenerate only what you want to change.

### Core Components

- **MusicWorkstation** (`resonantgen/core/workstation.py`): Main user interface providing natural language music generation with selective track regeneration
- **MusicGenEngine** (`resonantgen/core/musicgen_engine.py`): Clean wrapper around Meta's MusicGen for multi-track generation
- **TrackSession** (`resonantgen/core/track_session.py`): Multi-track session management with locking/unlocking capabilities
- **AudioTrack** (`resonantgen/core/track_session.py`): Individual track with metadata and lock state
- **PromptProcessor** (`resonantgen/core/prompt_processor.py`): Converts natural language to track-specific prompts

### Key Architecture Principles

1. **AI-Native Design**: Natural language is the primary interface, not a bolt-on feature
2. **Multi-Track Generation**: Every generation produces 4 tracks: drums, bass, harmony, melody
3. **Selective Regeneration**: Core innovation allowing users to lock loved tracks and regenerate others
4. **Context-Aware System**: Locked tracks provide musical context for regenerating other tracks

### Data Flow

1. User provides natural language prompt → PromptProcessor
2. PromptProcessor creates track-specific prompts → MusicGenEngine  
3. MusicGenEngine generates audio for each track → AudioTrack objects
4. AudioTrack objects stored in TrackSession with lock/unlock capabilities
5. For regeneration: locked tracks provide context for generating new versions of unlocked tracks

### Track Types

- **drums**: Rhythm and percussion patterns
- **bass**: Basslines that lock to drum patterns
- **harmony**: Chords, pads, atmospheric elements  
- **melody**: Lead lines, hooks, melodic content

### Key User Workflow

```python
# Generate initial tracks
tracks = maw.generate("chill lo-fi hip-hop beat at 72 BPM")

# Lock what you love
tracks['drums'].lock()

# Regenerate what you don't
tracks['bass'] = maw.regenerate("more aggressive 303 acid bass")

# Export the result  
tracks.export("my_track.wav", stems=True)
```

### Technology Stack

- **Foundation Model**: Meta's MusicGen (configurable sizes: small/medium/large)
- **Audio Processing**: PyTorch, torchaudio, librosa, scipy
- **Framework**: Pure Python with optional web interface via FastAPI/Gradio
- **Export**: Supports WAV export for both mixed tracks and individual stems

### Development Notes

- Use `model_size="small"` for faster development/testing
- The system is designed for RTX 3090-class GPUs but works on CPU
- Session management allows saving/loading work via pickle
- Track locking is the core differentiator from traditional AI music tools

### Critical Architecture Insight: Loop-Based Generation

**IMPORTANT**: The AI generates short musical patterns (1-2 seconds) that are then looped to create longer tracks. This solves the "8-second MusicGen limit" by working with music's naturally repetitive structure.

- Generate minimal pattern that captures musical essence
- Loop the pattern to desired duration  
- AI acts as "smart preset manager" translating text to sound parameters
- Much more efficient than generating long continuous audio

See `docs/LOOP_ARCHITECTURE_INSIGHTS.md` for detailed implementation strategy.

## Session Context & Progress Tracking

### Current Development Status (Auto-Updated)

**Last Session: January 6, 2025**
- ✅ Fixed "evil dimension" sound issue in MusicGen generation
- ✅ Updated MusicGenEngine defaults: guidance_scale=1.5, temperature=1.2
- ✅ Created optimized parameter testing suite
- ✅ **CONFIRMED SUCCESS**: User tested output/better_generation/ files - "sounded amazing in comparison"
- 🎯 **Next**: Apply fix to multi-track generation workflow

### Critical Bug Fix: MusicGen Parameters

**Problem**: Default `guidance_scale=3.0` caused distorted, scary-sounding audio
**Solution**: Lowered to `guidance_scale=1.5` with `temperature=1.2`
**Location**: `resonantgen/core/musicgen_engine.py:76` and `:113`

```python
# Optimized parameters for musical output
guidance_scale=1.5,  # Lower = more natural, less distorted
temperature=1.2,     # Slightly higher for musical variety
top_k=250,          # Limit choices for coherence  
top_p=0.95          # Nucleus sampling for better quality
```

### Test Outputs Available
- `output/quality_test/` - Parameter comparison tests
- `output/better_generation/` - Genre-specific tests with optimized parameters
- `output/real_loop_001/` - Multi-track generation example

### Session Recovery Commands
```bash
# Quick status check
python test_mvp.py

# Test current parameter quality
python test_better_generation.py

# Generate new multi-track example
python generate_real_loop.py

# Listen to latest improvements
ls output/better_generation/
```

### Development Context Saves
Context automatically saved to: `docs/SESSION_CONTEXT_[DATE].md`