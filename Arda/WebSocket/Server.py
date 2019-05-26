#author Arda Fakılı
import socket
import time
import logging

logging.basicConfig(level=logging.INFO)

global connections
connections = []
global connected
connected = False

host = '35.237.188.57'
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((host, port))
except socket.error as e:
    print(str(e))

s.listen(2)
logging.info("Server is waiting for connection")

def do(msg):
    if msg=="FaceDetection":
        value="Face Detected"
    elif msg=="exit":
	    value="close"
    else:
	    value="Wrong Service Parameter"
    logging.info("Client : " + msg)
    return value

def start_service(conn):
    try:
        if connected:
            while True:
                logging.info("Ready and Waiting for Client")
                data = conn.recv(1024)
                decoded_data = data.decode('utf-8')
                message = do(decoded_data)
                if message=="close":
                    exit()
                conn.send(str.encode("Server : "+message))
    except ConnectionResetError as cr:
        logging.info("Disconnected :" + str(conn.getpeername()))
        connections.remove(conn)
        conn.close()
    except UnicodeDecodeError as ue:
        print(ue)
    except:
        logging.info("Disconnected :" + str(conn.getpeername()))
        connections.remove(conn)
        conn.close()

while True:
    try:
        conn, addr = s.accept()
        logging.info('Server is connected to: ' + addr[0] + ':' + str(addr[1]))
        connected = True
        start_service(conn)
    except:
        conn.close()