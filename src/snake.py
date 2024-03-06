from enum import Enum

from sympy import prime_valuation
import settings

class Direction(Enum):
  UP = 0
  RIGHT = 1
  DOWN = 2
  LEFT = 3


class Snake:
  length = None
  direction = None
  body = None
  block_size = None
  head_color = settings.GREEN
  tail_color = settings.BLUE
  bounds = None
  prev_positions = None
  moves = None
  
  def __init__(self, block_size, bounds):
    self.block_size = block_size
    self.bounds = bounds
    self.prev_positions = []
    self.moves = {
      Direction.UP: [0, -block_size],
      Direction.DOWN: [0, block_size],
      Direction.RIGHT: [block_size, 0],
      Direction.LEFT: [-block_size, 0],
    }
    self.respawn()

  def respawn(self):
    self.length = 1
    self.body = [(20,20)]
    self.direction = Direction.RIGHT

  def draw(self, pygame, window):
    for segment in self.body:
      color = self.tail_color
      if segment == self.body[0]:
        color = self.head_color
      pygame.draw.rect(window, color, (segment[0],segment[1],self.block_size, self.block_size))

  def move(self):
    head = [self.body[0][0] + self.moves[self.direction][0], self.body[0][1]+ self.moves[self.direction][1]]
    self.prev_positions.append(self.body[-1])
    self.body = [head, *self.body[:-1]]
    # print(head, self.prev_positions, self.body)

  def check_for_danger(self, possition):
    return possition in self.body

  def steer(self, direction):
    if self.direction == Direction.DOWN and direction != Direction.UP:
      self.direction = direction
    elif self.direction == Direction.UP and direction != Direction.DOWN:
      self.direction = direction
    elif self.direction == Direction.LEFT and direction != Direction.RIGHT:
      self.direction = direction
    elif self.direction == Direction.RIGHT and direction != Direction.LEFT:
      self.direction = direction

  def try_eat_apple(self, apple):
    head = self.body[0]
    if head[0] == apple.x and head[1] == apple.y:
      self.length+=1
      self.body.append(self.prev_positions[-1])
      self.prev_positions.pop()
      return True
    return False

  def check_tail_collision(self):
    head = self.body[0]
    
    if len(self.body) == 0 or head not in self.body[1:]:
      return True
    return False

  def check_bounds(self):
    head = self.body[0]
    if head[0] >= self.bounds[0] or head[1] >= self.bounds[1] or head[0] < 0 or head[1] < 0:
      return False
    return True