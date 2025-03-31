from machine import ADC, Pin
import time

# Setup the flex sensor on an ADC pin (e.g., GPIO34)
flex_sensor = ADC(Pin(34))  # Use an ADC1-compatible pin
flex_sensor.atten(ADC.ATTN_11DB)  # Full range: 0-3.3V

while True:
    sensor_value = flex_sensor.read()  # Read the analog value (0-4095)
    voltage = sensor_value * (3.3 / 4095)  # Convert ADC reading to voltage
    print("Flex Sensor Value:", sensor_value, "| Voltage:", round(voltage, 2), "V")
    time.sleep(0.5)
