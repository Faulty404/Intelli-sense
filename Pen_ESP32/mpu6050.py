from machine import Pin, I2C
import time


MPU6050_ADDR = 0x68
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

class MPU6050:
    def __init__(self, i2c, addr=MPU6050_ADDR):
        self.i2c = i2c
        self.addr = addr
        self.i2c.writeto_mem(self.addr, PWR_MGMT_1, b'\x00') 
    def read_raw_data(self, addr):
        high, low = self.i2c.readfrom_mem(self.addr, addr, 2)
        value = (high << 8) | low
        if value > 32768:
            value -= 65536
        return value

    def get_accel_gyro(self):
        accel_x = self.read_raw_data(ACCEL_XOUT_H) / 16384.0
        accel_y = self.read_raw_data(ACCEL_XOUT_H + 2) / 16384.0
        accel_z = self.read_raw_data(ACCEL_XOUT_H + 4) / 16384.0
        
        gyro_x = self.read_raw_data(GYRO_XOUT_H) / 131.0
        gyro_y = self.read_raw_data(GYRO_XOUT_H + 2) / 131.0
        gyro_z = self.read_raw_data(GYRO_XOUT_H + 4) / 131.0
        
        return {
            "accel": (accel_x, accel_y, accel_z),
            "gyro": (gyro_x, gyro_y, gyro_z)
        }

i2c = I2C(0, scl=Pin(22), sda=Pin(21))

mpu = MPU6050(i2c)

while True:
    data = mpu.get_accel_gyro()
    print("Accel: X={:.2f} Y={:.2f} Z={:.2f}".format(*data["accel"]))
    print("Gyro: X={:.2f} Y={:.2f} Z={:.2f}".format(*data["gyro"]))
    print("-" * 30)
    time.sleep(1)
