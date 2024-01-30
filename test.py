from io import SEEK_END
import os
file_path = "/home/zahra/A/Darsi/Computer Networking/Chapter1.pdf"
filename = os.path.basename(file_path)
file = open(file_path)
print(filename)
print(type(filename))
file.seek(0, SEEK_END)
print(os.path.getsize(file_path))
print(file.tell())
