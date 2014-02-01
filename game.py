import pygame
from gui import Gui
from player import Player

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
  size = 500
  field = Gui(size, size, 1)
  #TODO get_game_data
  #use fake data until client-server is done
  player1 = Player((100, 100), pygame.Color("blue"), True)
  player2 = Player((size - 100, size - 100), pygame.Color("red"), False)
  game = Game([player1, player2])
  running = True
  while running:
    #get input
    inp = game.get_input()
    velocity = (inp[0], inp[1])
    running = inp[2]
    #TODO send_velocity(velocity)
    #TODO gd = get_game_data()
    for p in game.players:
      field.draw_player(p.position, p.color, size // 100, p.it)
    pygame.display.flip()

if __name__ == "__main__":
    main()
