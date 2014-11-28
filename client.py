import socket
import pickle
import constants
from random import randrange
from engine import Engine
from utils import printd

START = "start"

class Client:
  def __init__(self, server_host, server_port):
    self.engine = Engine()
    self.s = socket.socket(constants.S_FAMILY, constants.S_TYPE)
    self.s.settimeout(constants.S_START_TIMEOUT)
    self.server_host = server_host # init these before calling wait_to_start
    self.server_port = server_port
    received_game_data = self.wait_to_start()
    self.engine.set_game_data(received_game_data)
    self.local_player_id = received_game_data.get_player_id()
    print("CLIENT: Game started!")
    printd("My id is: {0}".format(self.local_player_id))

  def send_server(self, msg):
    self.s.sendto(pickle.dumps(msg), (self.server_host, self.server_port))

  def wait_to_start(self):
    reply = ""
    self.send_server(START)
    while reply == "" or reply == None:
      printd("CLIENT: Waiting for game data")
      reply, addr = self.s.recvfrom(1024)

    self.s.settimeout(constants.S_TIMEOUT)
    game_data = pickle.loads(reply)
    return game_data

  def update_velocity(self, vel):
    self.send_server(vel)
    self.engine.update_velocity(self.local_player_id, vel)

  def update_engine(self):
    """Whenever the client wants to update the state of the game, it should call
    this method. This will return the appropriate engine, which will either have
    been updated because it received something from the server, or
    because it predicted something while waiting for the server to reply."""
    printd("CLIENT: waiting for data")
    try:
      data, addr = self.s.recvfrom(1024)
      update_received = pickle.loads(data)
      self.engine.update(update_received)
      printd("CLIENT: received update from server")
    except socket.timeout:
      printd("CLIENT: nothing received")
      self.engine.update_default()

    return self.engine

  def get_game_data(self):
    return self.engine.get_game_data()

  def close_conn(self):
    self.s.close()

# To test
if __name__ == "__main__":
  host = 'localhost' # Vitchyr's Gateway
  port = 12121
  client = Client(host, port)

  while True:
    vel = randrange(10), randrange(10)
    client.update_velocity(vel)
    print("Vel sent", vel)

    players = client.get_players()
    print(players)
