from settings import *
from sprites import *
from groups import AllSprites
from support import *
from timer import Timer
from random import randint


class Game:
  def __init__(self):
    pygame.init()
    self.display_surface = pygame.display.set_mode(
      (WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Platformer')
    self.clock = pygame.time.Clock()
    self.running = True

    # groups
    self.all_sprites = AllSprites()
    self.collision_sprites = pygame.sprite.Group()
    self.bullet_sprites = pygame.sprite.Group()
    self.enemy_sprites = pygame.sprite.Group()

    #difficulty
    self.difficulty_mode = 'easy'  #or hard
    self.difficulty_mode = 'easy'  # Default difficulty is easy
    self.enemy_speed_increase = 0.75  # Default speed for easy mode
    self.spawn_rate_decrease = 1.1  # Enemies spawn slower in easy mode
    self.enemy_damage_multiplier = 0.5  # Enemies deal less damage in easy mode

    # load game
    self.load_assets()
    self.setup()

    # timers
    self.bee_timer = Timer(100, func=self.create_bee, autostart=True,
                           repeat=True)

  def menu_screen(self):
    # Simple menu screen to choose difficulty
    font = pygame.font.SysFont("Arial", 40)
    easy_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 50,
                              200, 50)
    hard_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 50,
                              200, 50)

    while True:
      self.display_surface.fill((0, 0, 0))

      # Draw buttons
      pygame.draw.rect(self.display_surface, (0, 255, 0), easy_button)
      pygame.draw.rect(self.display_surface, (255, 0, 0), hard_button)

      # Display text
      easy_text = font.render("Easy Mode", True, (0, 0, 0))
      hard_text = font.render("Hard Mode", True, (0, 0, 0))

      # Calculate center position for text within the buttons
      easy_text_pos = (easy_button.centerx - easy_text.get_width() // 2,
                       easy_button.centery - easy_text.get_height() // 2)
      hard_text_pos = (hard_button.centerx - hard_text.get_width() // 2,
                       hard_button.centery - hard_text.get_height() // 2)

      # Draw the text at the correct position
      self.display_surface.blit(easy_text, easy_text_pos)
      self.display_surface.blit(hard_text, hard_text_pos)

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
          if easy_button.collidepoint(event.pos):
            self.difficulty_mode = "easy"
            return
          elif hard_button.collidepoint(event.pos):
            self.difficulty_mode = "hard"
            return

      pygame.display.update()

  def create_bee(self):
      Bee(frames=self.bee_frames,
          pos=(WINDOW_WIDTH + 50, randint(0, self.level_height)),
          groups=(self.all_sprites, self.enemy_sprites),
          speed=randint(300, 500),
          difficulty_multiplier=self.enemy_speed_increase)

  def create_bullet(self, pos, direction):
    x = pos[0] + direction * 34 if direction == 1 else pos[
                                                         0] + direction * 34 - self.bullet_surf.get_width()
    Bullet(self.bullet_surf, (x, pos[1]), direction,
           (self.all_sprites, self.bullet_sprites))
    Fire(self.fire_surf, pos, self.all_sprites, self.player)
    self.audio['shoot'].play()

  def load_assets(self):
    # graphics
    self.player_frames = import_folder('images', 'player')
    self.bullet_surf = import_image('images', 'gun', 'bullet')
    self.fire_surf = import_image('images', 'gun', 'fire')
    self.bee_frames = import_folder('images', 'enemies', 'bee')
    self.worm_frames = import_folder('images', 'enemies', 'worm')

    # sounds
    self.audio = audio_importer('audio')

  def setup(self):
    tmx_map = load_pygame(join('data', 'maps', 'world.tmx'))
    self.level_width = tmx_map.width * TILE_SIZE
    self.level_height = tmx_map.height * TILE_SIZE

    for x, y, image in tmx_map.get_layer_by_name('Main').tiles():
      Sprite((x * TILE_SIZE, y * TILE_SIZE), image,
             (self.all_sprites, self.collision_sprites))

    for x, y, image in tmx_map.get_layer_by_name('Decoration').tiles():
      Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

    for obj in tmx_map.get_layer_by_name('Entities'):
      if obj.name == 'Player':
        self.player = Player((obj.x, obj.y), self.all_sprites,
                             self.collision_sprites, self.player_frames,
                             self.create_bullet)
      if obj.name == 'Worm':
        Worm(self.worm_frames,
             pygame.FRect(obj.x, obj.y, obj.width, obj.height),
             (self.all_sprites, self.enemy_sprites))

    # self.audio['music'].play(loops = -1)

  def collision(self):
    # bullets -> enemies
    for bullet in self.bullet_sprites:
      sprite_collision = pygame.sprite.spritecollide(bullet, self.enemy_sprites,
                                                     False,
                                                     pygame.sprite.collide_mask)
      if sprite_collision:
        self.audio['impact'].play()
        bullet.kill()
        for sprite in sprite_collision:
          sprite.destroy()

    # enemies -> player
    if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
        self.running = False

  def adjust_difficulty(self):
      if self.difficulty_mode == "easy":
        self.enemy_speed_increase = 0.75  # Slower enemies#          self.spawn_rate_decrease = 1.1  # Enemies spawn slower
        self.enemy_damage_multiplier = 0.5  # Enemies deal less damage
      elif self.difficulty_mode == "hard":
        self.enemy_speed_increase = 1.5  # Faster enemies
        self.spawn_rate_decrease = 0.8  # Enemies spawn faster
        self.enemy_damage_multiplier = 1.5  # Enemies deal more damage

  def run(self):
    self.menu_screen()  # Show the menu to select difficulty
    while self.running:
      dt = self.clock.tick(FRAMERATE) / 1000

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.running = False

      # Update game elements
      self.bee_timer.update()
      self.all_sprites.update(dt)
      self.collision()

      # Draw everything with the player's position as the target position
      self.display_surface.fill(BG_COLOR)
      self.all_sprites.draw(
        self.player.rect.center)  # Corrected to pass player position
      pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
  game = Game()
  game.run()

