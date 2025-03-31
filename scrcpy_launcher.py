import subprocess
import tkinter as tk
from tkinter import ttk, simpledialog, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import configparser
import os

# Default constants – these values are loaded from the config file.
DEFAULT_SCRCPY_PATH = r""
DEFAULT_ADB_PATH = r""
DEFAULT_WIRELESS_IP = "192.168.1.6:5555"
CONFIG_FILE = "scrcpy_config.ini"  # config file to store paths, wireless IP, and app icon

# For hiding command windows on Windows:
CREATE_NO_WINDOW = 0x08000000

def run_command(command_list, timeout=10):
    """Run a command hiddenly and return (stdout, stderr)."""
    try:
        result = subprocess.run(
            command_list,
            capture_output=True,
            text=True,
            creationflags=CREATE_NO_WINDOW,
            timeout=timeout
        )
        return result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return "", "Command timed out."
    except Exception as e:
        return "", str(e)

def restart_adb(log_func, adb_path):
    """Kill and restart the ADB server."""
    out, err = run_command([adb_path, "kill-server"])
    log_func("ADB kill-server executed.")
    out, err = run_command([adb_path, "start-server"])
    log_func("ADB start-server executed.")

def load_config():
    """Load configuration from the config file. Create defaults if needed."""
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_FILE):
        config["Paths"] = {"scrcpy": DEFAULT_SCRCPY_PATH, "adb": DEFAULT_ADB_PATH}
        config["Wireless"] = {"ip": DEFAULT_WIRELESS_IP}
        config["AppIcon"] = {"app_icon": ""}
        with open(CONFIG_FILE, "w") as f:
            config.write(f)
    else:
        config.read(CONFIG_FILE)
        if "Paths" not in config:
            config["Paths"] = {"scrcpy": DEFAULT_SCRCPY_PATH, "adb": DEFAULT_ADB_PATH}
        if "Wireless" not in config:
            config["Wireless"] = {"ip": DEFAULT_WIRELESS_IP}
        if "AppIcon" not in config:
            config["AppIcon"] = {"app_icon": ""}
        with open(CONFIG_FILE, "w") as f:
            config.write(f)
    return config

def save_config(config):
    """Save the given configuration to the config file."""
    with open(CONFIG_FILE, "w") as f:
        config.write(f)

class ScrcpyLauncher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.config_obj = load_config()
        paths = self.config_obj["Paths"]
        self.scrcpy_path = paths.get("scrcpy", DEFAULT_SCRCPY_PATH)
        self.adb_path = paths.get("adb", DEFAULT_ADB_PATH)
        self.wireless_ip = self.config_obj["Wireless"].get("ip", DEFAULT_WIRELESS_IP)
        self.app_icon_path = self.config_obj["AppIcon"].get("app_icon", "")

        self.title("scrcpy Launcher")
        self.geometry("480x550")
        self.resizable(False, False)
        self.configure(bg="#121212")
        # Set the taskbar icon from config if available.
        if self.app_icon_path and os.path.exists(self.app_icon_path):
            try:
                self.iconbitmap(self.app_icon_path)
            except Exception as e:
                print("Failed to set app icon:", e)

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TButton",
                             font=("Segoe UI", 14, "bold"),
                             foreground="#ffffff",
                             background="#3d7ea6",
                             borderwidth=0,
                             padding=10)
        self.style.map("TButton", background=[("active", "#559ecf")])
        self.pulse_color = "#3d7ea6"

        self.create_widgets()
        self.animate_buttons()
        self.update_usb_indicator()
        self.check_mirroring_status()

    def create_widgets(self):
        # Top bar with title and gear icon.
        top_frame = tk.Frame(self, bg="#121212")
        top_frame.pack(fill="x", pady=5, padx=10)
        title_label = tk.Label(top_frame, text="scrcpy Launcher", font=("Segoe UI", 24, "bold"),
                               bg="#121212", fg="#ffffff")
        title_label.pack(side="left", padx=(0,10))
        # Gear icon as a clickable label to open config window.
        settings_icon = tk.Label(top_frame, text="⚙", font=("Segoe UI", 24), bg="#121212", fg="#ffffff", cursor="hand2")
        settings_icon.pack(side="right")
        settings_icon.bind("<Button-1>", lambda e: self.open_config_window())

        # Indicators Frame
        indicator_frame = tk.Frame(self, bg="#121212")
        indicator_frame.pack(pady=10, fill="x", padx=15)
        self.usb_indicator_canvas = tk.Canvas(indicator_frame, width=24, height=24, bg="#121212", highlightthickness=0)
        self.usb_indicator_canvas.grid(row=0, column=0, padx=(0,8))
        self.usb_indicator_label = tk.Label(indicator_frame, text="USB Disconnected", font=("Segoe UI", 12),
                                            bg="#121212", fg="#ffffff")
        self.usb_indicator_label.grid(row=0, column=1, sticky="w", padx=(0,20))
        self.mirroring_indicator_canvas = tk.Canvas(indicator_frame, width=24, height=24, bg="#121212", highlightthickness=0)
        self.mirroring_indicator_canvas.grid(row=0, column=2, padx=(0,8))
        self.mirroring_indicator_label = tk.Label(indicator_frame, text="Not Mirroring", font=("Segoe UI", 12),
                                                  bg="#121212", fg="#ffffff")
        self.mirroring_indicator_label.grid(row=0, column=3, sticky="w")

        # Buttons Frame
        btn_frame = tk.Frame(self, bg="#121212")
        btn_frame.pack(pady=15)
        self.usb_btn = ttk.Button(btn_frame, text="USB", command=self.run_usb)
        self.usb_btn.grid(row=0, column=0, padx=15, ipadx=10, ipady=10)
        self.wireless_btn = ttk.Button(btn_frame, text="Wireless", command=self.run_wireless)
        self.wireless_btn.grid(row=0, column=1, padx=15, ipadx=10, ipady=10)

        # Log Area Label
        log_label = tk.Label(self, text="Log", font=("Segoe UI", 14, "bold"),
                             bg="#121212", fg="#ffffff")
        log_label.pack(anchor="w", padx=15)
        # Log Area with ScrolledText
        log_frame = tk.Frame(self, bg="#121212", bd=2, relief="sunken")
        log_frame.pack(fill="both", expand=True, padx=15, pady=(5,15))
        self.log_text = ScrolledText(log_frame, height=10, bg="#1e1e1e", fg="#c0c0c0",
                                     font=("Segoe UI", 10), wrap="word", bd=0, padx=5, pady=5)
        self.log_text.pack(fill="both", expand=True)
        self.log_text.configure(state="disabled")

    def open_config_window(self):
        """Open the configuration window to allow changes to scrcpy path, wireless IP, and app icon."""
        config_win = tk.Toplevel(self)
        config_win.title("Configuration")
        config_win.geometry("550x400")
        config_win.configure(bg="#121212")
        frame = tk.Frame(config_win, bg="#1e1e1e")
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        tk.Label(frame, text="scrcpy Path:", font=("Segoe UI", 12, "bold"), bg="#1e1e1e", fg="#ffffff").grid(row=0, column=0, sticky="w")
        scrcpy_entry = tk.Entry(frame, font=("Segoe UI", 12), width=45)
        scrcpy_entry.grid(row=0, column=1, padx=10, pady=5)
        scrcpy_entry.insert(0, self.scrcpy_path)
        def browse_scrcpy():
            file_path = filedialog.askopenfilename(title="Select scrcpy.exe", filetypes=[("Executable Files", "*.exe")])
            if file_path:
                scrcpy_entry.delete(0, tk.END)
                scrcpy_entry.insert(0, file_path)
        ttk.Button(frame, text="Browse", command=browse_scrcpy).grid(row=0, column=2, padx=5)

        tk.Label(frame, text="Wireless IP (with port):", font=("Segoe UI", 12, "bold"), bg="#1e1e1e", fg="#ffffff").grid(row=1, column=0, sticky="w")
        ip_entry = tk.Entry(frame, font=("Segoe UI", 12), width=45)
        ip_entry.grid(row=1, column=1, padx=10, pady=5, columnspan=2)
        ip_entry.insert(0, self.config_obj["Wireless"].get("ip", DEFAULT_WIRELESS_IP))

        tk.Label(frame, text="App Icon (Taskbar):", font=("Segoe UI", 12, "bold"), bg="#1e1e1e", fg="#ffffff").grid(row=2, column=0, sticky="w")
        icon_entry = tk.Entry(frame, font=("Segoe UI", 12), width=45)
        icon_entry.grid(row=2, column=1, padx=10, pady=5, columnspan=2)
        icon_entry.insert(0, self.config_obj["AppIcon"].get("app_icon", ""))
        def browse_icon():
            file_path = filedialog.askopenfilename(title="Select Icon", filetypes=[("ICO Files", "*.ico"), ("All Files", "*.*")])
            if file_path:
                icon_entry.delete(0, tk.END)
                icon_entry.insert(0, file_path)
        ttk.Button(frame, text="Browse", command=browse_icon).grid(row=2, column=3, padx=5)

        instructions = (
            "Instructions:\n"
            "- scrcpy Path: Full path to scrcpy.exe\n"
            "- Wireless IP: Your phone's wireless ADB connection (e.g., 192.168.1.X:5555)\n"
            "- App Icon: ICO file for the taskbar icon (only you can change this)"
        )
        tk.Label(frame, text=instructions, font=("Segoe UI", 10), bg="#1e1e1e", fg="#c0c0c0", justify="left").grid(row=3, column=0, columnspan=4, pady=10, sticky="w")

        def save_changes():
            self.scrcpy_path = scrcpy_entry.get().strip()
            self.config_obj["Paths"]["scrcpy"] = self.scrcpy_path
            self.config_obj["Wireless"]["ip"] = ip_entry.get().strip()
            self.app_icon_path = icon_entry.get().strip()
            self.config_obj["AppIcon"]["app_icon"] = self.app_icon_path
            save_config(self.config_obj)
            self.append_log("Configuration updated.")
            if self.app_icon_path and os.path.exists(self.app_icon_path):
                try:
                    self.iconbitmap(self.app_icon_path)
                    self.append_log("App icon updated.")
                except Exception as e:
                    self.append_log("Failed to update app icon: " + str(e))
            config_win.destroy()

        ttk.Button(frame, text="Save", command=save_changes).grid(row=4, column=0, columnspan=4, pady=15)

    def append_log(self, message):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def animate_buttons(self):
        new_color = "#559ecf" if self.pulse_color == "#3d7ea6" else "#3d7ea6"
        self.pulse_color = new_color
        self.style.configure("Pulse.TButton", background=new_color)
        self.usb_btn.config(style="Pulse.TButton")
        self.wireless_btn.config(style="Pulse.TButton")
        self.after(600, self.animate_buttons)

    def update_usb_indicator(self):
        connected = self.check_usb_connected()
        self.usb_indicator_canvas.delete("all")
        if connected:
            self.usb_indicator_canvas.create_oval(2, 2, 22, 22, fill="limegreen", outline="")
            self.usb_indicator_label.config(text="USB Connected", fg="limegreen")
        else:
            self.usb_indicator_canvas.create_oval(2, 2, 22, 22, fill="gold", outline="")
            self.usb_indicator_label.config(text="USB Disconnected", fg="gold")
        self.after(1000, self.update_usb_indicator)

    def update_mirroring_indicator(self, status):
        self.mirroring_indicator_canvas.delete("all")
        color = "limegreen" if status in ("USB Mirroring", "Wireless Mirroring") else "crimson"
        self.mirroring_indicator_canvas.create_oval(2, 2, 22, 22, fill=color, outline="")
        self.mirroring_indicator_label.config(text=status, fg=color)

    def check_usb_connected(self):
        out, err = run_command([self.adb_path, "devices", "-l"])
        lines = out.splitlines()
        for line in lines[1:]:
            line = line.strip()
            if line and "device" in line.lower() and "unauthorized" not in line.lower():
                serial = line.split()[0]
                if "." not in serial:
                    return True
        return False

    def check_wireless_connected(self):
        out, err = run_command([self.adb_path, "devices", "-l"])
        lines = out.splitlines()
        for line in lines[1:]:
            line = line.strip()
            if line and "device" in line.lower() and "unauthorized" not in line.lower():
                serial = line.split()[0]
                if "." in serial:
                    return True
        return False

    def check_mirroring_status(self):
        if self.check_usb_connected():
            self.update_mirroring_indicator("USB Mirroring")
        elif self.check_wireless_connected():
            self.update_mirroring_indicator("Wireless Mirroring")
        else:
            self.update_mirroring_indicator("Not Mirroring")
        self.after(2000, self.check_mirroring_status)

    def run_usb(self):
        if not self.check_usb_connected():
            self.append_log("⚠️ Please PLUG IN the USB cable to start USB Mirroring.")
            self.update_mirroring_indicator("Not Mirroring")
            return
        self.update_mirroring_indicator("USB Mirroring")
        self.append_log("USB Mirroring Started")
        out, err = run_command([self.adb_path, "disconnect"])
        self.append_log("Disconnected any wireless connections.")
        subprocess.Popen([self.scrcpy_path, "--select-usb"], creationflags=CREATE_NO_WINDOW)
        self.append_log("scrcpy launched in USB mode.")

    def run_wireless(self):
        try:
            if self.check_usb_connected():
                self.append_log("⚠️ Please REMOVE the USB cable before using Wireless mode.")
                return
            self.append_log("Attempting Wireless Mirroring...")
            saved_ip = self.config_obj["Wireless"].get("ip", DEFAULT_WIRELESS_IP)
            self.append_log(f"Using saved wireless IP: {saved_ip}")
            ip_target = saved_ip

            out, err = run_command([self.adb_path, "connect", ip_target])
            self.append_log(f"ADB connect (default):\nSTDOUT: {out}\nSTDERR: {err}")

            if "refused" in err.lower() or "cannot connect" in err.lower():
                self.append_log("Wireless connection failed. Restarting ADB server...")
                restart_adb(self.append_log, self.adb_path)
                out, err = run_command([self.adb_path, "connect", ip_target])
                self.append_log(f"ADB reconnect attempt:\nSTDOUT: {out}\nSTDERR: {err}")

            if "connected" in out.lower():
                self.append_log("Wireless Mirroring Started")
                self.update_mirroring_indicator("Wireless Mirroring")
                subprocess.Popen([self.scrcpy_path, "--select-tcpip"], creationflags=CREATE_NO_WINDOW)
            else:
                self.append_log("Wireless Mirroring Ended")
                new_ip = simpledialog.askstring("Wireless ADB", 
                                                "Enter your wireless IP (with port, e.g., 192.168.1.X:5555):",
                                                parent=self)
                if new_ip:
                    new_ip = new_ip.strip()
                    self.config_obj["Wireless"]["ip"] = new_ip
                    save_config(self.config_obj)
                    self.append_log(f"Saved new wireless IP: {new_ip}")
                    out, err = run_command([self.adb_path, "connect", new_ip])
                    self.append_log(f"ADB connect (manual):\nSTDOUT: {out}\nSTDERR: {err}")
                    if "connected" in out.lower():
                        self.append_log("Wireless Mirroring Started")
                        self.update_mirroring_indicator("Wireless Mirroring")
                        subprocess.Popen([self.scrcpy_path, "--select-tcpip"], creationflags=CREATE_NO_WINDOW)
                    else:
                        self.append_log("Wireless Mirroring Ended after manual IP entry.")
                        self.update_mirroring_indicator("Not Mirroring")
                        self.append_log("⚠️ Please ENABLE Wireless Debugging on your phone and ensure both devices are on the same Wi-Fi.")
                else:
                    self.append_log("No IP entered. Aborting Wireless Mirroring.")
                    self.update_mirroring_indicator("Not Mirroring")
        except Exception as e:
            self.append_log("Error in Wireless mode: " + str(e))
            self.update_mirroring_indicator("Not Mirroring")

    def start(self):
        self.check_mirroring_status()
        self.mainloop()

if __name__ == "__main__":
    app = ScrcpyLauncher()
    app.start()
