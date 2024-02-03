import os
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


def List():
    files = [f for f in os.listdir("./Files On Server")]
    control_conn.sendall(struct.pack("i", len(files)))
    control_conn.recv(buffer)
    for f in files:
        control_conn.sendall(str(f).encode('utf-8'))
        control_conn.recv(buffer)
        size = os.path.getsize("./Files On Server/" + f)
        control_conn.sendall(struct.pack("i", size))
        control_conn.recv(buffer)
    

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
    data_conn.close()


def Download():
    dataSocket.listen()
    data_conn,ad = dataSocket.accept()
    fileName = control_conn.recv(buffer).decode('utf-8')
    file_path = "./Files On Server/" + fileName
    fileSize = os.path.getsize(file_path)
    control_conn.sendall(struct.pack("i", fileSize))
    file = open(file_path, "rb")
    chunk = file.read(buffer)
    while chunk:
        data_conn.sendall(chunk)
        chunk = file.read(buffer)
    file.close()
    data_conn.close()


def Delete():
    fileName = control_conn.recv(buffer).decode('utf-8')
    file_path = "./Files On Server/" + fileName
    os.remove(file_path)
    

def Pwd():
    control_conn.recv(buffer)
    path = os.getcwd()
    control_conn.sendall(path.encode('utf-8'))



while True:
    command = control_conn.recv(buffer).decode('utf-8')
    control_conn.sendall(str(".").encode('utf-8'))
    match command:
        case "List":
            List()
        case "Upload":
            Upload()
        case "Download":
            Download()
        case "Delete":
            Delete()
        case "Pwd":
            Pwd()