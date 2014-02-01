class Player:
  position #tuple of ints giving x, y position
  color    #has type pygame.Color. also serves as id
  it       #boolean. is this player it?

  #constructor
  def __init__(_position, _color, _it):
    position = _position
    colot = _color
    it = _it

