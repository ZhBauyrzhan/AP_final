import pygame
from snake import *
from apple import Apple
import settings

class Game():
  def __init__(self):
    pygame.init()
    self.run = True
    pygame.time.delay(100)
    self.bounds = settings.WINDOW_SIZE
    self.window = pygame.display.set_mode(self.bounds)    
    pygame.display.set_caption("Snake")
    self.block_size = settings.BLOCK_SIZE
    self.apple = Apple(self.block_size,self.bounds)
    self.snake = Snake(self.block_size, self.bounds)

  def get_state(self):
    pass
  
  def move(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.run = False

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
      self.snake.steer(Direction.LEFT)
    elif keys[pygame.K_RIGHT]:
      self.snake.steer(Direction.RIGHT)
    elif keys[pygame.K_UP]:
      self.snake.steer(Direction.UP)
    elif keys[pygame.K_DOWN]:
      self.snake.steer(Direction.DOWN)
    self.snake.move()
  def check(self):
    if not self.snake.check_bounds() or not self.snake.check_tail_collision():
      self.apple.respawn()
      self.snake.respawn()
      self.run = 0
      # TODO write return 
    if self.snake.try_eat_apple(self.apple):
      self.apple.respawn()
  def draw(self):
    self.window.fill((0,0,0))
    self.apple.draw(pygame, self.window)
    self.snake.draw(pygame, self.window)
    pygame.display.update()
