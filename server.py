import socket
import pickle
from random import randrange

class Server:
  def __init__(self, _host, _port):
    self.s = socket.socket(socket.AF_INET)
    self.s.bind((host, port))
    self.conns = []

  def listen_for_conns(self, n_players):
    for n_joined in range(n_players):
      print("Waiting for %d players to connect..." % (n_players - n_joined))
      self.s.listen(5)
      conn, addr = self.s.accept()      # Estabilish connection with client
      print("Got connection from", addr)
      self.conns.append((conn, addr))
  
  def start_game(self):
    for conn, addr in self.conns:
      conn.send(b'\x01')

  def read_vels(self):
    vels = {}
    for conn, addr in self.conns:
      # Test reading and sending tuples
      data = conn.recv(1024)
      if len(data) > 0:
        vels[addr] = pickle.loads(data)
      else:
        vels[addr] = (0,0)
    return vels

  def send_game_data(self, game_data):
    data = pickle.dumps(game_data)
    for conn, addr in self.conns:
      conn.send(data)

  def close_conns(self):
    for conn, addr in self.conns:
      conn.close()
    self.conns = []

if __name__ == "__main__":
  host = '10.32.153.218' # Vitchyr's Gateway
  port = 12121
  server = Server(host, port)
  
  num_players = 2
  server.listen_for_conns(2)
  server.start_game()

  while True:
    vels = server.read_vels()
    print("Received velocities", vels)

    # calculate message
    game_data= [(randrange(10), randrange(10)), (randrange(10),randrange(10))]
    #game_data = engine.get_game_data()

    server.send_game_data(game_data)

    #server.close_conns()
