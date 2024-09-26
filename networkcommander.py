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

# Function to detect the platform and provide correct command
def get_platform_command(windows_command, unix_command):
    if platform.system().lower() == "windows":
        return windows_command
    else:
        return unix_command

# Function to start voice control
def start_voice_control():
    global voice_control_active, paused
    voice_control_active = True
    paused = False
    engine.say("Voice control activated. Please speak your command.")
    engine.runAndWait()
    listen_for_commands()

# Function to stop voice control
def stop_voice_control():
    global voice_control_active
    voice_control_active = False
    engine.say("Voice control deactivated.")
    engine.runAndWait()

# Function to pause voice control
def pause_voice_control():
    global paused
    paused = True
    engine.say("Voice control paused.")
    engine.runAndWait()

# Function to resume voice control
def resume_voice_control():
    global paused
    paused = False
    engine.say("Voice control resumed.")
    engine.runAndWait()
    listen_for_commands()

# Function to listen for voice commands
def listen_for_commands():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while voice_control_active and not paused:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

            try:
                command = recognizer.recognize_google(audio).lower()
                if 'start' in command:
                    start_voice_control()
                elif 'stop' in command:
                    stop_voice_control()
                elif 'pause' in command:
                    pause_voice_control()
                elif 'resume' in command:
                    resume_voice_control()
                elif 'display all ip configuration' in command:
                    run_command(get_platform_command("ipconfig", "ifconfig"))
                elif 'detailed ip configuration' in command:
                    run_command(get_platform_command("ipconfig /all", "ifconfig -a"))
                elif 'release ip address' in command:
                    run_command(get_platform_command("ipconfig /release", "sudo dhclient -r"))
                elif 'renew ip address' in command:
                    run_command(get_platform_command("ipconfig /renew", "sudo dhclient"))
                elif 'flush dns cache' in command:
                    run_command(get_platform_command("ipconfig /flushdns", "sudo systemd-resolve --flush-caches"))
                elif 'display dns cache' in command:
                    run_command("ipconfig /displaydns")
                elif 'register dns' in command:
                    run_command("ipconfig /registerdns")
                elif 'show network adapters' in command:
                    run_command("ipconfig /allcompartments /all")
                elif 'connect to vpn' in command:
                    upload_vpn_file()
                elif 'disconnect vpn' in command:
                    run_command(get_platform_command("vpnclient disconnect your_vpn_connection_name", "sudo pkill openvpn"))
                elif 'set proxy' in command:
                    run_command("netsh winhttp set proxy proxy_server_address")
                elif 'clear proxy' in command:
                    run_command("netsh winhttp reset proxy")
                elif 'start dynamic dns' in command:
                    start_dynamic_ip_updates()
                elif 'stop dynamic dns' in command:
                    stop_dynamic_ip_updates()
                else:
                    engine.say("Command not recognized.")
                    engine.runAndWait()
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                engine.say("Voice recognition error.")
                engine.runAndWait()

# Function to upload and apply VPN configuration
def upload_vpn_file():
    file_path = filedialog.askopenfilename(filetypes=[("OVPN Files", "*.ovpn")])
    if file_path:
        run_command(f"sudo openvpn --config {file_path}")

# Function to upload port forwarding CSV file
def upload_port_forwarding_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        try:
            df = pd.read_csv(file_path)
            for index, row in df.iterrows():
                run_command(f"netsh interface portproxy add v4tov4 listenport={row['ListenPort']} connectaddress={row['ConnectAddress']} connectport={row['ConnectPort']}")
            messagebox.showinfo("Success", "Port forwarding rules added successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload port forwarding file: {e}")

# Function to remove port forwarding rules from CSV file
def remove_port_forwarding_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        try:
            df = pd.read_csv(file_path)
            for index, row in df.iterrows():
                run_command(f"netsh interface portproxy delete v4tov4 listenport={row['ListenPort']}")
            messagebox.showinfo("Success", "Port forwarding rules removed successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove port forwarding rules: {e}")

# Function to update dynamic DNS using NoIP/DynDNS
def update_dynamic_ip():
    run_command("duc_client update")  # Replace this with your specific dynamic DNS client command

# Function to start dynamic DNS updates at regular intervals
def start_dynamic_ip_updates():
    global dynamic_ip_updating
    dynamic_ip_updating = True
    while dynamic_ip_updating:
        update_dynamic_ip()
        time.sleep(3600)  # Update every hour

# Function to stop dynamic DNS updates
def stop_dynamic_ip_updates():
    global dynamic_ip_updating
    dynamic_ip_updating = False

# Function to open WhatsApp fixed URL for support
def open_whatsapp_support():
    whatsapp_url = "https://call.whatsapp.com/video/vTjI0fXUWjJ0fx1ntYKvvo"
    webbrowser.open(whatsapp_url)

# Initialize the Tkinter window
root = tk.Tk()
root.title("Network Commander - Ethical Edition")
root.configure(bg="black")
root.geometry("800x600")

# Create a scrolled text widget for output
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg="black", fg="white", font=("Arial", 10))
output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Create buttons for various network commands
def create_command_button(frame, text, command):
    button = tk.Button(frame, text=text, bg="blue", fg="white", command=command, font=("Arial", 12), relief="raised", borderwidth=3)
    button.bind("<Enter>", lambda e: tooltip.show_tooltip(button, text))
    button.bind("<Leave>", lambda e: tooltip.hide_tooltip())
    return button

# Create frame for buttons
button_frame = tk.Frame(root, bg="black")
button_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

# Add buttons for network commands
buttons = [
    ("Display All IP Configuration", lambda: run_command(get_platform_command("ipconfig", "ifconfig"))),
    ("Detailed IP Configuration", lambda: run_command(get_platform_command("ipconfig /all", "ifconfig -a"))),
    ("Release IP Address", lambda: run_command(get_platform_command("ipconfig /release", "sudo dhclient -r"))),
    ("Renew IP Address", lambda: run_command(get_platform_command("ipconfig /renew", "sudo dhclient"))),
    ("Flush DNS Cache", lambda: run_command(get_platform_command("ipconfig /flushdns", "sudo systemd-resolve --flush-caches")))
]

for text, command in buttons:
    create_command_button(button_frame, text, command).pack(side=tk.LEFT, padx=10)

# WhatsApp Support Entry and Button
support_frame = tk.LabelFrame(root, text="Support", bg="black", fg="white", font=("Arial", 12), padx=10, pady=10)
support_frame.pack(fill=tk.X, padx=10, pady=10)

tk.Button(support_frame, text="WhatsApp Support", command=open_whatsapp_support, bg="green", fg="white", font=("Arial", 12), relief="raised", borderwidth=3).pack(side=tk.LEFT, padx=10)

# VPN and Port Forwarding Buttons
vpn_frame = tk.LabelFrame(root, text="VPN/Proxy Control", bg="black", fg="white", font=("Arial", 12), padx=10, pady=10)
vpn_frame.pack(fill=tk.X, padx=10, pady=10)

vpn_buttons = [
    ("Connect to VPN", upload_vpn_file),
    ("Disconnect VPN", lambda: run_command(get_platform_command("vpnclient disconnect your_vpn_connection_name", "sudo pkill openvpn"))),
    ("Set Proxy", lambda: run_command("netsh winhttp set proxy proxy_server_address")),
    ("Clear Proxy", lambda: run_command("netsh winhttp reset proxy"))
]

for text, command in vpn_buttons:
    create_command_button(vpn_frame, text, command).pack(side=tk.LEFT, padx=10)

# Port Forwarding Frame and Buttons
port_forwarding_frame = tk.LabelFrame(root, text="Port Forwarding", bg="black", fg="white", font=("Arial", 12), padx=10, pady=10)
port_forwarding_frame.pack(fill=tk.X, padx=10, pady=10)

port_forwarding_buttons = [
    ("Upload Port Forwarding CSV", upload_port_forwarding_file),
    ("Remove Port Forwarding CSV", remove_port_forwarding_file)
]

for text, command in port_forwarding_buttons:
    create_command_button(port_forwarding_frame, text, command).pack(side=tk.LEFT, padx=10)

# Controls for voice control
voice_control_frame = tk.Frame(root, bg="black")
voice_control_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

tk.Button(voice_control_frame, text="Start Voice Control", command=start_voice_control, bg="green", fg="white", font=("Arial", 12), relief="raised", borderwidth=3).pack(side=tk.LEFT, padx=10)
tk.Button(voice_control_frame, text="Pause Voice Control", command=pause_voice_control, bg="yellow", fg="black", font=("Arial", 12), relief="raised", borderwidth=3).pack(side=tk.LEFT, padx=10)
tk.Button(voice_control_frame, text="Resume Voice Control", command=resume_voice_control, bg="orange", fg="black", font=("Arial", 12), relief="raised", borderwidth=3).pack(side=tk.LEFT, padx=10)
tk.Button(voice_control_frame, text="Stop Voice Control", command=stop_voice_control, bg="red", fg="white", font=("Arial", 12), relief="raised", borderwidth=3).pack(side=tk.LEFT, padx=10)

# Tooltip class for showing tooltips
class Tooltip:
    def __init__(self, master):
        self.master = master
        self.tooltip = tk.Toplevel(master)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry("+0+0")
        self.label = tk.Label(self.tooltip, background="yellow", relief="solid", borderwidth=1, padx=5, pady=5)
        self.label.pack()
        self.tooltip.withdraw()

    def show_tooltip(self, widget, text):
        self.label.config(text=text)
        x, y, _, _ = widget.bbox("insert")
        x += widget.winfo_rootx() + 25
        y += widget.winfo_rooty() + 25
        self.tooltip.wm_geometry(f"+{x}+{y}")
        self.tooltip.deiconify()

    def hide_tooltip(self):
        self.tooltip.withdraw()

tooltip = Tooltip(root)

# Start the main loop
root.mainloop()
