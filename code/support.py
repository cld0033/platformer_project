from settings import *

def import_image(*path, format='png', alpha=True):
  full_path = join(*path) + f'.{format}'
  surf = pygame.image.load(full_path).convert_alpha() if alpha else (
    pygame.image.load(full_path).convert())
  return surf