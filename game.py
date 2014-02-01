import pygame
import time
from gui import Gui
from player import Player
from game_data import GameData
from client import Client

class Game:
  def __init__(self, _players):
    self.players = _players #list of players in the game
  def get_input(self):
    x = 0
    y = 0
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        return (0, 0, False)
      elif event.type == pygame.KEYDOWN:
        #respond to arrow keys and wasd
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
          x -= 1
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
          y -= 1
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
          x += 1
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
          y += 1
    return (x, y, True)

def main():
  host = "10.32.153.218"
  port = 12123
  client = Client(host, port)

  gd = client.get_game_data()
  field = Gui(gd.width, gd.height, 1.0)
  players = client.get_players()
  game = Game(players)

  while True:
    start_time = time.time()

    #get input
    inp = game.get_input()
    velocity = (inp[0], inp[1])
    if (not inp[2]):
      break

    #talk to server
    client.update_velocity(velocity)    #send my velocity to the server
    game.players = client.get_players() #update the player list

    #draw
    for p in game.players:
      field.draw_player(p.position, p.color, size // 100, p.it)
    pygame.display.flip()

    sleep_time = LOOP_TIME - (time.time() - start_time)
    if sleep_time > 0:
      time.sleep(sleep_time)

if __name__ == "__main__":
    main()
