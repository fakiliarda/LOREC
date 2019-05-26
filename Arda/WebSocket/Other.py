#author Arda Fakılı

import socket
import time
import logging
logging.basicConfig(level=logging.INFO)

host = '127.0.0.1'
port = 5555

connected = False
otherAppConnection = False
decodedData=""

def sum(num1,num2):
    return str(float(num1)+float(num2))
def sub(num1,num2):
    return str(float(num1)-float(num2))
def mult(num1,num2):
    return str(float(num1)*float(num2))
def div(num1,num2):
    return str(float(num1) / float(num2))


while True:
    try:
        if not connected:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host,port))
            connected=True
        while not otherAppConnection :
            data = s.recv(1024)
            decodedData = data.decode('utf-8')
            logging.info(decodedData)
            if decodedData == "start":
                otherAppConnection = True


        while True:
            data = s.recv(1024)
            if data.decode('utf-8') == "Connection error with other app":
                otherAppConnection = False
                s.send(str.encode("Waiting"))
                break
            decodedData = data.decode('utf-8')
            print("Received data: " +decodedData)
            first = decodedData.split("_")[0]
            if first is '+' or first is '-' or first is '*' or first is '/':
                operation = decodedData.split("_")[0]
                num1 = decodedData.split("_")[1]
                num2 = decodedData.split("_")[2]
                if operation is '+':
                    s.send(str.encode(sum(num1, num2)))
                elif operation is '-':
                    s.send(str.encode(sub(num1, num2)))
                elif operation is '*':
                    s.send(str.encode(mult(num1, num2)))
                elif operation is '/':
                    s.send(str.encode(div(num1, num2)))
                else:
                    s.send(str.encode("Invalid Input"))
                print("Result Sent...")
            else:
                print("Invalid Input")
                s.send(str.encode("Invalid Input"))

            if not data:
                break

    except socket.error as e:
        connected=False
        logging.info("No connection with app3")
        connected=False
        otherAppConnection=False
        time.sleep(1)
    except ValueError as ve:
        s.send(str.encode("Wrong Parameter"))
s.close()

