import socket
import pickle
import constants
from random import randrange

START = "start"

class Client:
  def __init__(self, server_host, server_port):
    self.s = socket.socket(constants.S_FAMILY, constants.S_TYPE)
    self.s.settimeout(constants.TIMEOUT)
    self.server_host = server_host # init these before calling wait_to_start
    self.server_port = server_port
    self.game_data = self.wait_to_start()
    print("CLEINT: Game started!")
    print("Game data = {0}".format(self.game_data))

  def send_server(self, msg):
    self.s.sendto(pickle.dumps(msg), (self.server_host, self.server_port))

  def wait_to_start(self):
    reply = ""
    while reply == "" or reply == None:
      print("CLIENT: Waiting for game data")
      self.send_server(START)
      reply, addr = self.s.recvfrom(1024)

    game_data = pickle.loads(reply)
    return game_data

  def update_velocity(self, vel):
    self.send_server(vel)

  def get_players(self, default):
    print("CLIENT: waiting for data")
    try:
      data, addr = self.s.recvfrom(1024)
      players = pickle.loads(data)
    except socket.timeout:
      print("CLIENT: nothing received")
      players = default
    print("CLIENT: players = {0}".format(players))
    return players

  def get_game_data(self):
    return self.game_data

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
