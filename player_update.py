class PlayerUpdate:
  """A wrapper for data that the client sends to the server about its player.
  This will generally have less data than the data that the server needs to sends
  back."""
  def __init__(self, player_dir):
    self.player_dir = player_dir

  def get_player_dir(self):
    return self.player_dir
