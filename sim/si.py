import scipy.io as sio
import matplotlib.pyplot as plt
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation


model = Sequential()
model.add(Dense(10, input_dim = 2))
model.add(Activation('relu'))
model.add(Dense(10))
model.add(Activation('relu'))
model.add(Dense(2))
model.compile(loss = 'mse', optimizer = 'rmsprop')

data = sio.loadmat('mathbai.mat')

dac_goal = data['dac_goal']
dac_input = data['dac_input']


print(dac_input.shape)
#plt.plot(dac_goal)
#plt.show()


model.fit(dac_input, dac_goal, epochs = 100, validation_split = 0.5)

pred = model.predict(dac_input)
plt.subplot(1, 2, 1)
plt.plot(pred[:, 0], 'r')
plt.plot(dac_goal[:, 0], 'b')
plt.subplot(1, 2, 2)
plt.plot(pred[:, 1], 'r')
plt.plot(dac_goal[:, 1], 'b')
plt.show()

weights = model.get_weights()

weights_mat = {}

index = 0

for item in weights:
    weights_mat['weight' + str(index)] = item
    index += 1
sio.savemat('weights', weights_mat)

