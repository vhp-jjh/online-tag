import socket
import pickle
import time
import constants
from utils import printd
from engine import Engine

CLOSE = "close"

class Server:
  def __init__(self, port):
    self.engine = Engine()
    # TODO: Maybe move these to this file
    self.s = socket.socket(constants.S_FAMILY, constants.S_TYPE)
    self.port = port
    self.s.bind(("", self.port)) # "" = all available interfaces
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
    for addr in self.addresses:
      game_data = self.engine.get_game_data()
      game_data.set_player_id(self.addr_to_color_map[addr])
      self.s.sendto(pickle.dumps(game_data), addr)
    self.s.settimeout(constants.S_TIMEOUT)

  def send_update_to_clients(self):
    printd("SERVER: start send_update_to_clients")
    update = self.engine.get_game_update()
    self.send_data(update)
    printd("SERVER: end send_update_to_clients")

  def get_updates_from_clients(self):
    printd("SERVER: start get_updates_from_clients")
    waiting_for = list(self.addresses) # to get a copy not pointer
    printd("SERVER: address = {0}".format(self.addresses))
    # for i in range(len(self.addresses)): #TODO: maybe make this smarter
    data = ""
    while len(waiting_for) > 0:
      try:
        data, addr_recv = self.s.recvfrom(1024)
        printd("SERVER: data received from {0}. data = {1}".format(addr_recv,data))
      except socket.timeout:
        printd("SERVER: no data received")
      if len(data) > 0 and addr_recv in waiting_for:
        vel = pickle.loads(data)
        color = self.addr_to_color_map[addr_recv]
        self.engine.update_velocity(color, vel)
        waiting_for.remove(addr_recv)

    self.engine.update_positions()
    printd("SERVER: end get_updates_from_clients")

  def close_conns(self):
    self.send_data(CLOSE)

  def play(self):
    while True:
      # I don't think server should delay
      #start = time.time()
      self.send_update_to_clients()
      self.get_updates_from_clients()
      
      #delay_left = constants.LOOP_TIME - (time.time() - start)
      #if delay_left > 0:
      #  time.sleep(delay_left)

if __name__ == "__main__":
  server = Server(constants.SERVER_PORT)
  server.listen_for_conns(constants.N_PLAYERS)
  print("SERVER: Game started!")
  server.start_game()

  server.play()
