import serial
import sys
sys.path.append('/home/keyur/.local/lib/python3.12/site-packages')
import numpy as np
import vosk
import json
import wave

# Bluetooth Serial Port
SERIAL_PORT = "/dev/rfcomm0"
BAUD_RATE = 115200

# Vosk Model Path
MODEL_PATH = "/home/keyur/Downloads/vosk-model-small-en-us-0.15"

# Initialize Bluetooth Serial
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

# Load Vosk Model
model = vosk.Model(MODEL_PATH)
recognizer = vosk.KaldiRecognizer(model, 16000)  # 16kHz sample rate

# Buffer to store audio samples
buffer_size = 1024  # Adjust as needed
audio_buffer = np.array([], dtype=np.int16)

print("Listening...")

while True:
    try:
        data = ser.readline().decode().strip()  # Read Bluetooth data
        if data.isdigit():  # Ensure it's a valid number
            sample = np.array([int(data)], dtype=np.int16)
            audio_buffer = np.append(audio_buffer, sample)
            
            # Process audio buffer when enough data is collected
            if len(audio_buffer) >= buffer_size:
                pcm_data = audio_buffer.tobytes()  # Convert to PCM format
                if recognizer.AcceptWaveform(pcm_data):
                    result = json.loads(recognizer.Result())
                    print("Recognized Text:", result["text"])
                
                # Clear buffer after processing
                audio_buffer = np.array([], dtype=np.int16)
    
    except Exception as e:
        print("Error:", e)

