import os
import socket
import io
import struct

IP = "127.0.0.1"
controlPort = 2121
dataPort = 2222
buffer = 1024
controlSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

def Help():
    list_of_commands = """\nHelp: Display list of commands
List: Get the list of files along with the size of each file
Connect: Connect to the FTP server
Upload <file_path>: Upload a file from the given path
Download <file_path>: Download a file from the given path
Delete <file_path>: Delete a file from the given path
Pwd: Display the current location on the server"""
    print(list_of_commands)

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

    
    

    




command = input("Client is running. Enter your command (type \"Help\" to see commands)\n")
while command!="q":
    if(command.startswith("Help")):
        Help()
    elif(command.startswith("Connect")):
        Connect()
    elif(command.startswith("Upload ")):
        Upload(command[7:])
    elif(command.startswith("Download ")):
        Upload(command[9:])
    else:
        print("\nCommand not found. type \"Help\" to see commands")
    command = input()