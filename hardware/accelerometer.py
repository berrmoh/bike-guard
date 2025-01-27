import smbus
import time
import math
import requests
import sys
import gpiozero

from gpiozero import Buzzer
from time import sleep


# Define the MPU-6050 I2C address and registers
MPU6050_ADDRESS = 0x68
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47

# Initialize the I2C bus
bus = smbus.SMBus(1)

# Initialize MPU-6050
def init_mpu():
    bus.write_byte_data(MPU6050_ADDRESS, PWR_MGMT_1, 0)

# Read raw data from a register (two bytes)
def read_raw_data(register):
    high = bus.read_byte_data(MPU6050_ADDRESS, register)
    low = bus.read_byte_data(MPU6050_ADDRESS, register + 1)
    value = (high << 8) + low
    if value > 32768:
        value = value - 65536
    return value

# Main function to read accelerometer and gyroscope data
def read_mpu_data():
    # Read accelerometer data
    accel_x = read_raw_data(ACCEL_XOUT_H)
    accel_y = read_raw_data(ACCEL_YOUT_H)
    accel_z = read_raw_data(ACCEL_ZOUT_H)

    # Read gyroscope data
    gyro_x = read_raw_data(GYRO_XOUT_H)
    gyro_y = read_raw_data(GYRO_YOUT_H)
    gyro_z = read_raw_data(GYRO_ZOUT_H)

    # Convert to g and degrees per second
    accel_x /= 16384.0
    accel_y /= 16384.0
    accel_z /= 16384.0
    gyro_x /= 131.0
    gyro_y /= 131.0
    gyro_z /= 131.0

    return {
        "accel": {"x": accel_x, "y": accel_y, "z": accel_z},
        "gyro": {"x": gyro_x, "y": gyro_y, "z": gyro_z}
    }

# Calculate pitch and roll
def calculate_pitch_roll(accel):
    ax = accel["x"]
    ay = accel["y"]
    az = accel["z"]

    pitch = math.atan2(ay, math.sqrt(ax * ax + az * az)) * (180 / math.pi)
    roll = math.atan2(-ax, az) * (180 / math.pi)
    
    #--------------Buzzer code start

    # Initialize the buzzer
    buzzer = Buzzer(17)

    #print("Buzzer on/off loop. Press Ctrl+C to stop.")
    try:
        #while True:
        #  buzzer.on()  # Turn on the buzzer
        #   sleep(1)     # Wait for 1 second
        #  buzzer.off() # Turn off the buzzer
        #  sleep(1)     # Wait for 1 second
        
        #Pick a treshold value to trigger the buzzer:    
        if pitch > 5 or roll > 10:
            print("Buzzer on")
            buzzer.on()  # Turn on the buzzer
            sleep(1)     # Wait for 1 second
            #buzzer.off() # Turn off the buzzer
            #sleep(1)     # Wait for 1 second
            
    except KeyboardInterrupt:
        print("\nExiting program.")
    #--------------Buzzer code end

    return pitch, roll

# Initialize MPU
init_mpu()


    
    
    
# Collect data
try:
    while True:
        data = read_mpu_data()
        pitch, roll = calculate_pitch_roll(data["accel"])
        
        #data adapted to work well for csv 
        print(f"{data['accel']['x']:.2f}, {data['accel']['y']:.2f}, {data['accel']['z']:.2f}, {data['gyro']['x']:.2f}, {data['gyro']['y']:.2f}, {data['gyro']['z']:.2f}, {pitch:.2f}, {roll:.2f}")
        sys.stdout.flush()  # Add this line to flush the output buffer

        time.sleep(1)
except KeyboardInterrupt:
    print("Measurement stopped by User")
