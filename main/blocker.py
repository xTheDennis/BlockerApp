import time
import tkinter as tk
import threading
import winsound
import pygetwindow as gw
import os
from updater import check_for_updates

check_for_updates()

# Seiten, die blockiert werden sollen
DANGEROUS_SITES = ["stake", "stake.com", "rainbet", "rainbet.com"]

# Liste der Browser-Prozesse, die sofort beendet werden sollen
BROWSERS_TO_KILL = ["chrome.exe", "msedge.exe", "opera.exe"]

# Ton abspielen (nervig)
def play_warning_sound():
    duration = 1000  # ms
    freq = 1000  # Hz
    for _ in range(5):
        winsound.Beep(freq, duration)

# Schwarzer Bildschirm mit "NEIN"
def show_warning_overlay():
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.configure(bg="black")
    label = tk.Label(root, text="NICHT AUFLADEN", fg="red", bg="black", font=("Arial", 100, "bold"))
    label.pack(expand=True)
    threading.Thread(target=root.after, args=(5000, root.destroy)).start()
    root.mainloop()

# Alle Browser hart beenden
def kill_browsers():
    for browser in BROWSERS_TO_KILL:
        os.system(f"taskkill /f /im {browser}")

# Überwachung der Fenster
def monitor_windows():
    while True:
        try:
            for window in gw.getAllTitles():
                for site in DANGEROUS_SITES:
                    if site.lower() in window.lower():
                        print(f"[!] BLOCKIERT: {site.upper()}")
                        threading.Thread(target=play_warning_sound).start()
                        threading.Thread(target=show_warning_overlay).start()
                        kill_browsers()
                        time.sleep(6)  # Cooldown
        except Exception as e:
            print(f"Fehler: {e}")
        time.sleep(1)

if __name__ == "__main__":
    print("🚫 Ultra-Harter Wächter aktiviert...")
    monitor_windows()
