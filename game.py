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

  #takes input, returns velocity and a flag that tells whether velocity should be
  #changed
  def get_input(self, x, y):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        quit()
      elif event.type == pygame.KEYDOWN:
        #respond to arrow keys and wasd
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
          new_speed = x - constants.SPEED
          if new_speed < -constants.SPEED:
            x = -constants.SPEED
          else:
            x = new_speed
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
          new_speed = y - constants.SPEED
          if new_speed < -constants.SPEED:
            y = -constants.SPEED
          else:
            y = new_speed
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
          new_speed = x + constants.SPEED
          if new_speed > constants.SPEED:
            x = constants.SPEED
          else:
            x = new_speed
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
          new_speed = y + constants.SPEED
          if new_speed > constants.SPEED:
            y = constants.SPEED
          else:
            y = new_speed
      elif event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
          x += constants.SPEED
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
          y += constants.SPEED
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
          x -= constants.SPEED
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
          y -= constants.SPEED
    return (x, y)

def main():
  client = Client(constants.HOST, constants.PORT)

  gd = client.get_game_data()
  field = Gui(gd.width, gd.height, 1.0)
  print("About to call client.get_playerS()")
  players = client.get_players()
  print("Done calling client.get_playerS()")
  game = Game(players)

  velocity = (0, 0)
  while True:
    start_time = time.time()

    #get input
    inp = game.get_input(velocity[0], velocity[1])
    velocity = (inp[0], inp[1])

    #talk to server
    client.update_velocity(velocity)    #send my velocity to the server
    game.players = client.get_players() #update the player list

    #draw
    field.fill_black()
    for p in game.players:
      field.draw_player(p.position, p.color, gd.radius, p.it)
    pygame.display.flip()

    sleep_time = constants.LOOP_TIME - (time.time() - start_time)
    if sleep_time > 0:
      time.sleep(sleep_time)

if __name__ == "__main__":
    main()
