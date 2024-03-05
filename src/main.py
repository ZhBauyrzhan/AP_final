import pygame
from agent import Agent
from game import Game

if __name__ == '__main__':
    for i in range(3):
        env = Game()
        while env.run:
            pygame.time.delay(100)
            env.move()
            env.check()
            env.draw()