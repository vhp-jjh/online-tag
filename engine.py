from game_start_data import GameStartData
from game_update import GameUpdate
from player import Player
from constants import *
from pygame import Color
from math import sqrt
import random

class Engine:
  def __init__(self, _width = WIDTH, _height = HEIGHT, _radius = RADIUS):
    self.width = _width   #in meters
    self.height = _height #in meters
    self.radius = _radius
    self.players = []
    self.colors = [Color("red"), Color("blue"), Color("green"),
                   Color("yellow")]
    self.freeze_time = 0
    self.dead_players = []

  def add_player(self):
    """add player and return it's color, which serves as a player's id."""
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
    player = Player(position, col, n_players == 0, INIT_HEALTH)
    self.players.append(player)
    return col

  def update_player(self, player_id, player_update):
    vel = player_update.get_vel()
    """Updates the velocity of the player with the matching color."""
    if self.freeze_time > 0:
      self.freeze_time -= 1

    for p in self.players:
      if p.get_color() == player_id:
        if p.is_it():
          p.decrement_health()
          if p.get_health() == 0:
            # kill this player and make someone else it.
            # Although usually removing from a list while iterating
            # through it is a bad idea, it's okay because we're
            # about to return
            self.players.remove(p)
            if len(self.players) <= 1:
              return GAME_OVER_MESSAGE
            random.choice(self.players).it = True
        if self.player_can_move_to(p, vel):
          p.set_vel(vel)
        else:
          p.set_vel((0,0)) #TODO maybe make them bounce?
        return OKAY_MESSAGE

    #raise Exception("Color not found in player list")
    # server trying to update dead player. just ignore it.
    return OKAY_MESSAGE
  
  def update_positions(self):
    """Update the position of each player based on their velocities."""
    for p in self.players:
      p.update_pos()

  @staticmethod
  def distance_sqr(x1, y1, x2, y2):
    return (x1-x2)**2 + (y1-y2)**2

  def tag(self, p1, p2):
    if self.freeze_time == 0:
      tmp = p1.it
      p1.it = p2.it
      p2.it = tmp

      self.freeze_time = TAG_BACK_DELAY

  # Returns if the player can move in a certain velocity
  def player_can_move_to(self, player, vel):
    x, y = player.predict_pos(vel)
    if player.it and self.freeze_time > 0:
      return False
    radius = self.radius
    # handle wall collisions
    if x - radius < 0 or y - radius < 0 or x + radius > WIDTH \
      or y + radius > HEIGHT:
      return False
    # handle player-player collisions
    for p in self.players:
      if p != player:
        d = Engine.distance_sqr(x, y, p.get_pos()[0], p.get_pos()[1])
        if d <= 4*radius*radius:
          if p.it or player.it:
            self.tag(player, p)
          return False
    return True

  #return the game data so the clients can draw it
  def get_players(self):
    return self.players

  def get_game_update(self):
    """Get all the data needed to update the game since the game was created or
    since the last time an update was made. Note that this will return less
    information than get_game_data."""
    return GameUpdate(self.players)

  def update(self, game_update):
    self.players = game_update.get_players()

  def update_default(self):
    """Do an update if nothing is received from the server."""
    for p in self.players:
      p.update_pos()

  def get_game_start_data(self):
    """Get all the game data needed to recreate the entire game."""
    return GameStartData(self.width, self.height, self.radius, self.players)

  def set_game_start_data(self, game_start_data):
    self.width = game_start_data.get_width()
    self.height = game_start_data.get_height()
    self.radius = game_start_data.get_radius()
    self.players = game_start_data.get_players()
