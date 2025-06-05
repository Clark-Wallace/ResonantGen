"""
ResonantGen - AI Music Workstation

Next-gen AI-native DAW powered by natural language, modular track regeneration, 
and scene-based performance control.
"""

__version__ = "0.1.0"
__author__ = "ResonantGen Team"

from .core.workstation import MusicWorkstation
from .core.track_session import TrackSession, AudioTrack
from .core.prompt_processor import PromptProcessor

__all__ = [
    "MusicWorkstation",
    "TrackSession", 
    "AudioTrack",
    "PromptProcessor",
]