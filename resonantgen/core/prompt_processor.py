"""
Prompt Processing - Convert natural language to track-specific prompts

This module handles the NLP processing that makes ResonantGen understand
musical intent and convert it to effective MusicGen prompts.
"""

import typing as tp
import re
from dataclasses import dataclass


@dataclass
class MusicContext:
    """Structured representation of musical intent from natural language."""
    
    # Basic parameters
    genre: str = ""
    mood: tp.List[str] = None
    tempo: tp.Optional[int] = None
    key: tp.Optional[str] = None
    time_signature: str = "4/4"
    
    # Instrumentation
    instruments: tp.Dict[str, tp.List[str]] = None
    
    # Style descriptors
    energy_level: float = 0.5  # 0.0 to 1.0
    style_tags: tp.List[str] = None
    
    def __post_init__(self):
        if self.mood is None:
            self.mood = []
        if self.instruments is None:
            self.instruments = {}
        if self.style_tags is None:
            self.style_tags = []


class PromptProcessor:
    """
    Processes natural language prompts into structured musical context
    and generates track-specific prompts for MusicGen.
    
    This is a key component that enables ResonantGen's natural language interface.
    """
    
    def __init__(self):
        # Genre keywords
        self.genre_patterns = {
            "lo-fi": ["lo-fi", "lofi", "low-fi"],
            "hip-hop": ["hip-hop", "hiphop", "hip hop", "rap"],
            "techno": ["techno", "electronic", "edm"],
            "jazz": ["jazz", "jazzy"],
            "ambient": ["ambient", "atmospheric", "ethereal"],
            "rock": ["rock", "guitar"],
            "pop": ["pop", "catchy"],
            "classical": ["classical", "orchestral", "symphony"],
            "reggae": ["reggae", "dub"],
            "funk": ["funk", "funky", "groove"]
        }
        
        # Mood keywords
        self.mood_patterns = {
            "chill": ["chill", "relaxed", "laid back", "calm"],
            "dark": ["dark", "moody", "brooding"],
            "uplifting": ["uplifting", "happy", "bright", "positive"],
            "aggressive": ["aggressive", "intense", "driving", "hard"],
            "dreamy": ["dreamy", "floating", "ethereal", "atmospheric"],
            "energetic": ["energetic", "high energy", "pumping", "powerful"]
        }
        
        # Instrument keywords for each track type
        self.instrument_patterns = {
            "drums": ["drums", "kick", "snare", "hihat", "percussion", "rhythm"],
            "bass": ["bass", "bassline", "sub", "low end", "808"],
            "harmony": ["chords", "harmony", "keys", "piano", "pads", "strings"],
            "melody": ["melody", "lead", "solo", "hook", "riff"]
        }
    
    def analyze(self, prompt: str) -> MusicContext:
        """
        Analyze a natural language prompt and extract musical context.
        
        Args:
            prompt: Natural language description of music
            
        Returns:
            MusicContext with extracted musical information
        """
        prompt_lower = prompt.lower()
        
        # Extract basic parameters
        genre = self._extract_genre(prompt_lower)
        mood = self._extract_mood(prompt_lower) 
        tempo = self._extract_tempo(prompt_lower)
        key = self._extract_key(prompt_lower)
        
        # Extract instrumentation hints
        instruments = self._extract_instruments(prompt_lower)
        
        # Extract style descriptors
        style_tags = self._extract_style_tags(prompt_lower)
        energy_level = self._estimate_energy_level(mood, style_tags)
        
        return MusicContext(
            genre=genre,
            mood=mood,
            tempo=tempo,
            key=key,
            instruments=instruments,
            style_tags=style_tags,
            energy_level=energy_level
        )
    
    def create_track_prompts(self, context: MusicContext) -> tp.Dict[str, str]:
        """
        Create track-specific prompts for MusicGen based on musical context.
        
        Args:
            context: Analyzed musical context
            
        Returns:
            Dictionary mapping track names to specific prompts
        """
        base_style = self._create_base_style_string(context)
        
        prompts = {}
        
        # Drums prompt
        drums_style = self._get_drum_style(context)
        prompts["drums"] = f"drums only, {drums_style}, {base_style}, no bass no melody no harmony"
        
        # Bass prompt  
        bass_style = self._get_bass_style(context)
        prompts["bass"] = f"bass line only, {bass_style}, {base_style}, no drums no melody no harmony"
        
        # Harmony prompt
        harmony_style = self._get_harmony_style(context)
        prompts["harmony"] = f"chord progression only, {harmony_style}, {base_style}, no drums no bass no melody"
        
        # Melody prompt
        melody_style = self._get_melody_style(context)
        prompts["melody"] = f"melody only, {melody_style}, {base_style}, no drums no bass no harmony"
        
        return prompts
    
    def create_regeneration_prompt(self, 
                                   track_name: str,
                                   new_description: str,
                                   locked_context: tp.Dict[str, tp.Any],
                                   original_context: MusicContext) -> str:
        """
        Create a prompt for regenerating a specific track while respecting locked tracks.
        
        Args:
            track_name: Name of track to regenerate
            new_description: New description for this track
            locked_context: Context from locked tracks
            original_context: Original musical context
            
        Returns:
            Track-specific prompt for regeneration
        """
        base_style = self._create_base_style_string(original_context)
        
        # Add tempo/key constraints from locked tracks if available
        constraints = []
        if locked_context.get("locked_track_names"):
            constraints.append("matching tempo and key")
            
        # Create exclusions for other track types
        other_tracks = ["drums", "bass", "harmony", "melody"]
        other_tracks.remove(track_name)
        exclusions = f"no {' no '.join(other_tracks)}"
        
        # Combine everything
        constraint_str = ", ".join(constraints) if constraints else ""
        if constraint_str:
            constraint_str = f", {constraint_str}"
        
        return f"{track_name} only, {new_description}, {base_style}{constraint_str}, {exclusions}"
    
    def _extract_genre(self, prompt: str) -> str:
        """Extract genre from prompt."""
        for genre, patterns in self.genre_patterns.items():
            for pattern in patterns:
                if pattern in prompt:
                    return genre
        return "electronic"  # default
    
    def _extract_mood(self, prompt: str) -> tp.List[str]:
        """Extract mood descriptors from prompt."""
        moods = []
        for mood, patterns in self.mood_patterns.items():
            for pattern in patterns:
                if pattern in prompt:
                    moods.append(mood)
                    break
        return moods or ["neutral"]
    
    def _extract_tempo(self, prompt: str) -> tp.Optional[int]:
        """Extract tempo from prompt."""
        # Look for patterns like "120 BPM", "at 90bpm", "72 beats per minute"
        tempo_patterns = [
            r'(\d+)\s*bpm',
            r'(\d+)\s*beats per minute',
            r'at\s+(\d+)',
            r'(\d+)\s*(beat|tempo)'
        ]
        
        for pattern in tempo_patterns:
            match = re.search(pattern, prompt)
            if match:
                return int(match.group(1))
        
        return None
    
    def _extract_key(self, prompt: str) -> tp.Optional[str]:
        """Extract key signature from prompt."""
        # Look for key signatures like "in C minor", "A major", "Dm"
        key_patterns = [
            r'in\s+([A-G][#b]?)\s+(major|minor)',
            r'([A-G][#b]?)\s+(major|minor)',
            r'([A-G][#b]?m)\b',  # Shorthand like "Dm"
        ]
        
        for pattern in key_patterns:
            match = re.search(pattern, prompt)
            if match:
                if len(match.groups()) == 2:
                    return f"{match.group(1)}_{match.group(2)}"
                else:
                    return match.group(1)
        
        return None
    
    def _extract_instruments(self, prompt: str) -> tp.Dict[str, tp.List[str]]:
        """Extract instrument mentions for each track type."""
        instruments = {}
        
        for track_type, patterns in self.instrument_patterns.items():
            found_instruments = []
            for pattern in patterns:
                if pattern in prompt:
                    found_instruments.append(pattern)
            
            if found_instruments:
                instruments[track_type] = found_instruments
        
        return instruments
    
    def _extract_style_tags(self, prompt: str) -> tp.List[str]:
        """Extract style descriptors."""
        style_words = [
            "analog", "digital", "vintage", "modern", "retro",
            "warm", "cold", "punchy", "smooth", "rough",
            "swing", "straight", "triplets", "syncopated"
        ]
        
        found_styles = []
        for style in style_words:
            if style in prompt:
                found_styles.append(style)
        
        return found_styles
    
    def _estimate_energy_level(self, moods: tp.List[str], styles: tp.List[str]) -> float:
        """Estimate energy level from mood and style."""
        energy_map = {
            "chill": 0.3,
            "dark": 0.6,
            "aggressive": 0.9,
            "uplifting": 0.7,
            "energetic": 0.8,
            "dreamy": 0.4
        }
        
        if not moods:
            return 0.5
        
        energies = [energy_map.get(mood, 0.5) for mood in moods]
        return sum(energies) / len(energies)
    
    def _create_base_style_string(self, context: MusicContext) -> str:
        """Create base style string from context."""
        parts = []
        
        if context.genre:
            parts.append(context.genre)
        
        if context.mood:
            parts.extend(context.mood)
        
        if context.tempo:
            parts.append(f"{context.tempo} BPM")
        
        if context.style_tags:
            parts.extend(context.style_tags[:2])  # Limit to avoid too long prompts
        
        return ", ".join(parts)
    
    def _get_drum_style(self, context: MusicContext) -> str:
        """Get drum-specific style based on context."""
        if context.genre == "lo-fi":
            return "laid back swing, vintage drum samples"
        elif context.genre == "techno":
            return "four on the floor kick, electronic percussion"
        elif context.genre == "hip-hop":
            return "boom bap pattern, punchy snare"
        else:
            return "rhythmic pattern"
    
    def _get_bass_style(self, context: MusicContext) -> str:
        """Get bass-specific style based on context."""
        if context.genre == "lo-fi":
            return "warm analog bass, smooth low end"
        elif context.genre == "techno":
            return "driving electronic bass, sub frequencies"
        elif context.genre == "hip-hop":
            return "deep 808 bass, punchy low end"
        else:
            return "bass line"
    
    def _get_harmony_style(self, context: MusicContext) -> str:
        """Get harmony-specific style based on context."""
        if context.genre == "lo-fi":
            return "jazzy chords, warm keys, vintage electric piano"
        elif context.genre == "techno":
            return "atmospheric pads, electronic textures"
        elif context.genre == "jazz":
            return "complex jazz chords, piano comping"
        else:
            return "chord progression"
    
    def _get_melody_style(self, context: MusicContext) -> str:
        """Get melody-specific style based on context."""
        if context.genre == "lo-fi":
            return "subtle melody, atmospheric lead, vinyl texture"
        elif context.genre == "techno":
            return "electronic lead, synthesizer melody"
        elif context.genre == "jazz":
            return "improvised solo, melodic phrases"
        else:
            return "melodic line"