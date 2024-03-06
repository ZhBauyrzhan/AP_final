import pygame
from snake import *
from apple import Apple
import settings
import numpy as np

class Game():
  def __init__(self):
    pygame.init()
    self.bounds = settings.WINDOW_SIZE
    self.window = pygame.display.set_mode(self.bounds)    
    pygame.display.set_caption("Snake")
    self.restart()
  def restart(self):
    self.run = True
    self.block_size = settings.BLOCK_SIZE
    self.apple = Apple(self.block_size,self.bounds)
    self.snake = Snake(self.block_size, self.bounds)
    self.frame = 0
    self.reward = 0
    self.score = 0
    self.done = False
    self.lose_frames = 0
    self.distance = self.calculate_distance()
  
  def calculate_distance(self):
    head = self.snake.body[0]
    apple = self.apple
    return ( abs(head[0] - apple.x) + abs(head[1] - apple.y) )

  def _get_map_state(self):
    head = self.snake.body[0]
    
    moves = self.snake.moves
    blocks = dict()
    blocks['left'] = [head[0] - moves[Direction.LEFT][0], head[1] - moves[Direction.LEFT][1]]
    blocks['right'] = [head[0] - moves[Direction.RIGHT][0], head[1] - moves[Direction.RIGHT][1]]
    blocks['up'] = [head[0] - moves[Direction.UP][0], head[1] - moves[Direction.UP][1]]
    blocks['down'] = [head[0] - moves[Direction.DOWN][0], head[1] - moves[Direction.DOWN][1]]
    
    is_direction_left = self.snake.direction == Direction.LEFT
    is_direction_right = self.snake.direction == Direction.RIGHT
    is_direction_up = self.snake.direction == Direction.UP
    is_direction_down = self.snake.direction == Direction.DOWN
    
    state = [
            (is_direction_left and self.snake.check_for_danger(blocks['left'])) or
            (is_direction_right and self.snake.check_for_danger(blocks['right'])) or
            (is_direction_up and self.snake.check_for_danger(blocks['up'])) or
            (is_direction_down and self.snake.check_for_danger(blocks['down'])),

            (is_direction_left and self.snake.check_for_danger(blocks['up'])) or
            (is_direction_right and self.snake.check_for_danger(blocks['down'])) or
            (is_direction_up and self.snake.check_for_danger(blocks['right'])) or
            (is_direction_down and self.snake.check_for_danger(blocks['left'])),

            (is_direction_left and self.snake.check_for_danger(blocks['down'])) or
            (is_direction_right and self.snake.check_for_danger(blocks['up'])) or
            (is_direction_up and self.snake.check_for_danger(blocks['left'])) or
            (is_direction_down and self.snake.check_for_danger(blocks['right'])),

            is_direction_left,
            is_direction_right,
            is_direction_up,
            is_direction_down,

            self.apple.x < head[0],
            self.apple.x > head[0], 
            self.apple.y < head[1],
            self.apple.y > head[1] 
      ]
    return np.array(state, dtype=int)

   
  def move(self, action):
    pygame.time.delay(10)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.run = False

    clock_wise_direction = [Direction.RIGHT,
                                Direction.DOWN, Direction.LEFT, Direction.UP]
    idx = clock_wise_direction.index(self.snake.direction)

    if action == 0:
      new_direction = clock_wise_direction[idx]
    elif action == 1:
      new_idx = (idx + 1) % 4
      new_direction = clock_wise_direction[new_idx]
    else:
      new_idx = (idx - 1) % 4
      new_direction = clock_wise_direction[new_idx]
     
    self.snake.steer(new_direction)
    self.snake.move()
    
    new_distance = self.calculate_distance()
    if new_distance < self.distance:
      self.reward += 1
    elif new_distance > self.distance:
      self.reward -= 5
    self.distance = new_distance
    
    self.frame += 1
    self.lose_frames += 1
    self.reward -= 1
    
    return self.get_state()
    
  def check(self):
    print('checked', self.snake.body[0])
    if not self.snake.check_bounds() or not self.snake.check_tail_collision():
      print('was', self.snake.body[0])
      # self.apple.respawn()
      # self.snake.respawn()
      self.run = 0
      self.done = True
      print(self.reward)
      self.reward -= 100
      print(self.reward)
      return 0
    if self.snake.try_eat_apple(self.apple):
      self.apple.respawn()
      self.reward += 1000
      self.score += 1
      self.lose_frames = 0
      return 1
    return 2
  def draw(self):
    self.window.fill((0,0,0))
    self.apple.draw(pygame, self.window)
    self.snake.draw(pygame, self.window)
    pygame.display.update()

  def get_state(self):
    return [self._get_map_state(), self.reward, self.done, self.score]