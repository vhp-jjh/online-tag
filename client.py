import socket
import pickle
import constants
import sys
from utils import printd

START = "start"

class Client:
  def __init__(self, engine, server_host, server_port):
    self.engine = engine
    self.s = socket.socket(constants.S_FAMILY, constants.S_TYPE)
    self.s.settimeout(constants.S_START_TIMEOUT)
    self.server_host = server_host # init these before calling wait_to_start
    self.server_port = server_port
    game_start_data = self.wait_to_start()
    self.engine.set_game_start_data(game_start_data)
    self.local_player_id = game_start_data.get_player_id()
    print("CLIENT: Game started!")
    printd("My id is: {0}".format(self.local_player_id))
    self.n_dropped = 0

  def send_server(self, msg):
    self.s.sendto(pickle.dumps(msg), (self.server_host, self.server_port))

  def wait_to_start(self):
    reply = ""
    self.send_server(START)
    while reply == "" or reply == None:
      reply, addr = self.s.recvfrom(1024)

    self.s.settimeout(constants.S_TIMEOUT)
    game_start_data = pickle.loads(reply)
    return game_start_data

  def update_player(self, player_update):
    self.send_server(player_update)
    self.engine.update_player(self.local_player_id, player_update)

  def update_engine(self):
    """Whenever the client wants to update the state of the game, it should call
    this method. This will return the appropriate engine, which will either have
    been updated because it received something from the server, or
    because it predicted something while waiting for the server to reply."""
    try:
      data, addr = self.s.recvfrom(1024)
      update_received = pickle.loads(data)
      if isinstance(update_received, str):
        print(update_received)
        sys.exit()
      self.engine.update(update_received)
    except socket.timeout:
      printd("CLIENT: nothing received. # dropped = {0}".format(self.n_dropped))
      self.n_dropped += 1
      self.engine.update_default()

    return self.engine

  def get_game_start_data(self):
    return self.engine.get_game_start_data()

  def close_conn(self):
    self.s.close()
