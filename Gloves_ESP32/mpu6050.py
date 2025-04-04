from machine import Pin, I2C
import time
import math

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

def std_dev(values):
    mean = sum(values) / len(values)
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    return math.sqrt(variance)

# Initialize I2C and MPU
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
mpu = MPU6050(i2c)

gyro_x_vals = []
gyro_y_vals = []
gyro_z_vals = []


accel_x_vals = []
accel_y_vals = []
accel_z_vals = []

SAMPLE_SIZE = 20  
THRESHOLD = 30.5
ACC_THRESHOLD = 50

while True:
    data = mpu.get_accel_gyro()
    gx, gy, gz = data["gyro"]
    data_acc = mpu.get_accel_gyro()
    ax, ay ,az = data["accel"]
    
    gyro_x_vals.append(gx)
    gyro_y_vals.append(gy)
    gyro_z_vals.append(gz)


    accel_x_vals.append(ax)
    accel_y_vals.append(ay)
    accel_z_vals.append(az)
    
    if len(gyro_x_vals) >= SAMPLE_SIZE and len(accel_x_vals) >= SAMPLE_SIZE:
        std_x = std_dev(gyro_x_vals)
        std_y = std_dev(gyro_y_vals)
        std_z = std_dev(gyro_z_vals)
        
        std_x_acc = std_dev(accel_x_vals)
        std_y_acc = std_dev(accel_y_vals)
        std_z_acc = std_dev(accel_z_vals)
        
        avg_std = (std_x + std_y + std_z) / 3
        avg_std_acc = (std_x_acc + std_y_acc + std_z_acc) / 3

        print("Gyro STD -> X={:.2f} Y={:.2f} Z={:.2f} | AVG STD={:.2f}".format(std_x, std_y, std_z, avg_std))
        print("Acc STD -> X={:.2f} Y={:.2f} Z={:.2f} | AVG STD={:.2f}".format(std_x_acc, std_y_acc, std_z_acc, avg_std_acc))

        if avg_std > THRESHOLD and avg_std_acc < ACC_THRESHOLD:
            print("🔴 Hand is SHAKY")
        else:
            print("🟢 Hand is STABLE")

        print("-" * 40)
        # Clear buffers for next round
        gyro_x_vals.clear()
        gyro_y_vals.clear()
        gyro_z_vals.clear()
        
        accel_x_vals.clear()
        accel_y_vals.clear()
        accel_z_vals.clear()
        
#     if len(accel_x_vals) >= SAMPLE_SIZE:
#         
# 
#         avg_std_acc = (std_x_acc + std_y_acc + std_z_acc) / 3
# 
#         print("Acc STD -> X={:.2f} Y={:.2f} Z={:.2f} | AVG STD={:.2f}".format(std_x_acc, std_y_acc, std_z_acc, avg_std_acc))
# # 
# #         if avg_std_acc > ACC_THRESHOLD:
# #             print("🔴 Hand is SHAKY")
# #         else:
# #             print("🟢 Hand is STABLE")
# # 
# #         print("-" * 40)
#         # Clear buffers for next round
#         accel_x_vals.clear()
#         accel_y_vals.clear()
#         accel_z_vals.clear()

    time.sleep(0.05)
