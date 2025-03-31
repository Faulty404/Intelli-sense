import serial
import os
import sys
sys.path.append('/home/keyur/.local/lib/python3.12/site-packages')
import time
import vosk
import json



# Bluetooth MAC address of ESP32
ESP32_MAC = "40:91:51:FC:0C:0A"

# Bind Bluetooth device before opening the serial port
os.system(f'sudo rfcomm bind 0 {ESP32_MAC}')
time.sleep(2)

# Open serial connection
try:
    ser = serial.Serial("/dev/rfcomm0", 115200, timeout=1)  # Open Bluetooth serial
    print("Connected to ESP32 Bluetooth on /dev/rfcomm0")
except serial.SerialException as e:
    print("Error:", e)
    exit()

# Load Vosk Speech Recognition Model
MODEL_PATH = "/home/keyur/Downloads/vosk-model-small-en-us-0.15"
if not os.path.exists(MODEL_PATH):
    print("Vosk model not found! Download from https://alphacephei.com/vosk/models")
    exit()

model = vosk.Model(MODEL_PATH)
recognizer = vosk.KaldiRecognizer(model, 16000)  # Vosk expects 16kHz PCM audio

print("Listening for PCM audio from ESP32...")

while True:
    try:
        # Read raw PCM audio data (binary) from Bluetooth
        data = ser.read(100)  # Read 4000 bytes at a time

        if data:
            # Process the PCM audio with Vosk
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")
                print("[VOSK] Recognized Speech:", text)

    except serial.SerialException as e:
        print("Serial error:", e)
        break
    except KeyboardInterrupt:
        print("\nStopping...")
        break

ser.close()

