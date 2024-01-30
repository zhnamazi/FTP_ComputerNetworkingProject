import socket
from pathlib import Path
import struct

IP = "127.0.0.1"
controlPort = 2121
dataPort = 2222
buffer = 1024
controlSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
controlSocket.bind((IP, controlPort))
controlSocket.listen()
control_conn, address = controlSocket.accept()

dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
dataSocket.bind((IP, dataPort))

Path("./Files On Server").mkdir(parents=True, exist_ok=True)



def Upload():
    dataSocket.listen()
    data_conn,ad = dataSocket.accept()
    fileName = control_conn.recv(buffer).decode('utf-8')
    control_conn.sendall(str(".").encode('utf-8'))
    fileSize = struct.unpack("i", control_conn.recv(buffer))[0]
    control_conn.sendall(str(".").encode('utf-8'))
    file_path = "./Files On Server/" + fileName
    file = open(file_path, "wb")
    comingSize = 0
    while comingSize < fileSize:
        chunck = data_conn.recv(buffer)
        file.write(chunck)
        comingSize += buffer
    file.close()
    dataSocket.close()
    

while True:
    command = control_conn.recv(buffer).decode('utf-8')
    control_conn.sendall(str(".").encode('utf-8'))
    match command:
        case "Upload":
            Upload()