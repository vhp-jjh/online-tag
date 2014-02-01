import socket

s = socket.socket()
host = socket.gethostname() # Local machine name
port = 12122

s.connect((host, port))
print(s.recv(1024).decode('UTF-8'))
s.close()
