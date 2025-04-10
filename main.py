import tkinter as tk
from tkinter import messagebox
import keyboard
import psutil
import os
import subprocess
import threading
import time

DEFAULT_HOTKEY = 'ctrl+alt+s'
SPOTIFY_PROCESS_NAME = 'Spotify.exe'
SPOTIFY_EXECUTABLE = os.path.expandvars(r"%AppData%\Spotify\Spotify.exe")

# === Core functions ===
def close_spotify():
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

def open_spotify():
    if os.path.exists(SPOTIFY_EXECUTABLE):
        subprocess.Popen([SPOTIFY_EXECUTABLE])
        status_label.config(text="Spotify opened")
    else:
        messagebox.showerror("Error, Spotify executable not found.")

def reopen_spotify():
    close_spotify()
    time.sleep(3)
    open_spotify()

# === Hotkey ===
def listen_for_hotkey(hotkey):
    def handler():
        close_spotify()
    keyboard.add_hotkey(hotkey, handler)
    keyboard.wait()

def update_hotkey():
    new_hotkey = hotkey_entry.get().strip()
    if new_hotkey:
        keyboard.clear_all_hotkeys()
        threading.Thread(target=listen_for_hotkey, args=(new_hotkey,), daemon=True).start()

# === UI Setup ===
root = tk.Tk()
root.title("Spotify ad skipper")
root.geometry("400x250")
root.resizable(False, False)

tk.Label(root, text="Set Your Hotkey (e.g., ctrl+alt+s):").pack(pady=(10,0))
hotkey_entry = tk.Entry(root, width=30)
hotkey_entry.insert(0, DEFAULT_HOTKEY)
hotkey_entry.pack(pady=5)

tk.Button(root, text="Set Hotkey", command=update_hotkey).pack(pady=5)
tk.Button(root, text="Reopen Spotify", command=reopen_spotify).pack(pady=5)

# tk.Button(root, text="Close Spotify", command=close_spotify).pack(pady=5)
# tk.Button(root, text="Open Spotify", command=open_spotify).pack(pady=5)

status_label = tk.Label(root, text="Ready", fg="green")
status_label.pack(pady=10)

threading.Thread(target=listen_for_hotkey, args=(DEFAULT_HOTKEY,), daemon=True).start()

root.mainloop()