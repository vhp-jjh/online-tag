import socket

s = socket.socket()
host = socket.gethostname() # Local machine name
port = 12122
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # forcefully take
                                                        # the address
s.bind((host, port))

s.listen(5)
while True:
  c, addr = s.accept()      # Estabilish connection with client
  print("Got connection from", addr)
  msg = "Thank you for connecting"
  c.send(msg.encode('UTF-8'))
  c.close()
