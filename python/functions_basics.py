from datetime import datetime
import time as tm
import subprocess
import sys

#---###---#

def get_time():
    
    local_date = datetime.now()
    local_date = local_date.strftime("%Y-%m-%d | %H:%M:%S")
    
    return local_date

#---###---#

def install_libs(package_list_collected):
    
    for package in package_list_collected:
        
        try:
            
            subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
            print(f"({get_time()}) | ✅ Successfully installed: {package}")
            print()
            tm.sleep(1)
            
        except subprocess.CalledProcessError:
            
            print(f"({get_time()}) | ❌ Failed to install: {package}")
            print()
            tm.sleep(1)
            
#---###---#
            
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
    tm.sleep(5)
    
import os
import subprocess
import sys

#---###---#

def install_python():
    """
    Checks if Python is installed. If not, downloads and installs it automatically on Windows.
    """
    try:
        # Verifica se o Python está instalado
        subprocess.run(["python", "--version"], check=True)
        print("✅ Python is already installed.")
    
    except subprocess.CalledProcessError:
        print("⚠️ Python is not installed. Downloading and installing...")

        # URL oficial para baixar o instalador do Python
        python_installer_url = "https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe"
        
        installer_path = os.path.join(os.getcwd(), "python_installer.exe")

        # Baixa o instalador do Python
        subprocess.run(["curl", "-o", installer_path, python_installer_url], check=True)

        # Executa a instalação silenciosa
        subprocess.run([installer_path, "/quiet", "InstallAllUsers=1", "PrependPath=1"], check=True)

        print("✅ Python installation completed successfully.")
        
#---###---#