import gym
env = gym.make('CartPole-v0')
episodes = []
for i_episode in range(200):
    obs = env.reset()
    obs_data = [] 
    for t in range(100):
        env.render()
        print(obs)
        action = env.action_space.sample()
        obs, rew, done, info = env.step(action)
        temp = []
        for item in obs:
            temp.append(item)
        temp.append(action)
        obs_data.append(temp)

        if done:
            print("episode finished after {} timesteps".format(t+1))
            break
    episodes.append(obs_data)

import numpy as np
episodes = np.asarray(episodes)
import scipy.io as sio
sio.savemat('episodes', {'episodes':episodes})
