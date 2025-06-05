#!/usr/bin/env python3
"""Utility for managing ResonantGen outputs."""

import os
import shutil
from pathlib import Path
from datetime import datetime

def create_session_dir(name: str = None) -> Path:
    """Create a new timestamped session directory."""
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
    if name:
        dir_name = f"session_{timestamp}_{name}"
    else:
        dir_name = f"session_{timestamp}"
    
    session_dir = Path(f"outputs/sessions/{dir_name}")
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir

def create_test_dir(test_name: str) -> Path:
    """Create a new timestamped test directory."""
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
    test_dir = Path(f"outputs/tests/{test_name}_{timestamp}")
    test_dir.mkdir(parents=True, exist_ok=True)
    return test_dir

def list_sessions():
    """List all generated sessions."""
    sessions_dir = Path("outputs/sessions")
    if not sessions_dir.exists():
        print("No sessions found.")
        return
    
    sessions = sorted(sessions_dir.glob("session_*"))
    print(f"Found {len(sessions)} sessions:")
    for session in sessions:
        wav_files = list(session.glob("*.wav"))
        print(f"  {session.name} ({len(wav_files)} files)")

def clean_temp():
    """Clean temporary files."""
    temp_dir = Path("temp")
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
        temp_dir.mkdir()
        print("✅ Cleaned temp directory")

def export_session(session_name: str, export_name: str):
    """Export a session to the exports directory."""
    session_dir = Path(f"outputs/sessions/{session_name}")
    if not session_dir.exists():
        print(f"❌ Session {session_name} not found")
        return
    
    export_dir = Path(f"outputs/exports/{export_name}")
    export_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy all wav files
    for wav_file in session_dir.glob("*.wav"):
        shutil.copy2(wav_file, export_dir)
    
    print(f"✅ Exported {session_name} to exports/{export_name}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python scripts/output_manager.py list")
        print("  python scripts/output_manager.py clean")
        print("  python scripts/output_manager.py export <session_name> <export_name>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "list":
        list_sessions()
    elif command == "clean":
        clean_temp()
    elif command == "export" and len(sys.argv) == 4:
        export_session(sys.argv[2], sys.argv[3])
    else:
        print("Invalid command")