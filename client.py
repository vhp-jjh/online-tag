import socket
import pickle
from random import randrange

class Client:
  def __init__(self, host, port):
    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.s.connect((host, port))

  def wait_to_start(self):
    data = self.s.recv(1024)
    while len(data) == 0:
      data = self.s.recv(1024)

  def send_vel(self, vel):
    data = pickle.dumps(vel) # Assuming vel is an int tuple (x, y)
    self.s.sendall(data)

  def close_conn(self):
    self.s.close()

  def read_game_data(self): 
    data = self.s.recv(1024)
    msg = pickle.loads(data)
    return msg

if __name__ == "__main__":
  host = '10.32.153.218' # Vitchyr's Gateway
  port = 12121
  client = Client(host, port)

  client.wait_to_start()
  while True:
    client.send_vel((randrange(10), randrange(10)))

    data = client.read_game_data()
    print(data)
  
  #client.close_conn()
