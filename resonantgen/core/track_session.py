"""
Track Session Management - Multi-track session with locking and regeneration

Provides the core multi-track functionality that makes ResonantGen revolutionary.
"""

import typing as tp
from dataclasses import dataclass, field
import torch
import torchaudio
import pickle
from pathlib import Path


@dataclass
class AudioTrack:
    """
    Represents a single audio track with metadata and locking capability.
    
    This is the core unit of ResonantGen's selective regeneration system.
    """
    data: torch.Tensor  # Audio data [1, samples]
    sample_rate: int
    duration: float
    track_type: str  # "drums", "bass", "harmony", "melody"
    metadata: tp.Dict[str, tp.Any] = field(default_factory=dict)
    _locked: bool = field(default=False, init=False)
    
    def lock(self):
        """Lock this track to prevent regeneration."""
        self._locked = True
        print(f"🔒 {self.track_type.capitalize()} track locked")
    
    def unlock(self):
        """Unlock this track to allow regeneration."""
        self._locked = False
        print(f"🔓 {self.track_type.capitalize()} track unlocked")
    
    @property
    def is_locked(self) -> bool:
        """Check if track is locked."""
        return self._locked
    
    def play(self):
        """Play this track (placeholder for now)."""
        print(f"🎵 Playing {self.track_type} track ({self.duration:.1f}s)")
        # TODO: Implement actual audio playback
    
    def export(self, filepath: str):
        """Export this track to audio file."""
        filepath = Path(filepath)
        torchaudio.save(
            filepath, 
            self.data, 
            self.sample_rate,
            format=filepath.suffix[1:] if filepath.suffix else "wav"
        )
        print(f"💾 Exported {self.track_type} to {filepath}")
    
    def get_features(self) -> tp.Dict[str, tp.Any]:
        """Extract musical features from this track for context."""
        # TODO: Implement actual feature extraction
        # For now, return basic info
        return {
            "track_type": self.track_type,
            "duration": self.duration,
            "sample_rate": self.sample_rate,
            "locked": self._locked,
            "rms_energy": torch.sqrt(torch.mean(self.data ** 2)).item(),
            "metadata": self.metadata
        }


class TrackSession:
    """
    Manages a multi-track session with selective regeneration capabilities.
    
    This is the core of ResonantGen's revolutionary workflow - the ability
    to lock tracks you love and regenerate only what you want to change.
    """
    
    def __init__(self, 
                 tracks: tp.Dict[str, AudioTrack] = None,
                 original_prompt: str = "",
                 context: tp.Dict[str, tp.Any] = None):
        """
        Initialize a track session.
        
        Args:
            tracks: Dictionary of track_name -> AudioTrack
            original_prompt: The original generation prompt
            context: Musical context information
        """
        self.tracks = tracks or {}
        self.original_prompt = original_prompt
        self.context = context or {}
        self.duration = max((track.duration for track in self.tracks.values()), default=0.0)
        
        # Track names expected in ResonantGen
        self.track_types = ["drums", "bass", "harmony", "melody"]
    
    def __getitem__(self, track_name: str) -> AudioTrack:
        """Get a track by name."""
        if track_name not in self.tracks:
            raise KeyError(f"Track '{track_name}' not found. Available: {list(self.tracks.keys())}")
        return self.tracks[track_name]
    
    def __setitem__(self, track_name: str, track: AudioTrack):
        """Set a track by name."""
        self.tracks[track_name] = track
        print(f"✅ Updated {track_name} track")
    
    def lock(self, track_name: str):
        """Lock a specific track."""
        self[track_name].lock()
    
    def unlock(self, track_name: str):
        """Unlock a specific track."""
        self[track_name].unlock()
    
    def get_locked_tracks(self) -> tp.Dict[str, AudioTrack]:
        """Get all currently locked tracks."""
        return {name: track for name, track in self.tracks.items() if track.is_locked}
    
    def get_unlocked_tracks(self) -> tp.Dict[str, AudioTrack]:
        """Get all currently unlocked tracks."""
        return {name: track for name, track in self.tracks.items() if not track.is_locked}
    
    def get_locked_context(self) -> tp.Dict[str, tp.Any]:
        """Extract musical context from locked tracks for regeneration."""
        locked_tracks = self.get_locked_tracks()
        if not locked_tracks:
            return {}
        
        context = {
            "locked_track_names": list(locked_tracks.keys()),
            "locked_features": {}
        }
        
        for name, track in locked_tracks.items():
            context["locked_features"][name] = track.get_features()
        
        return context
    
    def update_track(self, track_name: str, new_track: AudioTrack):
        """Update a track with regenerated version."""
        if track_name in self.tracks and self.tracks[track_name].is_locked:
            raise ValueError(f"Cannot update locked track '{track_name}'. Unlock it first.")
        
        self[track_name] = new_track
    
    def play(self):
        """Play all tracks mixed together."""
        print(f"🎵 Playing session: '{self.original_prompt}'")
        for name, track in self.tracks.items():
            status = "🔒" if track.is_locked else "🔓"
            print(f"  {status} {name}: {track.duration:.1f}s")
        
        # TODO: Implement actual mixed playback
        print("   (Audio playback not implemented yet)")
    
    def export(self, 
               filepath: str, 
               format: str = "wav",
               stems: bool = False):
        """
        Export the session to audio file(s).
        
        Args:
            filepath: Base filepath for export
            format: Audio format ("wav", "mp3", etc.)
            stems: If True, export individual stems
        """
        filepath = Path(filepath)
        
        if stems:
            # Export individual tracks
            stem_dir = filepath.parent / f"{filepath.stem}_stems"
            stem_dir.mkdir(exist_ok=True)
            
            for name, track in self.tracks.items():
                stem_path = stem_dir / f"{name}.{format}"
                track.export(stem_path)
            
            print(f"💾 Exported stems to {stem_dir}/")
        
        # Export mixed version
        if len(self.tracks) > 1:
            # Simple mixing - just sum the tracks
            mixed_audio = sum(track.data for track in self.tracks.values())
            mixed_audio = mixed_audio / len(self.tracks)  # Normalize
            
            sample_rate = next(iter(self.tracks.values())).sample_rate
            torchaudio.save(filepath.with_suffix(f".{format}"), mixed_audio, sample_rate)
            print(f"💾 Exported mixed track to {filepath.with_suffix(f'.{format}')}")
        else:
            # Single track - just export it
            track = next(iter(self.tracks.values()))
            track.export(filepath.with_suffix(f".{format}"))
    
    def save(self, filepath: str):
        """Save session to file for later loading."""
        with open(filepath, 'wb') as f:
            pickle.dump({
                'tracks': self.tracks,
                'original_prompt': self.original_prompt,
                'context': self.context,
                'duration': self.duration
            }, f)
        print(f"💾 Session saved to {filepath}")
    
    @classmethod
    def load(cls, filepath: str) -> 'TrackSession':
        """Load session from file."""
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        
        session = cls(
            tracks=data['tracks'],
            original_prompt=data['original_prompt'],
            context=data['context']
        )
        print(f"📁 Session loaded from {filepath}")
        return session
    
    def status(self):
        """Print current session status."""
        print(f"\n🎵 Session Status: '{self.original_prompt}'")
        print(f"   Duration: {self.duration:.1f}s")
        print(f"   Tracks: {len(self.tracks)}")
        
        for name, track in self.tracks.items():
            status = "🔒 LOCKED" if track.is_locked else "🔓 unlocked"
            print(f"     {name}: {status}")
        
        locked_count = len(self.get_locked_tracks())
        print(f"   Locked: {locked_count}/{len(self.tracks)} tracks")