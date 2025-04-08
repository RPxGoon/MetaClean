import os
import subprocess
import sys
import platform

def install_requirements():
    """Install dependencies from requirements.txt."""
    requirements_file = "requirements.txt"
    
    if not os.path.exists(requirements_file):
        print(f"Error: {requirements_file} not found in the current directory.")
        sys.exit(1)
    
    try:
        print("Installing dependencies from requirements.txt...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
        print("All dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while installing dependencies: {e}")
        sys.exit(1)

def install_ffmpeg():
    """Install FFmpeg based on the platform (macOS, Windows, Linux)."""
    system_platform = platform.system()

    try:
        if system_platform == "Darwin":  # macOS
            print("Installing FFmpeg for macOS...")
            # Check if Homebrew is installed
            try:
                subprocess.check_call(["which", "brew"])
            except subprocess.CalledProcessError:
                # Install Homebrew if not installed
                subprocess.check_call(["/bin/bash", "-c", 
                    "curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh | bash"])
            # Install FFmpeg using Homebrew
            subprocess.check_call(["brew", "install", "ffmpeg"])
        elif system_platform == "Windows":
            print("Installing FFmpeg for Windows...")
            # Use winget to install FFmpeg
            subprocess.check_call(["winget", "install", "ffmpeg"])
        elif system_platform == "Linux":
            print("Installing FFmpeg for Linux...")
            # Check for the distribution and install via apt or dnf
            dist_name = subprocess.check_output(["lsb_release", "-i"]).decode("utf-8").strip().split(":")[1].strip()
            if dist_name.lower() in ["ubuntu", "debian"]:
                subprocess.check_call(["sudo", "apt", "update"])
                subprocess.check_call(["sudo", "apt", "install", "-y", "ffmpeg"])
            elif dist_name.lower() in ["fedora"]:
                subprocess.check_call(["sudo", "dnf", "install", "-y", "ffmpeg"])
            else:
                print(f"Unsupported Linux distribution: {dist_name}")
                sys.exit(1)
        else:
            print(f"Unsupported platform: {system_platform}")
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while installing FFmpeg: {e}")
        sys.exit(1)

def run_main_tool():
    main_file = "metaclean.py"
    
    if not os.path.exists(main_file):
        print(f"Error: {main_file} not found in the current directory.")
        sys.exit(1)
    
    try:
        print(f"Running {main_file}...")
        subprocess.check_call([sys.executable, main_file])
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {main_file}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_ffmpeg()  
    install_requirements()
    run_main_tool()