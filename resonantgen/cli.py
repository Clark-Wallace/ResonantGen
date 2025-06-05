#!/usr/bin/env python3
"""
ResonantGen Phase 0 CLI - Musical Telepathy MVP

Jordan's workflow in under 60 seconds:
1. prompt "lo-fi beat description"
2. lock bass
3. regenerate drums  
4. export session_01
"""

import sys
import os
import time
from pathlib import Path
from typing import Optional, Dict

from .core.workstation import MusicWorkstation
from .core.track_session import TrackSession


class ResonantCLI:
    """Phase 0 CLI Interface - The minimum viable telepathy."""
    
    def __init__(self):
        self.workstation: Optional[MusicWorkstation] = None
        self.session: Optional[TrackSession] = None
        self.session_counter = 1
        self.start_time = time.time()
        
        print("\n🎵 ResonantGen - Musical Telepathy Phase 0")
        print("   Thought → Sound in under 60 seconds\n")
        
        # Initialize workstation
        print("Initializing musical consciousness...")
        self.workstation = MusicWorkstation(model_size="small")
        print("✅ Ready for telepathy\n")
        
    def prompt(self, description: str):
        """Generate music from natural language."""
        print(f"🧠 Processing: '{description}'")
        print("   Translating thought to sound...\n")
        
        # Generate tracks
        self.session = self.workstation.generate(description, duration=8.0)
        
        # Save to session folder
        session_name = f"session_{self.session_counter:02d}"
        session_path = Path("loops") / session_name
        session_path.mkdir(parents=True, exist_ok=True)
        
        # Export individual tracks
        for track_name, track in self.session.tracks.items():
            track_path = session_path / f"{track_name}.wav"
            track.export(str(track_path))
        
        print(f"\n✅ Generated loop saved to /loops/{session_name}/")
        print("   📁 drums.wav, bass.wav, harmony.wav, melody.wav")
        
        # Show elapsed time
        elapsed = time.time() - self.start_time
        print(f"   ⏱️  {elapsed:.1f} seconds elapsed\n")
        
    def lock(self, track_name: str):
        """Lock a track to preserve it during regeneration."""
        if not self.session:
            print("❌ No active session. Use 'prompt' first.\n")
            return
            
        # Handle 'chords' alias for 'harmony'
        if track_name == "chords":
            track_name = "harmony"
            
        if track_name not in self.session.tracks:
            print(f"❌ Track '{track_name}' not found.")
            print(f"   Available: {', '.join(self.session.tracks.keys())}\n")
            return
            
        self.session.lock(track_name)
        print(f"✅ Locked: {track_name}\n")
        
    def regenerate(self, track_name: str, description: Optional[str] = None):
        """Regenerate a specific track with optional new description."""
        if not self.session:
            print("❌ No active session. Use 'prompt' first.\n")
            return
            
        # Handle 'chords' alias for 'harmony'
        if track_name == "chords":
            track_name = "harmony"
            
        if track_name not in self.session.tracks:
            print(f"❌ Track '{track_name}' not found.")
            print(f"   Available: {', '.join(self.session.tracks.keys())}\n")
            return
            
        if self.session[track_name].is_locked:
            print(f"❌ Track '{track_name}' is locked. Unlock it first.\n")
            return
            
        # Use description or default regeneration prompt
        regen_prompt = description or f"different {track_name} pattern"
        
        print(f"🔄 Regenerating {track_name}...")
        new_track = self.workstation.regenerate(track_name, regen_prompt)
        
        # Update session folder
        session_name = f"session_{self.session_counter:02d}"
        session_path = Path("loops") / session_name
        track_path = session_path / f"{track_name}.wav"
        new_track.export(str(track_path))
        
        print(f"✅ Regenerated: {track_name}\n")
        
        # Show elapsed time
        elapsed = time.time() - self.start_time
        print(f"   ⏱️  {elapsed:.1f} seconds elapsed\n")
        
    def export(self, session_name: Optional[str] = None):
        """Export the current session."""
        if not self.session:
            print("❌ No active session. Use 'prompt' first.\n")
            return
            
        if not session_name:
            session_name = f"session_{self.session_counter:02d}"
            
        print(f"💾 Exporting {session_name}...")
        
        # Session already saved during generation
        session_path = Path("loops") / session_name
        
        # Also create a mixed version
        mixed_path = session_path / "mixed.wav"
        self.session.export(str(mixed_path), stems=False)
        
        print(f"\n✅ Exported to /loops/{session_name}/")
        print("   📁 Individual tracks + mixed.wav")
        
        # Final timing
        total_time = time.time() - self.start_time
        print(f"\n🎯 Total time: {total_time:.1f} seconds")
        
        if total_time < 60:
            print("   ✨ Under 60 seconds - Musical telepathy achieved!\n")
        else:
            print("   ⚡ Optimize for sub-60 second workflow\n")
            
        # Increment session counter for next session
        self.session_counter += 1
        self.start_time = time.time()
        
    def run(self):
        """Run the CLI interface."""
        print("Type 'help' for commands, 'quit' to exit\n")
        
        while True:
            try:
                # Get command
                cmd_input = input("resonant> ").strip()
                
                if not cmd_input:
                    continue
                    
                # Parse command and arguments
                parts = cmd_input.split(None, 1)
                cmd = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""
                
                # Handle commands
                if cmd == "quit" or cmd == "exit":
                    print("\n👋 Musical consciousness fading...\n")
                    break
                    
                elif cmd == "help":
                    self.show_help()
                    
                elif cmd == "prompt":
                    if not args:
                        print("❌ Usage: prompt <description>\n")
                    else:
                        self.prompt(args)
                        
                elif cmd == "lock":
                    if not args:
                        print("❌ Usage: lock <track_name>\n")
                    else:
                        self.lock(args)
                        
                elif cmd == "regenerate":
                    track_parts = args.split(None, 1)
                    if not track_parts:
                        print("❌ Usage: regenerate <track_name> [description]\n")
                    else:
                        track_name = track_parts[0]
                        description = track_parts[1] if len(track_parts) > 1 else None
                        self.regenerate(track_name, description)
                        
                elif cmd == "export":
                    self.export(args if args else None)
                    
                else:
                    print(f"❌ Unknown command: '{cmd}'. Type 'help' for commands.\n")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Musical consciousness fading...\n")
                break
            except Exception as e:
                print(f"❌ Error: {e}\n")
                
    def show_help(self):
        """Show help information."""
        print("""
🎵 ResonantGen Commands:

  prompt <description>    Generate music from natural language
                         Example: prompt chill lo-fi beat at 72 bpm
                         
  lock <track>           Lock a track to preserve during regeneration
                         Tracks: drums, bass, harmony/chords, melody
                         
  regenerate <track>     Regenerate an unlocked track
                         Example: regenerate drums
                         
  export [name]          Export session to /loops/ folder
                         Creates individual tracks + mixed.wav
                         
  help                   Show this help message
  quit                   Exit ResonantGen

🎯 Jordan's Workflow:
  1. prompt "lo-fi hip-hop beat with jazzy chords"
  2. lock bass
  3. regenerate drums
  4. export
  
⏱️  Goal: Complete workflow in under 60 seconds!
""")


def main():
    """Entry point for the CLI."""
    cli = ResonantCLI()
    cli.run()


if __name__ == "__main__":
    main()