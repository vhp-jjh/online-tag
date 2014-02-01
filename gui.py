import pygame

class Gui:
  def __init__(self, _width, _height, _ppm):
    pygame.init()
    self.width = _width   #width of the screen in meters
    self.height = _height #height of the screen in meters
    self.ppm = _ppm       #pixels per meter (float)
    self.screen = pygame.display.set_mode((int(_width * _ppm),
      int(_height * _ppm)))

  def draw_player(self, pos_m, color, radius, it):
    #pos_m and radius measured in meters
    #convert from meters to pixels
    pos_pixels = (pos_m[0] * self.ppm, pos_m[1] * self.ppm)
    #draw the player as a circle
    pygame.draw.circle(self.screen, color, pos_pixels, radius * self.ppm)
    if it:
      #draw black border around the it player
      pygame.draw.circle(self.screen, pygame.Color("white"), pos_pixels,
                         radius * self.ppm, 1 * self.ppm)
