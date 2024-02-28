import pygame
from snake import *
from apple import Apple
import settings

pygame.init()
bounds = settings.WINDOW_SIZE
window = pygame.display.set_mode(bounds)
pygame.display.set_caption("Snake")

block_size = settings.BLOCK_SIZE
apple = Apple(block_size,bounds)
snake = Snake(block_size, bounds)

run = True
while run:
  pygame.time.delay(100)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  keys = pygame.key.get_pressed()
  
  
  if keys[pygame.K_LEFT]:
    snake.steer(Direction.LEFT)
  elif keys[pygame.K_RIGHT]:
    snake.steer(Direction.RIGHT)
  elif keys[pygame.K_UP]:
    snake.steer(Direction.UP)
  elif keys[pygame.K_DOWN]:
    snake.steer(Direction.DOWN)
  
  snake.move()
  if not snake.check_bounds() or not snake.check_tail_collision():
    apple.respawn()
    snake.respawn()
    continue
  if snake.try_eat_apple(apple):
    apple.respawn()
  # print(snake.body)

  window.fill((0,0,0))
  apple.draw(pygame, window)
  snake.draw(pygame, window)
  pygame.display.update()