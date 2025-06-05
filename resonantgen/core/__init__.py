"""
ResonantGen Core Components

Contains the core music generation and track management systems.
"""

from .workstation import MusicWorkstation
from .track_session import TrackSession, AudioTrack
from .musicgen_engine import MusicGenEngine
from .prompt_processor import PromptProcessor

__all__ = [
    "MusicWorkstation",
    "TrackSession",
    "AudioTrack", 
    "MusicGenEngine",
    "PromptProcessor",
]