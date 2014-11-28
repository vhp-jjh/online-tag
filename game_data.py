#pretty much just a struct for passing data between games and engine
class GameData:
  def __init__(self, _width, _height, _radius, _players):
    self.width = _width #in meters
    self.height = _height
    self.radius = _radius
    self.players = _players
    self.player_id = -1

  def get_width(self):
    return self.width

  def get_height(self):
    return self.height

  def get_radius(self):
    return self.radius

  def get_players(self):
    return self.players

  def get_player_id(self):
    return self.player_id

  def set_player_id(self, player_id):
    self.player_id = player_id