import socket
import pickle
import time
import constants
from engine import Engine

CLOSE = "close"

class Server:
  def __init__(self, port):
    self.engine = Engine()
    # TODO: Maybe move these to this file
    self.s = socket.socket(constants.S_FAMILY, constants.S_TYPE)
    self.s.bind(("", port)) # "" = all available interfaces
    self.addresses = [] # List of addresses
    self.addr_to_color_map = {}

  def listen_for_conns(self, n_players):
    for n_joined in range(n_players):
      print("Waiting for %d players to connect..." % (n_players - n_joined))
      data = ""
      while data == "" or data == None:
        data, addr = self.s.recvfrom(1024)

      self.addresses.append(addr)
      self.addr_to_color_map[addr] = self.engine.add_player()
  
  def send_data(self, data):
    msg = pickle.dumps(data)
    for addr in self.addresses:
      self.s.sendto(msg, addr)
  
  def start_game(self):
    game_data = self.engine.get_game_data()
    self.send_data(game_data)

  def update_players(self):
    players = self.engine.get_players()
    self.send_data(players)

  def update_vels(self):
    for addr in self.addresses:
      data, addr_recv = self.s.recvfrom(1024)
      if len(data) > 0 and addr_recv == addr:
        vel = pickle.loads(data)
        color = self.addr_to_color_map[addr]
        self.engine.update_velocity(color, vel)

  def close_conns(self):
    self.send_data(CLOSE)

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
  server = Server(constants.SERVER_PORT)
  server.listen_for_conns(constants.N_PLAYERS)
  print("SERVER: Game started!")
  server.start_game()

  server.play()
