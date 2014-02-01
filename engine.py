class Engine:
  def __init__(self, _width, _height):
    self.width = _width   #in meters
    self.height = _height #in meters
    self.players = []
    self.colors = ["red", "blue", "green", "yellow"]

  def add_player(self):
    #add player and return it's color
    #because color serves as id
    n_players = len(self.players)
    if n_players == 0: #this is first player
      position = (5, 5)
    elif n_players == 1:
      position = (self.width - 5, self.height - 5)
    elif n_players == 2:
      position = (0, self.height - 5)
    elif n_players == 3:
      position = (self.width - 5, 0)
    else:
      print("too many players")
      quit()
    #create new player
    col = self.colors[n_players]
    player = Player(position, col, n_players == 0)
    self.players.append(player)
    return col

  #updates the velocity of the player with the matching color
  def update_velocity(color, vel):
    found = False
    for p in self.players:
      if p.color == color:
        found = True
        p.position[0] += vel[0]
        p.position[1] += vel[1]
    if found == False:
      print("color not found in player list")
      quit()

  #return the game data so the clients can draw it
  def get_game_data(self):
    return self.players
