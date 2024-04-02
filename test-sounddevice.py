import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write

# Configuration
fs = 44100  # Sample rate
duration = 5  # Duration of recording in seconds
filename = 'output.wav'  # Filename to save the recording

def record_audio(duration, filename, fs):
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='float64')
    sd.wait()  # Wait until recording is finished
    write(filename, fs, recording)  # Save as WAV file
    print(f"Recording saved as {filename}")

if __name__ == "__main__":
    record_audio(duration, filename, fs)
