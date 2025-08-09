"""
This script provides utility functions for environment setup and management.

Features include:
- Printing a custom ASCII art logo with a timed display.
- Checking if Python is installed and, if not, downloading and silently installing it on Windows.
- Installing Python packages via pip with real-time status feedback.
- Providing a helper function to retrieve formatted current date and time for logging.

These utilities help automate initial environment preparation and package management.
"""

#---###---#

# Importing Libraries
from datetime import datetime  # Import for handling date and time
import time as tm  # Import time module with alias 'tm' for delays
import subprocess  # For running system commands
import sys  # Access system-specific parameters and functions
import os  # For interacting with the operating system (paths, directories)

#---###---#

# Reconfigure standard output to use UTF-8 encoding (helps with printing special characters)
sys.stdout.reconfigure(encoding='utf-8')

#---###---#

# Returns the current local date and time formatted as a string: YYYY-MM-DD | HH:MM:SS
def get_time():
    local_date = datetime.now()  # Gets current datetime
    local_date = local_date.strftime("%Y-%m-%d | %H:%M:%S")  # Formats datetime to string
    
    return local_date

#---###---#

# Installs Python packages from a list using pip and reports success or failure
def install_libs(package_list_collected):
    for package in package_list_collected:
        try:
            # Runs the pip install command for each package, raising error if it fails
            subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
            
            # Prints success message with timestamp
            print(f"({get_time()}) | Successfully installed: {package}")
            print()
            tm.sleep(1)  # Waits 1 second before next install
            
        except subprocess.CalledProcessError:
            # Prints failure message with timestamp if installation fails
            print(f"({get_time()}) | Failed to install: {package}")
            print()
            tm.sleep(1)

#---###---#

# Prints a stylized ASCII art logo for "EMICORE" and waits 5 seconds before continuing
def print_logo():
    logo = r"""
      ███████╗███╗   ███╗██╗ ██████╗ ██████╗ █████╗ ███████╗
      ██╔════╝████╗ ████║██║██╔════╝██╔═══██╗██╔══██╗██╔════╝
      █████╗  ██╔████╔██║██║██║     ██║   ██║███████║█████╗  
      ██╔══╝  ██║╚██╔╝██║██║██║     ██║   ██║██╔══██║██╔══╝  
      ███████╗██║ ╚═╝ ██║██║╚██████╗╚██████╔╝██║  ██║███████╗
      ╚══════╝╚═╝     ╚═╝╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝

                      E M I C O R E
    """
    
    print("\n" + logo + "\n")
    tm.sleep(5)  # Pause to allow user to see the logo

#---###---#

# Checks if Python is installed on the system. If not installed, downloads and silently installs Python 3.11.4 on Windows.
def install_python():
    try:
        # Checks Python version to verify installation
        subprocess.run(["python", "--version"], check=True)
        print("Python is already installed.")
    
    except subprocess.CalledProcessError:
        # If Python is not installed, informs user and proceeds to download and install
        
        print("Python is not installed. Downloading and installing...")

        # Official URL for Python 3.11.4 installer for Windows 64-bit
        python_installer_url = "https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe"
        
        # Path where the installer will be saved (current working directory)
        installer_path = os.path.join(os.getcwd(), "python_installer.exe")

        # Downloads the Python installer using curl
        subprocess.run(["curl", "-o", installer_path, python_installer_url], check=True)

        # Runs the installer silently, installing for all users and adding Python to PATH
        subprocess.run([installer_path, "/quiet", "InstallAllUsers=1", "PrependPath=1"], check=True)

        print("Python installation completed successfully.")