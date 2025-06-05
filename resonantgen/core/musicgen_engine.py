"""
MusicGen Engine - Clean wrapper around MusicGen for ResonantGen

Provides a clean interface to MusicGen's generation capabilities
optimized for multi-track generation.
"""

import torch
import typing as tp
from transformers import MusicgenForConditionalGeneration, AutoProcessor


class MusicGenEngine:
    """
    Clean wrapper around MusicGen for ResonantGen's multi-track generation.
    
    This class provides a simplified interface to MusicGen that's optimized
    for our track-specific generation needs.
    """
    
    def __init__(self, model_size: str = "small", device: torch.device = None):
        """
        Initialize the MusicGen engine.
        
        Args:
            model_size: Size of model ("small", "medium", "large") 
            device: Torch device to run on
        """
        self.model_size = model_size
        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Load model and processor
        model_name = f"facebook/musicgen-{model_size}"
        print(f"Loading MusicGen {model_size} model...")
        
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.model = MusicgenForConditionalGeneration.from_pretrained(model_name)
        self.model.to(self.device)
        
        # Set generation parameters
        self.sample_rate = self.model.config.audio_encoder.sampling_rate
        self.max_new_tokens = 512  # ~8 seconds of audio
        
        print(f"✅ MusicGen {model_size} loaded on {self.device}")
        print(f"   Sample rate: {self.sample_rate}Hz")
    
    def generate(self, prompt: str, duration: float = 8.0) -> torch.Tensor:
        """
        Generate audio from text prompt.
        
        Args:
            prompt: Text description of the music to generate
            duration: Duration in seconds (approximate)
            
        Returns:
            Audio tensor [1, samples] at model's sample rate
        """
        # Calculate tokens needed for duration
        # Rough estimate: ~32 tokens per second
        tokens_needed = int(duration * 32)
        tokens_needed = min(tokens_needed, 1024)  # Cap at model limit
        
        # Process prompt
        inputs = self.processor(
            text=[prompt],
            padding=True,
            return_tensors="pt"
        ).to(self.device)
        
        # Generate with no_grad for efficiency
        with torch.no_grad():
            audio_values = self.model.generate(
                **inputs,
                max_new_tokens=tokens_needed,
                do_sample=True,
                guidance_scale=1.5,  # Lower = more natural, less "evil" sound
                temperature=1.2,     # Slightly higher for musical variety
                top_k=250,          # Limit choices for coherence
                top_p=0.95          # Nucleus sampling for better quality
            )
        
        # Return single audio tensor
        return audio_values[0].cpu()  # [1, samples]
    
    def generate_batch(self, prompts: tp.List[str], duration: float = 8.0) -> tp.List[torch.Tensor]:
        """
        Generate multiple tracks in parallel for efficiency.
        
        Args:
            prompts: List of text prompts
            duration: Duration for each track
            
        Returns:
            List of audio tensors
        """
        tokens_needed = int(duration * 32)
        tokens_needed = min(tokens_needed, 1024)
        
        # Process all prompts
        inputs = self.processor(
            text=prompts,
            padding=True,
            return_tensors="pt"
        ).to(self.device)
        
        # Generate all at once
        with torch.no_grad():
            audio_values = self.model.generate(
                **inputs,
                max_new_tokens=tokens_needed,
                do_sample=True,
                guidance_scale=1.5,
                temperature=1.2,
                top_k=250,
                top_p=0.95
            )
        
        # Return list of individual tracks
        return [audio[None] for audio in audio_values.cpu()]
    
    def set_generation_params(self, **kwargs):
        """Update generation parameters."""
        if 'max_new_tokens' in kwargs:
            self.max_new_tokens = kwargs['max_new_tokens']
        if 'guidance_scale' in kwargs:
            self.guidance_scale = kwargs['guidance_scale']
        if 'temperature' in kwargs:
            self.temperature = kwargs['temperature']
    
    def get_model_info(self) -> dict:
        """Get information about the loaded model."""
        return {
            "model_size": self.model_size,
            "sample_rate": self.sample_rate,
            "device": str(self.device),
            "max_tokens": self.max_new_tokens,
            "parameters": sum(p.numel() for p in self.model.parameters()) / 1e6
        }