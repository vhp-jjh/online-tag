import pygame
import time
import constants
from gui import Gui
from player import Player
from game_data import GameData
from client import Client

class Game:
  def __init__(self, _players):
    self.players = _players #list of players in the game

  # returns a boolean tuple of 4 directions
  def get_input(self, dirs):
    up, down, left, right = dirs
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        quit()
      elif event.type == pygame.KEYDOWN:
        #respond to arrow keys and wasd
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
          left += 1
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
          up += 1
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
          right += 1
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
          down += 1
      elif event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
          left -= 1
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
          up -= 1
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
          right -= 1
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
          down -= 1
    return (up, down, left, right)
  
  def dirs_to_vel(self, dirs):
    x = 0
    y = 0
    if dirs[0] > 0 and dirs[1] > 0:
      y = 0
    elif dirs[0] > 0:
      y = -constants.SPEED
    elif dirs[1] > 0:
      y = constants.SPEED

    if dirs[2] > 0 and dirs[3] > 0:
      x = 0
    elif dirs[2] > 0:
      x = -constants.SPEED
    elif dirs[3] > 0:
      x = constants.SPEED
    return (x, y)

def main():
  client = Client(constants.SERVER_ADDR, constants.SERVER_PORT)

  gd = client.get_game_data()
  field = Gui(gd.width, gd.height, 1.0)
  engine = client.update_engine()
  players = engine.get_players()
  print("CLIENT: players = {0}".format(players))
  game = Game(players) # TODO: figure out if we want to bother passing this

  # up, down, left, right
  dirs = (0, 0, 0, 0)
  while True:
    start_time = time.time()

    #get input
    dirs = game.get_input(dirs)
    velocity = game.dirs_to_vel(dirs)

    #talk to server
    client.update_velocity(velocity)    #send my velocity to the server
    engine = client.update_engine()
    game.players = engine.get_players()

    #draw
    field.fill_black()
    for p in game.players:
      field.draw_player(p.get_pos(), p.get_color(), gd.radius, p.is_it())
    pygame.display.flip()

    sleep_time = constants.LOOP_TIME - (time.time() - start_time)
    if sleep_time > 0:
      time.sleep(sleep_time)

if __name__ == "__main__":
    main()
