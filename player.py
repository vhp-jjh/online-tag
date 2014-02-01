class Player:

  #constructor
  def __init__(self, _position, _color, _it):
    self.position = _position #tuple of ints giving x, y position in meters
    self.color = _color       #has type pygame.Color. also serves as id
    self.it = _it             #boolean. is this player it?

