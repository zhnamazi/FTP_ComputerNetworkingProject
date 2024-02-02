import os
from pathlib import Path
import socket
import io
import struct

IP = "127.0.0.1"
controlPort = 2121
dataPort = 2222
buffer = 1024
controlSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

Path("./Download Folder").mkdir(parents=True, exist_ok=True)


def Help():
    list_of_commands = """\nHelp: Display list of commands
List: Get the list of files along with the size of each file
Connect: Connect to the FTP server
Upload <file_path>: Upload a file from the given path
Download <file_path>: Download a file from the given path
Delete <file_path>: Delete a file from the given path
Pwd: Display the current location on the server"""
    print(list_of_commands)


def List():
    controlSocket.sendall(str("List").encode('utf-8'))
    controlSocket.recv(buffer)
    controlSocket.sendall(str(".").encode('utf-8'))
    num = struct.unpack("i" ,controlSocket.recv(buffer))[0]
    for i in range(num):
        name = controlSocket.recv(buffer).decode('utf-8')
        controlSocket.sendall(str(".").encode('utf-8'))
        size = struct.unpack("i", controlSocket.recv(buffer))[0]
        controlSocket.sendall(str(".").encode('utf-8'))
        # changed_size = size/1000
        # if(size > 1000):
        #     changed_size = changed_size / 1000
        print(name, '   ', size)


def Connect():
    try:
        controlSocket.connect((IP,controlPort))
    except:
        "unsuccessful connection"


def Upload(file_path):
    controlSocket.sendall(str("Upload").encode('utf-8'))
    controlSocket.recv(buffer)
    dataSocket.connect((IP, dataPort))
    fileName = os.path.basename(file_path)
    controlSocket.sendall(fileName.encode('utf-8'))
    controlSocket.recv(buffer)
    fileSize = os.path.getsize(file_path)
    controlSocket.sendall(struct.pack("i", fileSize))
    controlSocket.recv(buffer)
    file = open(file_path, "rb")
    chunk = file.read(buffer)
    while chunk:
        dataSocket.sendall(chunk)
        chunk = file.read(buffer)
    file.close()
    dataSocket.close()


def Download(fileName):
    controlSocket.sendall(str("Download").encode('utf-8'))
    controlSocket.recv(buffer)
    dataSocket.connect((IP, dataPort))
    controlSocket.sendall(fileName.encode('utf-8'))
    fileSize = struct.unpack("i", controlSocket.recv(buffer))[0]
    file_path = "./Download Folder/" + fileName
    file = open(file_path, "wb")
    comingSize = 0
    while comingSize < fileSize:
        chunk = dataSocket.recv(buffer)
        file.write(chunk)
        comingSize += buffer
    file.close()
    dataSocket.close()


def Delete(fileName):
    controlSocket.sendall(str("Delete").encode('utf-8'))
    controlSocket.recv(buffer)
    controlSocket.sendall(fileName.encode('utf-8'))
       

def Pwd():
    controlSocket.sendall(str("Pwd").encode('utf-8'))
    controlSocket.recv(buffer)
    controlSocket.sendall(str(".").encode('utf-8'))
    path = controlSocket.recv(buffer).decode('utf-8')
    print(path)


command = input("Client is running. Enter your command (type \"Help\" to see commands)\n")
while command!="q":
    if command.startswith("Help"):
        Help()
    elif command.startswith("List"):
        List()
    elif command.startswith("Connect"):
        Connect()
    elif command.startswith("Upload "):
        Upload(command[7:])
    elif command.startswith("Download "):
        Download(command[9:])
    elif command.startswith("Delete "):
        Delete(command[7:])
    elif command.startswith("Pwd"):
        Pwd()
    else:
        print("\nCommand not found. type \"Help\" to see commands")
    command = input()

controlSocket.close()