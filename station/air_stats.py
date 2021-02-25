#
# written by @author ZyzonixDev
# published by ZyzonixDevelopments
# -
# date      | Sun Jan 03 2021
# python-v  | 3.5.3
# -
# file      | air_stats.py
# -
# USING FOLLOWING RESSOURCE(S):
# -
# Author : Matt Hawkins
# Date   : 21/01/2018
# - 
# https://www.raspberrypi-spy.co.uk/
# -
#--------------------------------------
from ctypes import c_short
from ctypes import c_byte
from ctypes import c_ubyte
import smbus
import time

# access to values: station.air_stats.get<VALUE>()

DEVICE = 0x76 # Default device I2C address
# Register Addresses
REG_DATA = 0xF7
REG_CONTROL = 0xF4
REG_CONTROL_HUM = 0xF2

# Oversample setting - page 27
OVERSAMPLE_TEMP = 2
OVERSAMPLE_PRES = 2
OVERSAMPLE_HUM = 2
MODE = 1

def getShort(data, index):
    # return two bytes from data as a signed 16-bit value
    return c_short((data[index+1] << 8) + data[index]).value

def getUShort(data, index):
    # return two bytes from data as an unsigned 16-bit value
    return (data[index+1] << 8) + data[index]    

def getChar(data,index):
    # return one byte from data as a signed char
    result = data[index]
    if result > 127:
        result -= 256
    return result  

def getUChar(data,index):
    # return one byte from data as an unsigned char
    result =  data[index] & 0xFF
    return result

# NEVER USED
def readBME280ID(addr=DEVICE):
    # initializing device bus if not available
    bus = smbus.SMBus(1)
    # Chip ID Register Address
    REG_ID     = 0xD0
    (chip_id, chip_version) = bus.read_i2c_block_data(addr, REG_ID, 2)
    return (chip_id, chip_version)


# getting current temperature 
def getTemperature():
    # initializing device bus if not available
    bus = smbus.SMBus(1)
    # Oversample setting
    control = OVERSAMPLE_TEMP<<5 | OVERSAMPLE_PRES<<2 | MODE
    bus.write_byte_data(DEVICE, REG_CONTROL, control)

    # Convert byte data to word values
    cal1 = bus.read_i2c_block_data(DEVICE, 0x88, 24)
    dig_T1 = getUShort(cal1, 0)
    dig_T2 = getShort(cal1, 2)
    dig_T3 = getShort(cal1, 4)
    
    # Wait in ms 
    wait_time = 1.25 + (2.3 * OVERSAMPLE_TEMP)
    # Wait the required time 
    time.sleep(wait_time/1000)  
    
    # Reading data a second time
    data = bus.read_i2c_block_data(DEVICE, REG_DATA, 8)

    # Calculating raw value
    temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)   
    var1 = ((((temp_raw>>3)-(dig_T1<<1)))*(dig_T2)) >> 11
    var2 = (((((temp_raw>>4) - (dig_T1)) * ((temp_raw>>4) - (dig_T1))) >> 12) * (dig_T3)) >> 14
    
    # Storing values in temp array (function can be used for raw temp / calculation of pressure)
    t_fine = var1+var2
    temp = float(((t_fine * 5) + 128) >> 8)/100.0
    temp_array = [temp, t_fine]
    return temp_array #[0] = final value in degrees (Celcius) [1] = raw value for pressure / humidity


# getting current humidity
def getHumidity():
    # initializing device bus if not available
    bus = smbus.SMBus(1)
    # Oversample setting for humidity register
    bus.write_byte_data(DEVICE, REG_CONTROL_HUM, OVERSAMPLE_HUM)
 
    # Convert byte data to word values
    cal2 = bus.read_i2c_block_data(DEVICE, 0xA1, 1)
    cal3 = bus.read_i2c_block_data(DEVICE, 0xE1, 7)
    
    dig_H1 = getUChar(cal2, 0)
    dig_H2 = getShort(cal3, 0)
    dig_H3 = getUChar(cal3, 2)
    dig_H4 = getChar(cal3, 3)
    dig_H4 = (dig_H4 << 24) >> 20
    dig_H4 = dig_H4 | (getChar(cal3, 4) & 0x0F)
    dig_H5 = getChar(cal3, 5)
    dig_H5 = (dig_H5 << 24) >> 20
    dig_H5 = dig_H5 | (getUChar(cal3, 4) >> 4 & 0x0F)
    dig_H6 = getChar(cal3, 6)

    # Wait in ms 
    wait_time = 1.25 + (2.3 * OVERSAMPLE_HUM) + 0.575
    # Wait the required time 
    time.sleep(wait_time/1000)   

    # Reading data a second time --> getting raw value
    data = bus.read_i2c_block_data(DEVICE, REG_DATA, 8)
    
    # Calculating raw value
    hum_raw = (data[6] << 8) | data[7]

    # Refine humidity
    humidity = float(getTemperature()[1]) - 76800.0
    humidity = (hum_raw - (dig_H4 * 64.0 + dig_H5 / 16384.0 * humidity)) * (dig_H2 / 65536.0 * (1.0 + dig_H6 / 67108864.0 * humidity * (1.0 + dig_H3 / 67108864.0 * humidity)))
    humidity = humidity * (1.0 - dig_H1 * humidity / 524288.0)
    
    # Compensation of wrong calculations
    if humidity > 100:
        humidity = 100
    elif humidity < 0:
        humidity = 0

    return humidity    


# getting current air pressure
def getPressure():
    # initializing device bus if not available
    bus = smbus.SMBus(1)
    # Oversample setting
    control = OVERSAMPLE_TEMP<<5 | OVERSAMPLE_PRES<<2 | MODE
    bus.write_byte_data(DEVICE, REG_CONTROL, control)

    # Convert byte data to word values 
    cal1 = bus.read_i2c_block_data(DEVICE, 0x88, 24) 
    dig_P1 = getUShort(cal1, 6)
    dig_P2 = getShort(cal1, 8)
    dig_P3 = getShort(cal1, 10)
    dig_P4 = getShort(cal1, 12)
    dig_P5 = getShort(cal1, 14)
    dig_P6 = getShort(cal1, 16)
    dig_P7 = getShort(cal1, 18)
    dig_P8 = getShort(cal1, 20)
    dig_P9 = getShort(cal1, 22)

    # Wait in ms 
    wait_time = 1.25 + (2.3 * OVERSAMPLE_PRES) + 0.575
    # Wait the required time 
    time.sleep(wait_time/1000)   

    # Reading data a second time --> getting raw value
    data = bus.read_i2c_block_data(DEVICE, REG_DATA, 8)
    pres_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)

    # getting temperature value
    t_fine = getTemperature()[1]

    # Refine pressure and adjust for temperature
    var1 = t_fine / 2.0 - 64000.0
    var2 = var1 * var1 * dig_P6 / 32768.0
    var2 = var2 + var1 * dig_P5 * 2.0
    var2 = var2 / 4.0 + dig_P4 * 65536.0
    var1 = (dig_P3 * var1 * var1 / 524288.0 + dig_P2 * var1) / 524288.0
    var1 = (1.0 + var1 / 32768.0) * dig_P1
    if var1 == 0:
        pressure=0
    else:
        pressure = 1048576.0 - pres_raw
        pressure = ((pressure - var2 / 4096.0) * 6250.0) / var1
        var1 = dig_P9 * pressure * pressure / 2147483648.0
        var2 = pressure * dig_P8 / 32768.0
        pressure = pressure + (var1 + var2 + dig_P7) / 16.0
    
    pressure = pressure/100.0
    return pressure
