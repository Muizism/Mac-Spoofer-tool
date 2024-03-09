from datetime import datetime as dt
import socket
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import re
import string
import random
from tkinter import scrolledtext
from scapy.all import sniff, ARP
from PIL import Image, ImageTk

NETWORK_INTERFACE_REG_PATH = r"HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Class\\{4d36e972-e325-11ce-bfc1-08002be10318}"
TRANSPORT_NAME_REGEX = re.compile("{.+}")
MAC_ADDRESS_REGEX = re.compile(r"([A-Z0-9]{2}[:-]){5}([A-Z0-9]{2})")
manufacturers = {
    "Apple": "00:03:93:00:00:00",
    "Asus": "00:0C:6E:00:00:00",
    "Avaya": "00:1B:4F:00:00:00",
    "Acer": "00:25:DB:00:00:00",
    "Amazon": "F8:E0:79:00:00:00",
    "Broadcom": "00:10:18:00:00:00",
    "Cisco": "00:14:69:00:00:00",
    "Dell": "00:14:22:00:00:00",
    "Google": "BC:54:51:00:00:00",
    "HP": "00:25:B3:00:00:00",
    "HTC": "00:0E:2E:00:00:00",
    "Huawei": "00:1A:2B:00:00:00",
    "IBM": "00:04:AC:00:00:00",
    "Intel": "00:0D:BC:00:00:00",
    "Juniper": "00:0B:86:00:00:00",
    "LG": "00:19:7D:00:00:00",
    "Lenovo": "00:0A:95:00:00:00",
    "Microsoft": "00:50:F2:00:00:00",
    "Motorola": "00:18:2E:00:00:00",
    "Netgear": "00:24:B2:00:00:00",
    "Nokia": "00:19:B7:00:00:00",
    "Nintendo": "E0:76:D0:00:00:00",
    "OnePlus": "30:05:5C:00:00:00",
    "Raspberry Pi": "B8:27:EB:00:00:00",
    "Samsung": "00:17:D5:00:00:00",
    "Siemens": "00:08:25:00:00:00",
    "Sony": "00:0A:D9:00:00:00",
    "Thinkpad": "00:90:4B:00:00:00",
    "Toshiba": "00:16:41:00:00:00",
    "Xiaomi": "F4:8B:32:00:00:00",
    "ZTE": "00:1D:0F:00:00:00",
    "Qualcomm": "00:60:57:00:00:00",
    "Fujitsu": "00:09:3A:00:00:00",
    "Cisco Meraki": "F8:1E:DF:00:00:00",
    "VMware": "00:50:56:00:00:00",
    "D-Link": "00:1E:58:00:00:00",
    "Aruba": "64:9E:F3:00:00:00"
}

def get_connected_adapters_mac_address():
    """Get MAC addresses and transport names of connected adapters"""
    connected_adapters_mac = []
    try:
        for potential_mac in subprocess.check_output("getmac").decode().splitlines():
            mac_address = MAC_ADDRESS_REGEX.search(potential_mac)
            transport_name = TRANSPORT_NAME_REGEX.search(potential_mac)
            if mac_address and transport_name:
                connected_adapters_mac.append((mac_address.group(), transport_name.group()))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get connected adapters: {e}")
    return connected_adapters_mac

def resolve_ip(ip):
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        return hostname
    except socket.herror:
        return "Unknown"

def clean_mac(mac):
    """Clean non hexadecimal characters from a MAC address and uppercase it"""
    return "".join(c for c in mac if c in string.hexdigits).upper()

def get_random_mac_address():
    """Generate and return a MAC address in the format of WINDOWS"""
    uppercased_hexdigits = ''.join(set(string.hexdigits.upper()))
    return random.choice(uppercased_hexdigits) + random.choice("24AE") + "".join(random.sample(uppercased_hexdigits, k=10))

def change_mac_address(adapter_transport_name, new_mac_address):
    """Change the MAC address of the selected network adapter"""
    try:
        output = subprocess.check_output(f"reg QUERY " + NETWORK_INTERFACE_REG_PATH.replace("\\\\", "\\")).decode()
        for interface in re.findall(rf"{NETWORK_INTERFACE_REG_PATH}\\\d+", output):
            adapter_index = int(interface.split("\\")[-1])
            interface_content = subprocess.check_output(f"reg QUERY {interface.strip()}").decode()
            if adapter_transport_name in interface_content:
                subprocess.check_output(f"reg add {interface} /v NetworkAddress /d {new_mac_address} /f").decode()
                return adapter_index
    except Exception as e:
        messagebox.showerror("Error", f"Failed to change MAC address: {e}")
        return None

def disable_enable_adapter(adapter_index, action="disable"):
    """Disable or enable the network adapter to apply the MAC address change"""
    try:
        if action == "disable":
            subprocess.check_output(f"wmic path win32_networkadapter where index={adapter_index} call disable").decode()
        else:
            subprocess.check_output(f"wmic path win32_networkadapter where index={adapter_index} call enable").decode()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to {action} the adapter: {e}")


class FirstWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mac Spoofer")
        self.root.geometry("400x300")

        self.load_image()

        self.display_description()

        self.open_main_window_button = tk.Button(self.root, text="Next", command=self.open_main_window)
        self.open_main_window_button.pack(side=tk.RIGHT, anchor=tk.S, pady=15, padx=5, fill=tk.X)

    def load_image(self):
        image_path = "welcome.PNG"  
        image = Image.open(image_path)
        image = image.resize((150, 300), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        self.image_label = tk.Label(self.root, image=photo)
        self.image_label.image = photo
        self.image_label.pack(side=tk.LEFT, padx=10, pady=10)

    def display_description(self):
     label_text = "Welcome to Mac-Spoofer tool"
     description_text = """
     This versatile tool enables users to manipulate MAC addresses, providing options from various vendors or generating random ones. It simplifies network sniffing and seamlessly applies the chosen MAC address for educational purposes.
     """
     self.label = tk.Label(self.root, text=label_text, font=("Arial", 10, "bold"))
     self.label.pack(pady=20)
     self.description_label = tk.Label(self.root, text=description_text, justify=tk.LEFT, padx=10)
     self.description_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=0)
     self.description_label.config(font=("Consolas", 8), wraplength=200, anchor=tk.W, justify=tk.LEFT)
 
    def open_main_window(self):
        self.root.destroy()  
        main_window = MainApplication()


class MainApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.app = MacChangerGUI(self.root)
        self.root.mainloop()

def create_window():
    window = tk.Tk()
    window.geometry('600x400')  
    return window

class MacChangerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mac Spoofer")
        self.sniffing= False
        self.create_widgets()
        self.populate_adapters()

    def create_widgets(self):
      
        paned_window = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)
        left_frame = ttk.Frame(paned_window)
        paned_window.add(left_frame, weight=1)
        right_frame = ttk.Frame(paned_window)
        paned_window.add(right_frame, weight=1)

        self.adapter_label = ttk.Label(left_frame, text="Select Network Adapter:")
        self.adapter_label.pack(padx=10, pady=5)

        self.adapter_combobox = ttk.Combobox(left_frame, state="readonly", width=60)
        self.adapter_combobox.pack(padx=10, pady=5)
        
        self.manufacturer_label = ttk.Label(left_frame, text="Select Manufacturer:")
        self.manufacturer_label.pack(padx=10, pady=5)

        self.manufacturer_combobox = ttk.Combobox(left_frame, state="readonly", width=60)
        self.manufacturer_combobox.pack(padx=10, pady=5)
        self.manufacturer_combobox['values'] = list(manufacturers.keys())
        self.manufacturer_combobox.bind("<<ComboboxSelected>>", self.populate_mac_address)

        self.mac_entry_label = ttk.Label(left_frame, text="New MAC Address (leave blank for random):")
        self.mac_entry_label.pack(padx=10, pady=5)

        self.mac_entry = ttk.Entry(left_frame, width=63)
        self.mac_entry.pack(padx=10, pady=5)

        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        self.change_button = ttk.Button(left_frame, text="Change MAC Address", command=self.change_mac)
        self.change_button.pack(side=tk.LEFT, expand=True)

        self.reset_button = ttk.Button(left_frame, text="Reset", command=self.reset_mac)
        self.reset_button.pack(side=tk.LEFT, expand=True)

        buttons_frame = ttk.Frame(right_frame)
        buttons_frame.pack(pady=5) 

        self.start_sniffing_button = ttk.Button(buttons_frame, text="Start Sniffing", command=self.start_sniffing)
        self.start_sniffing_button.pack(side=tk.LEFT, padx=5)  

        self.stop_sniffing_button = ttk.Button(buttons_frame, text="Stop Sniffing", command=self.stop_sniffing)
        self.stop_sniffing_button.pack(side=tk.LEFT, padx=5)
        self.text_area = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, width=50, height=15)
        self.text_area.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

    def change_mac(self):
        adapter_info = self.adapter_combobox.get()
        if not adapter_info:
            messagebox.showwarning("Warning", "Please select a network adapter.")
            return
        manufacturer = self.manufacturer_combobox.get()
        new_mac_address = manufacturers.get(manufacturer, "")
    
        if manufacturer and not new_mac_address:
            messagebox.showwarning("Warning", "Invalid manufacturer selected.")
            return
        transport_name = TRANSPORT_NAME_REGEX.search(adapter_info).group()
        new_mac_address = self.mac_entry.get().strip()

        if not new_mac_address:
            new_mac_address = get_random_mac_address()
        else:
            new_mac_address = clean_mac(new_mac_address)

        adapter_index = change_mac_address(transport_name, new_mac_address)
        if adapter_index is not None:
            disable_enable_adapter(adapter_index, "disable")
            disable_enable_adapter(adapter_index, "enable")
            messagebox.showinfo("Success", f"MAC Address changed to {new_mac_address}")

    def start_sniffing(self):
        if not self.sniffing:
            self.sniffing = True
            self.text_area.insert(tk.END, "Sniffing started...\n")
            threading.Thread(target=self.sniff_packets, daemon=True).start()

    def stop_sniffing(self):
        if self.sniffing:
            self.sniffing = False
            self.text_area.insert(tk.END, "Sniffing stopped.\n")

    def sniff_packets(self):
        while self.sniffing:
            sniff(prn=self.handle_packet, filter="arp", store=False, timeout=1)

    def handle_packet(self, packet):
        if ARP in packet:
            src_ip = packet[ARP].psrc
            src_mac = packet[ARP].hwsrc
            hostname = resolve_ip(src_ip)
            message = f"ARP Packet: {src_mac} -> {src_ip} ({hostname})\n"
            self.text_area.insert(tk.END, message)
            self.text_area.see(tk.END)

    def populate_mac_address(self, event):
     manufacturer = self.manufacturer_combobox.get()
     mac_address = manufacturers.get(manufacturer, "")
     self.mac_entry.delete(0, tk.END)
     self.mac_entry.insert(0, mac_address)

    def populate_adapters(self):
        adapters = get_connected_adapters_mac_address()
        self.adapter_combobox['values'] = [f"{mac}, {transport}" for mac, transport in adapters]

    def reset_mac(self):
        adapter_info = self.adapter_combobox.get()
        if not adapter_info:
            messagebox.showwarning("Warning", "Please select a network adapter.")
            return

        transport_name = TRANSPORT_NAME_REGEX.search(adapter_info).group()
        current_mac_address = MAC_ADDRESS_REGEX.search(adapter_info).group()

        adapter_index = change_mac_address(transport_name, current_mac_address)
        if adapter_index is not None:
            disable_enable_adapter(adapter_index, "disable")
            disable_enable_adapter(adapter_index, "enable")
            messagebox.showinfo("Success", f"MAC Address reset to {current_mac_address}")

if __name__ == "__main__":
    first_window = FirstWindow()
    first_window.root.mainloop()
  
