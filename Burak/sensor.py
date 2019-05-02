import serial
import time

ser = serial.Serial('COM3', 9600, timeout=0.0000001)

while 1:
    arduinodata = ser.readline().decode('ascii')
    print(arduinodata) 

  
ser.close()       
