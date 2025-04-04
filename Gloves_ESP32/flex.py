from machine import ADC, Pin
import time

flex_sensor_thumb = ADC(Pin(32)) 
flex_sensor_index = ADC(Pin(33)) 
flex_sensor_mid = ADC(Pin(34)) 
flex_sensor_ring = ADC(Pin(35)) 
flex_sensor_pinky = ADC(Pin(25)) 

flex_sensor_thumb.atten(ADC.ATTN_11DB) 
flex_sensor_index.atten(ADC.ATTN_11DB) 
flex_sensor_mid.atten(ADC.ATTN_11DB) 
flex_sensor_ring.atten(ADC.ATTN_11DB)
flex_sensor_pinky.atten(ADC.ATTN_11DB)


while True:
    sensor_value_thumb = flex_sensor_thumb.read()
    sensor_value_index = flex_sensor_index.read()
    sensor_value_mid = flex_sensor_mid.read()  
    sensor_value_ring = flex_sensor_ring.read()
    sensor_value_pinky = flex_sensor_pinky.read()
    print("Thumb Sensor Value:", sensor_value_thumb)
    print("Index Sensor Value:", sensor_value_index)
    print("Middle Sensor Value:", sensor_value_mid)
    print("Ring Sensor Value:", sensor_value_ring)
    print("Pinky Sensor Value:", sensor_value_pinky)
    time.sleep(0.5)

