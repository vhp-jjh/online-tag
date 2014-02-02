import socket
import pickle
import time
import constants
from engine import Engine

class Server:
  def __init__(self, host, port):
    self.engine = Engine()
    self.s = socket.socket(socket.AF_INET)
    self.s.bind((host, port))
    self.conns = []
    self.addr_to_color_map = {}

  def listen_for_conns(self, n_players):
    for n_joined in range(n_players):
      print("Waiting for %d players to connect..." % (n_players - n_joined))
      self.s.listen(5)
      conn, addr = self.s.accept()      # Estabilish connection with client
      print("Got connection from", addr)
      self.conns.append((conn, addr))
      color = self.engine.add_player()
      self.addr_to_color_map[addr] = color
  
  def send_data(self, data):
    msg = pickle.dumps(data)
    for conn, addr in self.conns:
      conn.send(msg)
  
  def start_game(self):
    game_data = self.engine.get_game_data()
    self.send_data(game_data)

  def update_players(self):
    players = self.engine.get_players()
    self.send_data(players)

  def update_vels(self):
    for conn, addr in self.conns:
      data = conn.recv(1024)
      if len(data) > 0:
        vel = pickle.loads(data)
        color = self.addr_to_color_map[addr]
        self.engine.update_velocity(color, vel)

  def close_conns(self):
    for conn, addr in self.conns:
      conn.close()
    self.conns = []

  def play(self):
    while True:
      # I don't think server should delay
      #start = time.time()

      self.update_players()
      self.update_vels()
      
      #delay_left = constants.LOOP_TIME - (time.time() - start)
      #if delay_left > 0:
      #  time.sleep(delay_left)

if __name__ == "__main__":
  server = Server(constants.HOST, constants.PORT)
  
  server.listen_for_conns(constants.N_PLAYERS)
  server.start_game()

  server.play()
