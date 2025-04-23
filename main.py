import tkinter as tk
from tkinter import messagebox
import keyboard
import psutil
import os
import json
import subprocess
import threading
import time
import win32gui
import win32con
import win32process

CONFIG_FILE = 'settings.json'

DEFAULT_HOTKEY = 'ctrl+alt+s'
SPOTIFY_PROCESS_NAME = 'Spotify.exe'
SPOTIFY_EXECUTABLE = os.path.expandvars(r"%AppData%\Spotify\Spotify.exe")

# === Core functions ===
def close_spotify():
    def enum_windows_callback(hwnd, pid_list):
        try:
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid in pid_list:
                win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        except Exception as e:
            print ("Window enumeration error: ", e)

    spotify_pids = [
        proc.pid for proc in psutil.process_iter(['name'])
        if proc.info['name'] and 'spotify.exe' in proc.info['name'].lower()
    ]

    if not spotify_pids:
        print("Spotify is not running")
        return
    
    win32gui.EnumWindows(enum_windows_callback, spotify_pids)
    print("Succesfully closed Spotify")


def open_spotify():
    if os.path.exists(SPOTIFY_EXECUTABLE):
        subprocess.Popen(
            [SPOTIFY_EXECUTABLE],
            close_fds=True,
            creationflags=subprocess.DETACHED_PROCESS
        )
        status_label.config(text="Spotify opened")
    else:
        messagebox.showerror("Error", "Spotify executable not found.")

def reopen_spotify():
    close_spotify()
    time.sleep(3)
    open_spotify()

def update_status(status):
    status_label.config(text=status)

# === Settings ===
def load_settings():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            settings = json.load(f)
    else: 
        settings = DEFAULT_HOTKEY
        save_settings(settings)
    return settings

# Open 'settings.json' and write the settings in there.
def save_settings(settings):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(settings, f)

# === Hotkey ===
def listen_for_hotkey(hotkey):
    def handler():
        reopen_spotify()
    keyboard.add_hotkey(hotkey, handler)
    keyboard.wait()

def update_hotkey():
    new_hotkey = hotkey_entry.get().strip()
    if new_hotkey:
        keyboard.clear_all_hotkeys()
        save_settings(new_hotkey)
        threading.Thread(target=listen_for_hotkey, args=(new_hotkey,), daemon=None).start()

# === UI Setup ===
root = tk.Tk()
root.title("Spotify ad skipper")
root.geometry("400x250")
root.resizable(False, False)

tk.Label(root, text="Set Your Hotkey (e.g., ctrl+alt+s):", font=("Arial", 16)).pack(pady=(10,0))
hotkey_entry = tk.Entry(root, width=30)
hotkey_entry.insert(0, DEFAULT_HOTKEY)
hotkey_entry.pack(pady=5)

tk.Button(root, text="Set Hotkey", command=update_hotkey).pack(pady=5)
tk.Button(root, text="Reopen Spotify", command=reopen_spotify).pack(pady=5)

tk.Button(root, text="Close Spotify", command=close_spotify).pack(pady=5)
tk.Button(root, text="Open Spotify", command=open_spotify).pack(pady=5)

status_label = tk.Label(root, text="Ready", fg="green")
status_label.pack(pady=10)

threading.Thread(target=listen_for_hotkey, args=(DEFAULT_HOTKEY,), daemon=None).start()

root.mainloop()