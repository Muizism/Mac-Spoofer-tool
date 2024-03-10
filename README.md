# Mac Spoofer

Mac Spoofer is a Python tool for manipulating MAC addresses on Windows systems. It provides options for changing MAC addresses of network adapters and sniffing ARP packets for educational purposes.

**Note:** Wireshark must be installed on your system as it provides the required libpcap library for packet sniffing functionality.

## Usage

1. Clone the repository:

    ```bash
    git clone https://github.com/Muizism/Mac-Spoofer-tool
    ```

2. Open the project folder in Visual Studio Code.

3. Install dependencies by opening the integrated terminal in Visual Studio Code and running:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the tool with administrator privileges:

    - Open the `Mac-spoofer.py` file in Visual Studio Code.
    - Right-click on the file and select "Run Python File in Terminal" from the context menu.

5. Follow the on-screen instructions to change MAC addresses or start/stop packet sniffing.

## Important Note

This tool requires administrator privileges to modify network adapter settings. Please ensure that Visual Studio Code is running with elevated privileges when executing the tool.
Wireshark 
