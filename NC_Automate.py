import os
import platform
import subprocess
import sys
import shutil

# Define the network commander script to be created
NETWORK_COMMANDER_SCRIPT = """
import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import subprocess
import pyttsx3
import speech_recognition as sr
import pandas as pd
import os
import time
import webbrowser  # For WhatsApp support link
import platform  # For platform-specific commands

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Set speech rate

# Global variables for voice control state
voice_control_active = False
paused = False
dynamic_ip_updating = False

# Ethical consideration function
def ethical_warning():
    engine.say("Please ensure you have permission to execute network commands.")
    engine.runAndWait()

# Function to run commands and display output
def run_command(command):
    try:
        ethical_warning()
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output_text.delete(1.0, tk.END)  # Clear previous output
        output_text.insert(tk.END, result.stdout)
        engine.say(f"Command executed: {command}")
        engine.runAndWait()
    except Exception as e:
        output_text.insert(tk.END, f"Error: {e}")
        engine.say(f"Error executing command: {e}")
        engine.runAndWait()

# Other functions (rest of networkcommander.py script here)

# Start the main loop
root.mainloop()
"""

def install_linux():
    print("Detected Linux. Installing dependencies...")

    try:
        print("Updating package list and installing dependencies...")
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run(["sudo", "apt", "install", "-y", "python3-tk", "openvpn"], check=True)
    except Exception as e:
        print(f"Error installing system packages on Linux: {e}")

    install_python_dependencies()

def install_mac():
    print("Detected macOS. Installing dependencies...")

    try:
        if subprocess.run(["brew", "--version"], check=True, capture_output=True).returncode != 0:
            print("Homebrew not found. Installing Homebrew...")
            subprocess.run(
                '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
                shell=True,
                check=True
            )
        subprocess.run(["brew", "install", "openvpn"], check=True)
    except Exception as e:
        print(f"Error installing system packages on macOS: {e}")

    install_python_dependencies()

def install_windows():
    print("Detected Windows. Installing dependencies...")

    try:
        print("You need to install OpenVPN manually from: https://openvpn.net/community-downloads/")
        webbrowser.open("https://openvpn.net/community-downloads/")
    except Exception as e:
        print(f"Error opening OpenVPN download page on Windows: {e}")

    install_python_dependencies()

def install_python_dependencies():
    print("Installing Python packages...")

    packages = [
        "pyttsx3", "SpeechRecognition", "pandas", "requests", "tk", "webbrowser"
    ]

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + packages)
        print("All Python dependencies installed successfully.")
    except Exception as e:
        print(f"Error installing Python packages: {e}")

def create_network_commander_script(folder_path):
    """Create the networkcommander.py script in the target folder."""
    try:
        script_path = os.path.join(folder_path, "networkcommander.py")
        with open(script_path, "w") as script_file:
            script_file.write(NETWORK_COMMANDER_SCRIPT)
        print(f"'networkcommander.py' created at {script_path}.")
    except Exception as e:
        print(f"Error creating 'networkcommander.py': {e}")

def get_desktop_folder():
    """Determine the desktop folder path depending on the platform."""
    desktop_folder = ""
    if platform.system().lower() == "windows":
        desktop_folder = os.path.join(os.environ["USERPROFILE"], "Desktop")
    elif platform.system().lower() == "darwin":  # macOS
        desktop_folder = os.path.join(os.path.expanduser("~"), "Desktop")
    elif platform.system().lower() == "linux":
        desktop_folder = os.path.join(os.path.expanduser("~"), "Desktop")

    return desktop_folder

def create_network_commander_folder():
    """Create the NetworkCommander folder on the desktop."""
    desktop_folder = get_desktop_folder()

    if not desktop_folder:
        print("Unable to determine the desktop folder.")
        return ""

    # Create the NetworkCommander folder on the desktop
    network_commander_folder = os.path.join(desktop_folder, "NetworkCommander")
    try:
        os.makedirs(network_commander_folder, exist_ok=True)
        print(f"NetworkCommander folder created at {network_commander_folder}.")
        return network_commander_folder
    except Exception as e:
        print(f"Error creating NetworkCommander folder: {e}")
        return ""

def main():
    current_os = platform.system().lower()

    if "linux" in current_os:
        install_linux()
    elif "darwin" in current_os:  # macOS detection
        install_mac()
    elif "windows" in current_os:
        install_windows()
    else:
        print(f"Unsupported operating system: {current_os}")
        sys.exit(1)

    # Create the NetworkCommander folder on the desktop
    network_commander_folder = create_network_commander_folder()
    if network_commander_folder:
        create_network_commander_script(network_commander_folder)
        print(f"Setup complete. You can now run 'networkcommander.py' from {network_commander_folder}.")

if __name__ == "__main__":
    main()
