import os
import socket
from pathlib import Path
import struct

#set up the IP and ports
IP = "127.0.0.1"
controlPort = 2121
dataPort = 2222
buffer = 1024

controlSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) #socket for connection control
controlSocket.bind((IP, controlPort)) 
controlSocket.listen() #listen for incoming connection
print("Listening... ")
control_conn, address = controlSocket.accept() #accepted control connection when a client connects
print("Client Accepted")

dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) #socket for data transfer
dataSocket.bind((IP, dataPort))

Path(".\Files On Server").mkdir(parents=True, exist_ok=True)


def List():
    print("Client Requested The List")
    files = [f for f in os.listdir(os.path.join(".", "Files On Server"))] #create a list of files
    control_conn.sendall(struct.pack("i", len(files))) #send number of files
    control_conn.recv(buffer)
    for f in files:
        control_conn.sendall(str(f).encode('utf-8')) #send the name
        control_conn.recv(buffer)
        size = os.path.getsize(os.path.join(".", "Files On Server", f)) #calculate the sixe
        control_conn.sendall(struct.pack("i", size))
        control_conn.recv(buffer)
    

def Upload():
    print("Client Wants To Upload a File")
    dataSocket.listen() #listen for incoming connection
    data_conn,ad = dataSocket.accept() #accept and obtain data connection
    fileName = control_conn.recv(buffer).decode('utf-8') #recieve the file name from client using the control connection
    control_conn.sendall(str(".").encode('utf-8'))
    fileSize = struct.unpack("i", control_conn.recv(buffer))[0] #recieve file size
    control_conn.sendall(str(".").encode('utf-8'))
    file_path = os.path.join(".", "Files On Server", fileName) #create file path
    file = open(file_path, "wb") #create new file with file_path in binary write mode
    comingSize = 0
    print(" Client Is Uploading...")
    while comingSize < fileSize: #recieve and write data chuncks
        chunck = data_conn.recv(buffer)
        file.write(chunck)
        comingSize += buffer
    file.close()
    data_conn.close()
    dataSocket.close()
    print(f"Upload Is Complete On: {file_path}")


def Download():
    dataSocket.listen()
    data_conn,ad = dataSocket.accept()
    fileName = control_conn.recv(buffer).decode('utf-8')
    file_path = os.path.join(".", "Files On Server", fileName)
    fileSize = os.path.getsize(file_path)
    control_conn.sendall(struct.pack("i", fileSize))
    file = open(file_path, "rb") #open file in binary read mode
    chunk = file.read(buffer)
    print("Client Is Downloading...")
    while chunk:
        data_conn.sendall(chunk)
        chunk = file.read(buffer)
    file.close()
    data_conn.close()
    dataSocket.close()
    print("Client Download Is Complete")


def Delete():
    fileName = control_conn.recv(buffer).decode('utf-8')
    file_path = os.path.join(".", "Files On Server", fileName)
    os.remove(file_path)
    print(f"Client Deleted A File On {file_path}")
    

def Pwd():
    control_conn.recv(buffer)
    path = os.path.join(os.getcwd(), "Files On Server")
    control_conn.sendall(path.encode('utf-8'))
    print("Client Wants Current Directory")



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
