from argparse import Action
import pygame
from agent import Agent
from game import Game
import numpy as np
import settings
import random
import matplotlib.pyplot as plt
from IPython import display


def plot(scores):
    plt.ion()

    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.show(block=False)
    plt.pause(.1)

if __name__ == '__main__':
    agent = Agent(11, 3)
    scores = []
    rewards = []
    env = Game()
    
    state = np.reshape(env.get_state()[0], (1,11))     

    for i in range(500):
        reward = 0
        while env.run:
            pygame.time.delay(10)
            _, cur_reward, done, _score = env.get_state()
            action = agent.act(state)
            next_state, new_cur_reward, done, _score = env.move(action)
            env.check()
            print(state, action)
            next_state = np.reshape(next_state, [1, 11])
            agent.remember(state, action, reward, next_state, done)
            if not env.run:
                reward = env.reward
                break
            state = next_state
            if agent.epsilon > agent.epsilon_min:
                agent.epsilon = agent.epsilon * agent.epsilon_decay
            else:
                agent.epsilon = agent.epsilon_min
            if len(agent.memory) > 10*settings.BATCH_SIZE and random.randint(0,100)%2==0:
                agent.replay(settings.BATCH_SIZE)
                agent.epsilon*=agent.epsilon_decay
            env.draw()
        
        print(f"episode: {i}, score: {env.score}, epsilone: {agent.epsilon}, reward: {reward}")
        rewards.append(reward)
        if reward == 100 or reward == 0:
            break
        scores.append(env.score)
        print(rewards)
        env.restart()
    plot(scores=scores)