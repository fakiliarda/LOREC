#author Arda Fakılı
import socket
import time
import logging
logging.basicConfig(level=logging.INFO)

host = '35.237.188.57'
port = 5555

connected = False
decodedData=""

def printResult(result):
    print(result)


while True:
    try:
        if not connected:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host,port))
            connected=True
        do = input("Write service to use : ")
        s.send(str.encode(do))
        logging.info("Waiting for Server")
        data = s.recv(1024)
        decoded_data = data.decode('utf-8')    
        printResult(decoded_data)
    except:
        s.close()
        connected = False
        logging.info("No connection with Server")
s.close()


