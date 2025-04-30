import pygame
from sprites import *
from settings import *
from groups import AllSprites
from support import *
from timer import Timer

class Game:
  def __init__(self):
    pygame.init()
    self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,
                                                    WINDOW_HEIGHT))
    pygame.display.set_caption("Platformer")
    self.clock = pygame.time.Clock()
    self.running = True

    self.all_sprites = AllSprites()
    self.collision_sprites = pygame.sprite.Group()


  #load game
    self.load_assests()
    self.setup()

    self.bee_timer = Timer(200, func = self.create_bee)
    self.bee_timer.activate()

  def create_bee(self):
    Bee(self.bee_frames, (500, 600), self.all_sprites)

  def create_bullet(self):
    Bullet(self.bullet_surf, pos, direction, (self.all_sprites,
                                              self.bullet_sprites))

  def load_assests(self):
    self.player_frames = import_folder('images', 'player')
    self.bullet_surf = import_image('images', 'gun', 'bullet')
    self.fire_surf = import_image('images', 'gun', 'fire')
    self.bee_frames = import_folder('images', 'enemies', 'bee')
    self.worm_frames = import_folder('images', 'enemies', 'worm')
    print(self.bullet_surf)


  def setup(self):
    tmx_map = load_pygame(join('data', 'maps', 'world.tmx'))

    for x,y, image in tmx_map.get_layer_by_name('Main').tiles():
        Sprite((x * TILE_SIZE, y * TILE_SIZE), image,
               (self.all_sprites, self.collision_sprites))

    for x, y, image in tmx_map.get_layer_by_name('Decoration').tiles():
      Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

    for obj in tmx_map.get_layer_by_name('Entities'):
      if obj.name == 'Player':
        self.player = Player((obj.x, obj.y), self.all_sprites,
                        self.collision_sprites, self.player_frames)

    Bee(self.bee_frames, (500,600), self.all_sprites)
    Worm(self.worm_frames, (700, 600), self.all_sprites)

  def run(self):
    while self.running:
      dt = self.clock.tick(FRAMERATE) / 1000

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.running = False

      self.bee_timer.update()
      self.all_sprites.update(dt)

      self.display_surface.fill(BG_COLOR)
      self.all_sprites.draw(self.player.rect.center)
      pygame.display.update()


if __name__ == '__main__':
  game = Game()
  game.run()