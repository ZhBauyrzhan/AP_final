from collections import deque
from keras import Sequential
from keras.layers import Dense
from keras.optimizers.legacy import Adam
import numpy as np
import random

class Agent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=200000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.85
        self.learning_rate = 0.01
        self.model = self._build_model()
        
    def _build_model(self):
        model =  Sequential()
        model.add(Dense(11, input_dim=11, activation='relu'))
        # model.add(Dense(64, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(3, activation='softmax'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        model.build()
        return model
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                Q_next=self.model.predict(next_state)[0]
                target = (reward + self.gamma *np.amax(Q_next))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            # print(state, action, self.epsilon, target, target_f)
            self.model.fit(state, target_f, epochs=1, verbose=0)