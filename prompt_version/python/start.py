import subprocess  # For running external system commands and processes
import time as tm  # Standard time module for delays

#---###---#

# Runs Python script 'main.py' in a new Windows console window
def start_emicore():
    # Sets console code page to 65001 (UTF-8) for proper Unicode support
    command = 'chcp 65001 > nul && python main.py'
    
    # Opens a new console window and executes the command, leaving the window open after execution
    subprocess.run(["cmd.exe", "/K", command], creationflags=subprocess.CREATE_NEW_CONSOLE)

#---###---#

try:
    tm.sleep(2)  # Waits 2 seconds before starting to smooth startup
    
    # Calls function to launch the Emicore application
    start_emicore()

except ValueError as error:
    # Catches and prints any ValueError during initialization
    print(f"Error captured at initialization: {error}")
    tm.sleep(10)  # Waits 10 seconds to allow the user to see the error message