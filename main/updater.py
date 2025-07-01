import requests
import os
import shutil
import sys

__version__ = "1.0.1"  # Aktuelle Version des Programms

def check_for_updates():
    version_url = "https://github.com/xTheDennis/BlockerApp/releases/latest/download/version.txt"
    exe_url = "https://github.com/xTheDennis/BlockerApp/releases/latest/download/blocker.exe"

    try:
        remote_version = requests.get(version_url, timeout=5).text.strip()
        if remote_version > __version__:
            print(f"Neue Version {remote_version} gefunden – Update wird geladen...")
            r = requests.get(exe_url, stream=True, timeout=10)
            with open("update_blocker.exe", "wb") as f:
                shutil.copyfileobj(r.raw, f)
            print("Update abgeschlossen. Starte neue Version...")
            os.startfile("update_blocker.exe")
            sys.exit()
    except Exception as e:
        print("Update-Check fehlgeschlagen:", e)
