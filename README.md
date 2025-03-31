# Scrcpy Launcher

A modern and user-friendly launcher for **Scrcpy**, allowing you to mirror your Android device via **USB or Wireless Debugging** with a simple, dynamic interface.

---

## 🚀 Features

- **One-click USB & Wireless mirroring**
- **Automatic detection** of USB and Wireless Debugging
- **Real-time status indicators** (USB connected, Mirroring status, etc.)
- **Built-in Configurations** to change Scrcpy path, IP, and port
- **No command-line hassle** – runs commands in the background
- **Beautiful & modern UI** with animations

---

## 💅 Prerequisites

Before using this launcher, ensure you have the following:
- **Scrcpy** installed
- **Python** installed
- **USB Debugging enabled on your phone** (for initial setup)

---

## 👅 Installation

### Step 1: Download Scrcpy

1. Download **Scrcpy** from the official repository: [Scrcpy GitHub](https://github.com/Genymobile/scrcpy/releases)
2. Extract it to a folder (e.g., `C:\Users\YourName\scrcpy`)

### Step 2: Install Python (if not installed)

1. Download and install **Python** from [Python Official Site](https://www.python.org/downloads/)
2. Ensure **pip** is installed by running:
   ```sh
   python -m ensurepip --default-pip
   ```

### Step 3: Install Required Dependencies

Run the following commands in the launcher’s directory:

```sh
pip install pyqt5
pip install adb-shell
pip install configparser
```

---

## 🔧 Configuration

Before using the launcher, you need to configure it properly. Follow these steps:

### 1️⃣ Enable USB Debugging

1. Open **Settings** on your Android phone.
2. Go to **About Phone**.
3. Tap **Build Number** **7 times** to enable Developer Mode.
4. Go back to **Settings > Developer Options**.
5. Enable **USB Debugging**.

### 2️⃣ Set the Scrcpy Path

1. Open the launcher.
2. Click the **⚙️ Settings Icon** (top-right corner).
3. Under **Scrcpy Path**, set the folder where you extracted Scrcpy.

### 3️⃣ Set the Wireless Debugging IP & Port

1. Open **Developer Options** on your Android phone.
2. Enable **Wireless Debugging**.
3. Tap **Pair Device with Pairing Code**.
4. Note the **IP Address** and **Port** shown.
5. In the **Launcher Settings**, enter this **IP**\*\*:Port\*\* under "Wireless Settings".

### 4️⃣ Set Custom App Icon (Optional)

1. Place your **.ico** file anywhere on your PC.
2. Open the settings.
3. Set the **App Icon Path** to your **.ico** file.
4. Restart the app.

---

## 📰 How to Use

### **🐐 USB Mirroring**

1. **Enable USB Debugging** (see above).
2. **Connect your phone via USB**.
3. Click the **USB Mirroring** button.
4. Your phone screen should appear!

### **📶 Wireless Mirroring**

1. **Enable USB Debugging first** (required for initial setup).
2. **Connect your phone via USB** and run **USB Mirroring at least once**.
3. Enable **Wireless Debugging** on your phone.
4. Unplug the USB cable.
5. Click **Wireless Mirroring**.
6. If IP/Port is incorrect, it will prompt you to enter the correct values.
7. Your phone screen should appear!

---

## 🔍 Troubleshooting

### **Wireless Debugging Not Working?**

👉 **Ensure USB Debugging was enabled first.**  
👉 **Ensure ADB is enabled** on your phone.  
👉 **Ensure USB is unplugged** before starting Wireless Mode.  
👉 Run `adb kill-server` and try again.  
👉 If the connection fails, it will ask you to re-enter the **IP and Port**.

### **USB Not Detected?**

👉 **Enable Developer Options & USB Debugging**.  
👉 Try **another USB port** or cable.  
👉 Run `adb devices` in **cmd** to check if the device is recognized.

---

## 🛠️ Future Features

- Auto-detect and fix connection issues.  
- Custom hotkeys for quick mirroring.  
- Auto-start with Windows.

---

## 🐝 License

This project is open-source under the **MIT License**. Feel free to contribute and improve!

---

### ⭐ Enjoy using Scrcpy Launcher? Give it a star on GitHub! ⭐




<p><small>Made with love ❤️‍🔥 by Moh (<a href="https://discord.com">@m7i1</a>)</small></p>

<p><small>Made with love ❤️‍🔥 by Moh (<a href="https://discord.com">@m7i1</a>)</small></p>

<p><small>Made with love ❤️‍🔥 by Moh (<a href="https://discord.com">@m7i1</a>)</small></p>

<p><small>Made with love ❤️‍🔥 by Moh (<a href="https://discord.com">@m7i1</a>)</small></p>

<p><small>Made with love ❤️‍🔥 by Moh (<a href="https://discord.com">@m7i1</a>)</small></p>

<p><small>Made with love ❤️‍🔥 by Moh (<a href="https://discord.com">@m7i1</a>)</small></p>

<p><small>Made with love ❤️‍🔥 by Moh (<a href="https://discord.com">@m7i1</a>)</small></p>
