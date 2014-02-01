from game_data import GameData
from player import Player
from constants import *
from pygame import Color

#TODO collision detection
class Engine:
  def __init__(self, _width = WIDTH, _height = HEIGHT, _radius = RADIUS):
    self.width = _width   #in meters
    self.height = _height #in meters
    self.radius = _radius
    self.players = []
    self.colors = [Color("red"), Color("blue"), Color("green"),
                   Color("yellow")]

  #add player and return it's color
  #because color serves as id
  def add_player(self):
    #calculate position
    n_players = len(self.players)
    if n_players == 0: #this is first player
      position = (self.radius, self.radius)
    elif n_players == 1:
      position = (self.width - self.radius, self.height - self.radius)
    elif n_players == 2:
      position = (0, self.height - self.radius)
    elif n_players == 3:
      position = (self.width - self.radius, 0)
    else:
      print("too many players")
      quit()

    #create new player
    col = self.colors[n_players]
    player = Player(position, col, n_players == 0)
    self.players.append(player)
    return col

  #updates the velocity of the player with the matching color
  def update_velocity(self, color, vel):
    found = False
    for p in self.players:
      if p.color == color:
        found = True
        new_x = p.position[0] + vel[0]
        new_y = p.position[1] + vel[1]
        no_collision = self.can_move(p, new_x, new_y)
        p.position = tuple((new_x, new_y))
    if found == False:
      print("color not found in player list")
      quit()

  #def distance((x1, y1), (

  #check for collision
  def can_move(self, player, x, y):
    if x < 0 or y < 0 or x > WIDTH or y > HEIGHT:
      return True
    for p in self.players:
      if p == player:
        continue



  #return the game data so the clients can draw it
  def get_players(self):
    return self.players

  def get_game_data(self):
    return GameData(self.width, self.height, self.radius)
