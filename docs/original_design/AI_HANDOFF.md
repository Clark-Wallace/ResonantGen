# AI Handoff Document - ResonantGen Project

## For the Downstream Claude Instance

This document is designed to communicate our vision and technical approach for building ResonantGen - a custom AI music generation engine built on MusicGen's architecture but designed specifically for our AI-native DAW.

### Your Mission

You are tasked with helping to strip down and rebuild MusicGen into ResonantGen - a modular, track-aware music generation system that powers the next generation of AI-native music production.

### Core Vision

**Build an AI music generation engine where:**
- Users describe music in natural language ("dark techno with ethereal vocals and a driving bassline")
- The system generates multi-track compositions (drums, bass, leads, pads, vocals)
- Users can lock tracks they love and regenerate only what they want to change
- Everything is optimized for real-time performance on modern GPUs (RTX 3090)

### What Makes This Different

Traditional DAWs + AI = Bolted-on features
ResonantGen = AI-native from the ground up

We're not adding AI to a DAW. We're building a music production system where AI is the primary interface.

### Key Technical Decisions

1. **Start with MusicGen's Core**
   - Keep: EnCodec audio tokenization, transformer architecture
   - Strip: Unnecessary dependencies, general-purpose features
   - Rebuild: Multi-track awareness, modular generation, track context

2. **Modular Model Architecture**
   - Separate models for different track types (drums, bass, melodic, vocal)
   - Shared context understanding between models
   - Ability to condition generation on locked tracks

3. **Performance First**
   - Target: 3-5 seconds for 8-second clip generation
   - Direct PyTorch/CUDA optimization for RTX 3090
   - No unnecessary abstraction layers

### Your First Tasks

1. **Analyze MusicGen's Architecture**
   - Identify core components needed for audio generation
   - Map out dependencies that can be eliminated
   - Understand EnCodec integration

2. **Design Modular Pipeline**
   - How to split generation into track-specific models
   - How to maintain musical coherence across tracks
   - How to implement the track-locking mechanism

3. **Start Minimal**
   - Get basic audio generation working without audiocraft dependencies
   - Focus on single-track generation first
   - Build up to multi-track once foundation is solid

### Communication Protocol

When documenting your work:
- Use clear headers for different components
- Include code examples where helpful
- Flag critical decisions with "DECISION:" markers
- Mark uncertainties with "QUESTION:" for upstream discussion
- Use "INSIGHT:" for important discoveries about MusicGen's architecture

### Success Metrics

You'll know you're on the right track when:
- Generation works without audiocraft/transformers dependency conflicts
- Audio quality matches or exceeds original MusicGen
- Track-aware generation produces musically coherent results
- Generation time is under 10 seconds on RTX 3090

### Remember

We're not just porting MusicGen. We're reimagining it for a specific purpose: natural language music production with selective regeneration. Every decision should support that goal.

---

*This handoff prepared by the upstream Claude instance working on ResonantGen architecture. Check ARCHITECTURE.md for detailed technical specifications.*