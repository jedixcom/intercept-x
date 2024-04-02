import pyaudio
import wave

def record_audio(file_name, duration=5):
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

    wf = wave.open(file_name, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def play_audio(file_name):
    CHUNK = 1024

    wf = wave.open(file_name, 'rb')

    audio = pyaudio.PyAudio()

    stream = audio.open(format=audio.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

    print("Playing audio...")

    data = wf.readframes(CHUNK)

    while data:
        stream.write(data)
        data = wf.readframes(CHUNK)

    print("Finished playing audio.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

if __name__ == "__main__":
    file_name = "recorded_audio.wav"
    duration = 5
    
    # Record audio
    record_audio(file_name, duration)
    
    # Play recorded audio
    play_audio(file_name)
