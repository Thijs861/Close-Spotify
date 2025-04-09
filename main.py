import keyboard
import psutil
import os
import subprocess
import time
from pathlib import Path

def get_spotify_path():
    user_profile = os.environ.get('USERPROFILE')
    default_path = Path(user_profile) / "AppData" / "Roaming" / "Spotify" / "Spotify.exe"
    if default_path.exists():
        return str(default_path)
    else: 
        print("Spotify.exe not found at the default location.")
        return None

def close_Spotify():
    closed = False
    # Search for all running processes on your system and sort them by name.
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and 'spotify.exe' in proc.info['name'].lower():
            try:
                proc.terminate() # Close Spotify.
                closed = True
                print("Spotify has been closed.")
            except (psutil.NoSuchProcess, psutil.AccesDenied):
                print("Could not close Spotify") # If the program failed, return an error
    if not closed:
        print("Spotify was not running.")
    else: 
        reopen_spotify()

def reopen_spotify(delay=3):
    print(f"Reopening Spotify in {delay} seconds...")
    time.sleep(delay)
    spotify_path = get_spotify_path()
    if spotify_path:
        try:
            subprocess.Popen(spotify_path)
        except Exception as e:
            print(f"Failed to launch Spotify: {e}")

# Hotkey for closing Spotify.
keyboard.add_hotkey('ctrl+alt+s', close_Spotify)

print("Press Ctrl + Alt + S to close Spotify.")
print("Press Esc to exit.")

keyboard.wait('esc')