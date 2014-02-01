#pretty much just a struct for passing data between games and engine
class GameData:
  def __init__(self, _width, _height, _radius):
    self.width = _width #in meters
    self.height = _height
    self.radius = _radius
