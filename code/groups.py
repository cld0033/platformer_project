from settings import *

class AllSprites(pygame.sprite.Group):
  def __init__(self):
    super().__init__()
    self.display_surface = pygame.display.get_surface()
    self.offset = pygame.Vector2()

  # def draw(self, target_pos):
  #   self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)
  #   self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2)
  #
  #   for sprite in self:
  #     self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)

  def draw(self, target_pos):
    # Ensure target_pos is a valid (x, y) tuple
    if isinstance(target_pos, tuple) or isinstance(target_pos,
                                                   pygame.math.Vector2):
      self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)
      self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2)
    else:
      raise TypeError(
        "target_pos must be a tuple or pygame.Vector2 with (x, y) coordinates.")

    for sprite in self:
      self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)