import os
import shutil
import subprocess

REPO = "xTheDennis/BlockerApp"  # Dein GitHub-Repo
VERSION_FILE = "../version.txt"
EXE_NAME = "blocker.exe"
EXE_PATH = f"../dist/{EXE_NAME}"

def read_version():
    with open(VERSION_FILE, "r") as f:
        return f.read().strip()

def bump_version(version):
    major, minor, patch = map(int, version.split("."))
    patch += 1
    return f"{major}.{minor}.{patch}"

def write_version(new_version):
    with open(VERSION_FILE, "w") as f:
        f.write(new_version)

def build_exe():
    subprocess.run([
        "python", "-m", 
        "PyInstaller",
        "--onefile",
        "--noconsole",
        "--distpath", "../dist",
        "--workpath", "../build",
        "blocker.py"
    ], check=True)

def upload_to_github(new_version):
    os.system(f"gh release delete v{new_version} -y --repo {REPO}")
    os.system(
        f'gh release create v{new_version} {EXE_PATH} {VERSION_FILE} '
        f'--title "Version {new_version}" '
        f'--notes "Automatisch generierter Release" '
        f'--repo {REPO}'
    )

def main():
    print("📦 Starte automatisierten Build- & Release-Prozess...")

    current_version = read_version()
    print(f"📄 Aktuelle Version: {current_version}")

    new_version = bump_version(current_version)
    write_version(new_version)
    print(f"⬆️  Neue Version: {new_version}")

    print("🔨 Baue neue EXE...")
    build_exe()

    print("🚀 Lade Release hoch...")
    upload_to_github(new_version)

    print("✅ Fertig! Version", new_version, "wurde veröffentlicht.")

if __name__ == "__main__":
    main()
