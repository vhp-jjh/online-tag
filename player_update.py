class PlayerUpdate:
  """A wrapper for data that the client sends to the server about its player.
  This will generally have less data than the data that the server needs to sends
  back."""
  def __init__(self, vel):
    self.vel = vel

  def get_vel(self):
    return self.vel