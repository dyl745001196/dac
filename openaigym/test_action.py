import gym
env = gym.make('CartPole-v0')

env.reset()

dataset = []
actions = []
for i in range(1000):
    env.render()
    action = env.action_space.sample()
    print('action', action)
    actions.append(action)
    obs, rew, done, info = env.step(action)

    dataset.append(obs)

import numpy as np

dataset = np.asarray(dataset)
actions = np.asarray(actions)

np.savetxt('dataset.txt', dataset)


import scipy.io as sio

data = {'data': dataset, 'action':actions}


sio.savemat('data_openai_cart_pole', data)


