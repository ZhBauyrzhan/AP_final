from argparse import Action
import pygame
from agent import Agent
from game import Game
import numpy as np
import settings
import random
import matplotlib.pyplot as plt

if __name__ == '__main__':
    agent = Agent(11, 3)
    scores = []
    rewards = []
    env = Game()

    for i in range(50):
        done = False
        while env.run:
            state, reward, _done, _score = env.get_state()
            state = np.reshape(state, (1,11))  
            action = agent.act(state)
            next_state, reward, _done, _score = env.move(action)
            if env.check() == 0:
                done = True
            reward = env.reward if not done else  reward-10
            next_state = np.reshape(next_state, [1, 11])
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            print(f"second {state=}")
            if len(agent.memory) > settings.BATCH_SIZE:
                agent.replay(settings.BATCH_SIZE)
                agent.memory.pop()
            env.draw()
        
        print(f"episode: {i}, score: {env.score}, epsilone: {agent.epsilon}, reward: {reward}")
        if agent.epsilon*agent.epsilon_decay >= agent.epsilon_min and random.randint(0,100) % 2 == 0:
            agent.epsilon*=agent.epsilon_decay
        rewards.append(reward)
        scores.append(env.score)
        print(rewards)
        env.restart()
    plt.plot(np.arange(1, i+2), scores)
    plt.show()
    