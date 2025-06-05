# ResonantGen Quick Start Guide

Get up and running with the world's first AI Music Workstation in minutes.

---

## Installation

```bash
# Clone the repository
git clone https://github.com/clark-wallace/ResonantGen.git
cd ResonantGen

# Install dependencies
pip install -r requirements.txt

# Or install as package
pip install -e .
```

---

## Your First AI-Generated Track

```python
from resonantgen import MusicWorkstation

# Initialize the workstation
maw = MusicWorkstation()

# Generate multi-track music from natural language
tracks = maw.generate("chill lo-fi hip-hop beat at 72 BPM with jazzy chords")

# Listen to the result
tracks.play()

# Export to audio file
tracks.export("my_first_track.wav")
```

That's it! You just created professional multi-track music with natural language.

---

## The Revolutionary Feature: Selective Regeneration

```python
# Generate initial tracks
tracks = maw.generate("dark techno with driving bassline")

# Love the drums but want a different bass?
tracks['drums'].lock()  # Lock what you love
tracks['bass'] = maw.regenerate("more aggressive 303 acid bass")  # Change what you don't

# Perfect! Same drums, new bass that fits perfectly
tracks.play()
tracks.export("my_track.wav", stems=True)  # Export individual tracks too
```

---

## Understanding the Workflow

### 1. Natural Language Input
ResonantGen understands musical concepts:

```python
# Genre and style
tracks = maw.generate("ambient electronic with ethereal pads")

# Specific parameters  
tracks = maw.generate("jazz at 120 BPM in C minor")

# Instrumentation requests
tracks = maw.generate("rock song with distorted guitar and punchy drums")
```

### 2. Multi-Track Generation
Every generation creates 4 separate tracks:
- **drums**: Rhythm and percussion
- **bass**: Bass lines and low-end
- **harmony**: Chords, pads, atmospheric elements  
- **melody**: Lead lines, hooks, melodic content

### 3. Selective Control
Lock any combination of tracks:

```python
# Lock multiple tracks
tracks['drums'].lock()
tracks['harmony'].lock()

# Regenerate the rest
tracks['bass'] = maw.regenerate("make it funkier")
tracks['melody'] = maw.regenerate("add some jazz improvisation")
```

### 4. Professional Export
Export in multiple formats:

```python
# Mixed stereo track
tracks.export("song.wav")

# Individual stems for DAW
tracks.export("song.wav", stems=True)  # Creates song_stems/ folder

# Save session for later
maw.save_session("my_session.rsg")
```

---

## Example Workflows

### Workflow 1: Hip-Hop Producer
```python
# Start with a basic idea
tracks = maw.generate("boom bap hip-hop at 90 BPM")

# Perfect drums, but want modern bass
tracks['drums'].lock()
tracks['bass'] = maw.regenerate("modern 808 bass with sub frequencies")

# Add some jazz influence to chords
tracks['harmony'] = maw.regenerate("jazz piano chords with vinyl texture")

# Export for sampling
tracks.export("hip_hop_loop.wav", stems=True)
```

### Workflow 2: Electronic Music Artist
```python
# Generate dance track
tracks = maw.generate("progressive house at 128 BPM with ethereal breakdown")

# Love the energy but want different lead
tracks['drums'].lock()
tracks['bass'].lock()
tracks['melody'] = maw.regenerate("add arpeggiated synth lead with filter sweeps")

# Export for live performance
tracks.export("live_set_track.wav")
```

### Workflow 3: Film Composer
```python
# Create atmospheric score
tracks = maw.generate("cinematic ambient with tension and mystery")

# Perfect atmosphere, need different rhythm
tracks['harmony'].lock()  # Keep the atmospheric pads
tracks['melody'].lock()   # Keep the mysterious lead

# Add subtle percussion
tracks['drums'] = maw.regenerate("subtle film score percussion, orchestral")

# Export stems for mixing
tracks.export("film_score_cue.wav", stems=True)
```

---

## Advanced Features

### Session Management
```python
# Work on multiple ideas
session1 = maw.generate("idea 1")
maw.save_session("idea1.rsg")

session2 = maw.generate("idea 2") 
maw.save_session("idea2.rsg")

# Return to previous work
maw.load_session("idea1.rsg")
tracks = maw.current_session
```

### Context-Aware Regeneration
When you regenerate a track, ResonantGen automatically:
- Matches tempo from locked tracks
- Maintains key signature coherence
- Respects frequency space allocation
- Preserves overall musical style

### Prompt Engineering Tips
```python
# Be specific about instruments
"analog synthesizer bass with warm filter"

# Specify musical elements
"syncopated drums with ghost notes"

# Combine genres creatively  
"jazz-influenced electronic with live drum feel"

# Use emotional descriptors
"melancholic piano with hope in the melody"
```

---

## Troubleshooting

### Performance Optimization
```python
# Use smaller model for speed
maw = MusicWorkstation(model_size="small")

# Use GPU if available
maw = MusicWorkstation(device="cuda")
```

### Common Issues

**"Generation is slow"**
- Use `model_size="small"` for faster generation
- Ensure you have adequate RAM/GPU memory

**"Tracks don't sound separated"**
- Try more specific prompts: "drums only, no bass no melody"
- Adjust generation parameters in prompt

**"Can't export audio"**
- Ensure you have write permissions in the output directory
- Check that torchaudio is properly installed

---

## What's Next?

This MVP proves the concept of AI-native music creation. Future developments will include:

- **Web interface** for easier use
- **Live performance mode** for real-time control
- **Advanced NLP** for better musical understanding  
- **MIDI export** for traditional DAW integration
- **Collaboration features** for sharing and remixing

---

## Join the Revolution

You're now equipped with the world's first AI Music Workstation. 

**Create. Lock. Regenerate. Repeat.**

Welcome to the future of music production! 🎵

---

*For more examples, see the `/examples` folder*  
*For technical details, see the full documentation*