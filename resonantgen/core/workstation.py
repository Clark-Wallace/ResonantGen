"""
MusicWorkstation - Main interface for ResonantGen

This is the primary user-facing class that provides the natural language
music generation interface with selective regeneration capabilities.
"""

import typing as tp
from dataclasses import dataclass
import torch

from .musicgen_engine import MusicGenEngine
from .track_session import TrackSession, AudioTrack
from .prompt_processor import PromptProcessor


@dataclass
class GenerationRequest:
    """Request for music generation."""
    prompt: str
    duration: float = 8.0
    locked_tracks: tp.Dict[str, str] = None
    style_params: tp.Dict[str, tp.Any] = None
    
    def __post_init__(self):
        if self.locked_tracks is None:
            self.locked_tracks = {}
        if self.style_params is None:
            self.style_params = {}


class MusicWorkstation:
    """
    Main interface for ResonantGen AI Music Workstation.
    
    This class provides the natural language interface for music generation
    with selective track regeneration capabilities.
    
    Example:
        >>> maw = MusicWorkstation()
        >>> tracks = maw.generate("chill lo-fi hip-hop beat at 72 BPM")
        >>> tracks['drums'].lock()
        >>> tracks['melody'] = maw.regenerate("add vinyl crackle atmosphere")
        >>> tracks.export("my_track.wav")
    """
    
    def __init__(self, model_size: str = "small", device: str = "auto"):
        """
        Initialize the Music Workstation.
        
        Args:
            model_size: Size of MusicGen model ("small", "medium", "large")
            device: Device to run on ("cuda", "cpu", "auto")
        """
        self.device = self._setup_device(device)
        self.engine = MusicGenEngine(model_size=model_size, device=self.device)
        self.prompt_processor = PromptProcessor()
        self.current_session: tp.Optional[TrackSession] = None
        
    def _setup_device(self, device: str) -> torch.device:
        """Setup the compute device."""
        if device == "auto":
            return torch.device("cuda" if torch.cuda.is_available() else "cpu")
        return torch.device(device)
    
    def generate(self, prompt: str, duration: float = 8.0, **kwargs) -> TrackSession:
        """
        Generate a multi-track composition from natural language prompt.
        
        Args:
            prompt: Natural language description of the music
            duration: Duration in seconds
            **kwargs: Additional generation parameters
            
        Returns:
            TrackSession with generated tracks
            
        Example:
            >>> tracks = maw.generate("dark techno with driving bass at 128 BPM")
        """
        request = GenerationRequest(prompt=prompt, duration=duration, **kwargs)
        
        # Process the prompt to understand musical intent
        music_context = self.prompt_processor.analyze(prompt)
        
        # Generate tracks using context-aware prompting
        track_prompts = self.prompt_processor.create_track_prompts(music_context)
        
        generated_tracks = {}
        for track_name, track_prompt in track_prompts.items():
            print(f"Generating {track_name}...")
            audio_data = self.engine.generate(track_prompt, duration)
            
            generated_tracks[track_name] = AudioTrack(
                data=audio_data,
                sample_rate=self.engine.sample_rate,
                duration=duration,
                track_type=track_name,
                metadata={
                    "prompt": track_prompt,
                    "original_request": prompt,
                    "generation_context": music_context
                }
            )
        
        # Create session
        self.current_session = TrackSession(
            tracks=generated_tracks,
            original_prompt=prompt,
            context=music_context
        )
        
        return self.current_session
    
    def regenerate(self, track_name: str, new_prompt: str, **kwargs) -> AudioTrack:
        """
        Regenerate a specific track with new prompt while respecting locked tracks.
        
        Args:
            track_name: Name of track to regenerate ("drums", "bass", "harmony", "melody")
            new_prompt: New description for this track
            **kwargs: Additional parameters
            
        Returns:
            New AudioTrack for the regenerated track
            
        Example:
            >>> new_bass = maw.regenerate("bass", "more aggressive 303 acid sound")
        """
        if not self.current_session:
            raise ValueError("No active session. Generate tracks first.")
        
        # Get context from locked tracks
        locked_context = self.current_session.get_locked_context()
        
        # Create context-aware prompt
        full_prompt = self.prompt_processor.create_regeneration_prompt(
            track_name=track_name,
            new_description=new_prompt,
            locked_context=locked_context,
            original_context=self.current_session.context
        )
        
        # Generate new track
        audio_data = self.engine.generate(full_prompt, self.current_session.duration)
        
        new_track = AudioTrack(
            data=audio_data,
            sample_rate=self.engine.sample_rate,
            duration=self.current_session.duration,
            track_type=track_name,
            metadata={
                "prompt": full_prompt,
                "regeneration_request": new_prompt,
                "locked_context": locked_context
            }
        )
        
        # Update session
        self.current_session.update_track(track_name, new_track)
        
        return new_track
    
    def performance_mode(self) -> "PerformanceInterface":
        """
        Enter live performance mode for real-time track manipulation.
        
        Returns:
            PerformanceInterface for live control
        """
        if not self.current_session:
            raise ValueError("No active session. Generate tracks first.")
        
        # TODO: Implement performance interface
        # This will provide Yamaha Motif-style live control
        raise NotImplementedError("Performance mode coming in Phase 4")
    
    def save_session(self, filepath: str):
        """Save the current session to file."""
        if not self.current_session:
            raise ValueError("No active session to save.")
        
        self.current_session.save(filepath)
    
    def load_session(self, filepath: str) -> TrackSession:
        """Load a session from file."""
        self.current_session = TrackSession.load(filepath)
        return self.current_session