import scipy.io as sio
import numpy as np
import keras
import matplotlib.pyplot as plt
from keras.layers import Dense, Activation
from keras.models import Sequential

data = sio.loadmat('si_dac_data.mat')
# load the data of dac algorithm input and goal
# the data is prepared of deep learning method
dac_input = data['dac_input_whole_set']
dac_goal = data['dac_goal_whole_set']
dac_input = dac_input.astype('double')
dac_goal = dac_goal.astype('double')


goal_max = np.max(dac_goal)
goal_min = np.min(dac_goal)

# dac_goal = 2*(dac_goal - goal_min)/(goal_max - goal_min) -1  

model = Sequential()
model.add(Dense(20, input_dim=1))	
model.add(Activation('sigmoid'))
model.add(Dense(20))
model.add(Activation('relu'))
model.add(Dense(1))

model.compile(loss='mse', optimizer='rmsprop')
fig = plt.figure()
plt.pause(0.1)
import pdb
pdb.set_trace()
for i in range(20):
	model.fit(dac_input, dac_goal, epochs=1, batch_size = 64, validation_split = 0.4)


	pred_out = model.predict(dac_input)
	plt.clf()
	plt.plot(dac_goal, 'b')
	plt.plot(pred_out, 'r')
	plt.pause(0.1)
	
plt.show()



