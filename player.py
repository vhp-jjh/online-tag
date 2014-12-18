class Player:
  def __init__(self, _pos, _color, _it, _health):
    self.pos = _pos #tuple of ints. x, y position in meters
    self.color = _color       #has type pygame.Color. also serves as id
    self.it = _it             #boolean. is this player it?
    self.vel = tuple(0 for i in range(len(_pos)))
    self.init_health = _health
    self.health = _health

  def set_vel(self, vel):
    self.vel = vel

  def get_pos(self):
    return self.pos

  def predict_pos(self, vel):
    return tuple(p + v for p, v in zip(self.pos, vel))

  def update_pos(self):
    self.pos = tuple(p + v for p, v in zip(self.pos, self.vel))

  def get_color(self):
    return self.color

  def is_it(self):
    return self.it

  def get_health(self):
    return self.health

  def reset_health(self):
    self.health = self.init_health
    
  def decrement_health(self):
    self.health -= 1
