import serial
import os,time

port= serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=1)

port.write('AT'+'\r\n')
rcv = port.read(10)
print rcv
