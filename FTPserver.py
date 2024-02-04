import os
from pathlib import Path
import socket
import io
import struct
import time

#set up the IP and ports
IP = "127.0.0.1"
controlPort = 2121
dataPort = 2222
buffer = 1024
# communication control socket 
controlSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
# the directory where downloaded files will be stored
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
    controlSocket.sendall(str("List").encode('utf-8')) #send List command 
    controlSocket.recv(buffer)  #recive an acknowledgment from the server
    controlSocket.sendall(str(".").encode('utf-8'))  #send placeholder character
    num = struct.unpack("i" ,controlSocket.recv(buffer))[0] #recieve number of files from server
    if num == 0:
        print("No Files On Server")
    for i in range(num):
        name = controlSocket.recv(buffer).decode('utf-8')
        controlSocket.sendall(str(".").encode('utf-8'))
        size = struct.unpack("i", controlSocket.recv(buffer))[0]
        controlSocket.sendall(str(".").encode('utf-8'))
        # changed_size = size/1000
        # if(size > 1000):
        #     changed_size = changed_size / 1000
        print(f"File #{i+1} with Name {name} and Size: {size} bytes")


def Connect():
    try:
        controlSocket.connect((IP,controlPort)) #connect to server with IP addr of the server
                                                #and the port on which the server's listening
        print("Connected")
    except:
        "unsuccessful connection"


def Upload(file_path):
    # time.sleep(1)
    controlSocket.sendall(str("Upload").encode('utf-8'))  #send Upload command
    controlSocket.recv(buffer)
    dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    dataSocket.connect((IP, dataPort))
    print("You Are Connected To The Server")
    fileName = os.path.basename(file_path) #extract file name from path
    controlSocket.sendall(fileName.encode('utf-8')) #send file name to server
    controlSocket.recv(buffer)
    fileSize = os.path.getsize(file_path) #calculate file size
    controlSocket.sendall(struct.pack("i", fileSize)) #send file size to server
    controlSocket.recv(buffer)
    try:
        file = open(file_path, "rb") #open file in binary mode
        chunk = file.read(buffer) # read the file in chunk of size given by buffer
        print("Uploading...")
        while chunk:
            dataSocket.sendall(chunk)  #send each chunck
            chunk = file.read(buffer)
    except Exception as e:
        print(f"Error While Uploading File: {e}")
    finally:
        print("Upload Is Complete")
        file.close()
        dataSocket.close()


def Download(fileName):
    controlSocket.sendall(str("Download").encode('utf-8'))
    controlSocket.recv(buffer)
    dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    dataSocket.connect((IP, dataPort))
    print("You Are Connected To The Server")
    controlSocket.sendall(fileName.encode('utf-8'))
    fileSize = struct.unpack("i", controlSocket.recv(buffer))[0]
    file_path = "./Download Folder/" + fileName
    file = open(file_path, "wb") #create local file in binary write mode
    comingSize = 0
    print("Downloading...")
    while comingSize < fileSize:
        chunk = dataSocket.recv(buffer)
        file.write(chunk)
        comingSize += buffer
    print("Download Is Complete")
    file.close()
    dataSocket.close()


def Delete(fileName):
    controlSocket.sendall(str("Delete").encode('utf-8'))  #send delete command
    controlSocket.recv(buffer)
    controlSocket.sendall(fileName.encode('utf-8')) #indicate which file should be deleted
    print("Delete Is Complete")
       

def Pwd():
    controlSocket.sendall(str("Pwd").encode('utf-8'))
    controlSocket.recv(buffer)
    controlSocket.sendall(str(".").encode('utf-8'))
    path = controlSocket.recv(buffer).decode('utf-8')
    print(f"Current Directory: {path}")


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
