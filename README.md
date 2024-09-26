# NETWORK-COMMANDER
CROSS PLATFORM NETWORK COMMANDER FOR HACKERS 

![mt](https://github.com/user-attachments/assets/a3f2f5d0-eb4f-4101-9795-99bc21956dad)

Network Commander - Usage and Features Documentation
© 2024 Darkspace Software & Security
Author: Michael James Blenkinsop
Introduction
Network Commander is a comprehensive network management tool that operates across Windows, macOS, and Linux platforms. It is designed to provide network administrators and users with an easy-to-use interface for performing a variety of network-related tasks, including managing VPN connections, port forwarding, Dynamic DNS, and more. Additionally, the tool features voice control functionality for hands-free operation.
Features
1. Network Command Execution
Network Commander offers a wide range of network command functionalities. Users can execute network commands directly from the graphical interface, or through voice commands. Available network commands include:
- Display IP configuration (ipconfig/ifconfig)
- Flush DNS cache
- Renew or release IP address
- Display detailed network adapter information
These commands help users manage network configurations and troubleshoot networking issues.
2. VPN Management
With built-in support for OpenVPN, users can upload .ovpn configuration files to establish secure VPN connections. The user can connect and disconnect VPNs through the GUI, simplifying VPN management. This feature is useful for both personal and enterprise environments, where VPN connectivity is essential.
3. Port Forwarding
Network Commander allows users to manage port forwarding rules by uploading a CSV file. The rules from the CSV file are automatically applied to the system. In addition, users can remove port forwarding rules by uploading a removal CSV file. This functionality simplifies the process of setting up and managing port forwarding, which is particularly important in environments with firewalls and NAT devices.
4. Dynamic DNS (NoIP/DynDNS)
Dynamic DNS support allows users to keep their domain name updated with their dynamic public IP address. Network Commander integrates with Dynamic DNS services like NoIP or DynDNS to ensure that users' IP addresses are always up to date, even if they change frequently. This feature is particularly useful for users hosting services from their home networks.
5. Voice Control
Voice control is one of the standout features of Network Commander. Users can execute a wide range of commands using their voice. The voice recognition system, powered by Google Speech Recognition, allows hands-free operation for common tasks such as checking IP configurations, managing VPNs, and running network diagnostics. This is especially useful for users who need to multitask or prefer voice-driven workflows.
6. WhatsApp Support
Network Commander includes a built-in support feature that connects users to a WhatsApp video call. By clicking the WhatsApp support button, users are automatically redirected to a fixed video call link. This feature can be used to provide real-time assistance and troubleshooting to end-users.
7. Graphical User Interface (GUI)
The graphical interface of Network Commander is designed to be user-friendly and intuitive. Built with Tkinter, the interface allows users to run commands via buttons and text inputs. Users can easily execute network tasks without needing to open a terminal or know the specific command syntax. This makes the tool accessible to both technical and non-technical users.
8. Cross-Platform Support
Network Commander is fully cross-platform and works seamlessly across Windows, macOS, and Linux systems. The tool detects the user's operating system and adjusts its functionality accordingly. Whether the user is managing a Windows environment or working on a Linux-based server, Network Commander ensures compatibility and ease of use.
Installation and Setup
To install Network Commander, the user should follow these steps:
1. Download and run the 'NC_Automate.py' script.
2. The script will automatically detect the operating system and install necessary dependencies (OpenVPN, Tkinter, Python libraries).
3. After installation, a 'NetworkCommander' folder will be created on the user's desktop.
4. Inside this folder, the main 'networkcommander.py' script will be available.
5. Users can run 'networkcommander.py' to launch the tool and start managing their network configurations.
Usage
Once the installation is complete, the user can run 'networkcommander.py' from the desktop folder to access the tool. The GUI provides buttons for running commands, while the voice control option allows users to interact with the tool via voice commands. For advanced users, port forwarding rules and VPN configurations can be uploaded via the interface.
Conclusion
Network Commander is a powerful and flexible tool designed to streamline network management tasks. With its GUI and voice control functionality, it is suitable for both novice users and advanced network administrators. The tool's cross-platform support, integration with VPN and Dynamic DNS services, and intuitive interface make it an essential tool for managing network configurations.
