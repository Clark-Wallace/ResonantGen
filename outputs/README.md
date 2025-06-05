# ResonantGen Outputs

This directory contains all generated audio files organized by purpose.

## Directory Structure

```
outputs/
├── sessions/          # User generation sessions
│   ├── session_001/   # Timestamped session folders
│   ├── session_002/
│   └── ...
├── tests/             # Development and parameter tests
│   ├── parameter_tests/
│   ├── quality_tests/
│   └── benchmarks/
├── exports/           # Final exported tracks
│   ├── stems/         # Individual track stems
│   └── mixed/         # Final mixed tracks
└── README.md         # This file
```

## Session Naming Convention

- **sessions/session_YYYY_MM_DD_HH_MM/** - User generation sessions
- **tests/test_DESCRIPTION/** - Development tests
- **exports/PROJECT_NAME/** - Final exports

## File Organization

Each session contains:
- `drums.wav` - Drum track
- `bass.wav` - Bass track  
- `harmony.wav` - Harmony/chord track
- `melody.wav` - Melody track
- `mixed.wav` - Final mix
- `session_info.json` - Generation metadata

## Usage

- User sessions go in `sessions/`
- Development tests go in `tests/`
- Final tracks ready for use go in `exports/`