import socket
import pickle
import time
import constants
from utils import printd
from engine import Engine
import random

CLOSE = "close"

class Server:
  def __init__(self, engine, port):
    self.engine = engine
    self.s = socket.socket(constants.S_FAMILY, constants.S_TYPE)
    self.port = port
    self.s.bind(("", self.port)) # "" = all available interfaces
    self.addresses = [] # List of addresses
    self.addr_to_player_id_map = {} #for tag, id = color

  def wait_for_players(self, n_players):
    for n_joined in range(n_players):
      print("Waiting for %d players to connect..." % (n_players - n_joined))
      data = ""
      while data == "" or data == None:
        data, addr = self.s.recvfrom(1024)

      self.addresses.append(addr)
      self.addr_to_player_id_map[addr] = self.engine.add_player()
  
  def send_data(self, data):
    msg = pickle.dumps(data)
    for addr in self.addresses:
      # DROP_RATE is zero if DEBUG is set to false
      if random.random() >= constants.DROP_RATE:
        self.s.sendto(msg, addr)
      else:
        printd("SERVER: dropping packet")
  
  def start_game(self):
    print("SERVER: Game started!")
    for addr in self.addresses:
      game_data = self.engine.get_game_start_data()
      game_data.set_player_id(self.addr_to_player_id_map[addr])
      self.s.sendto(pickle.dumps(game_data), addr)
    self.s.settimeout(constants.S_TIMEOUT)

  def send_update_to_clients(self):
    update = self.engine.get_game_update()
    self.send_data(update)

  def get_updates_from_clients(self):
    waiting_for = list(self.addresses) # to get a copy not pointer
    # for i in range(len(self.addresses)): #TODO: maybe make this smarter
    data = ""
    while len(waiting_for) > 0:
      try:
        data, addr_recv = self.s.recvfrom(1024)
      except socket.timeout:
        printd("SERVER: no data received")
      if len(data) > 0 and addr_recv in waiting_for:
        player_update = pickle.loads(data)
        player_id = self.addr_to_player_id_map[addr_recv]
        self.engine.update_player(player_id, player_update)
        waiting_for.remove(addr_recv)

    self.engine.update_positions()

  def close_conns(self):
    self.send_data(CLOSE)

  def play(self):
    while True:
      self.send_update_to_clients()
      self.get_updates_from_clients()

if __name__ == "__main__":
  random.seed(time.time())
  server = Server(Engine(), constants.SERVER_PORT)
  server.wait_for_players(constants.N_PLAYERS)
  server.start_game()
  server.play()
