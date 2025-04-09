import keyboard
import psutil
import os
import time

def close_Spotify():
    closed = False
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and 'spotify.exe' in proc.info['name'].lower():
            try:
                proc.terminate()
                print("Spotify has been closed.")
            except (psutil.NoSuchProcess, psutil.AccesDenied):
                print("Could not close Spotify")
    if not closed:
        print("Spotify was not running.")

keyboard.add_hotkey('ctrl+alt+s', close_Spotify)

print("Press Ctrl + Alt + S to close Spotify.")
print("Press Esc to exit.")

keyboard.wait('esc')