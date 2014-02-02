import socket
import pickle
from random import randrange

class Client:
  def __init__(self, host, port):
    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.s.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
    self.s.connect((host, port))
    self.game_data = self.wait_to_start()

  def wait_to_start(self):
    data = self.s.recv(1024)
    while len(data) == 0:
      data = self.s.recv(1024)
    game_data = pickle.loads(data)
    return game_data

  def update_velocity(self, vel):
    data = pickle.dumps(vel) # Assuming vel is an int tuple (x, y)
    self.s.sendall(data)

  def get_players(self): 
    data = self.s.recv(1024)
    msg = pickle.loads(data)
    return msg

  def get_game_data(self):
    return self.game_data

  def close_conn(self):
    self.s.close()

# To test
if __name__ == "__main__":
  host = '10.32.153.218' # Vitchyr's Gateway
  port = 12121
  client = Client(host, port)

  while True:
    vel = randrange(10), randrange(10)
    client.update_velocity(vel)
    print("Vel sent", vel)

    players = client.get_players()
    print(players)
