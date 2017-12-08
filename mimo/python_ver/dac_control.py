import numpy as np
import matplotlib.pyplot as plt
import keras
from keras.layers import Dense, Activation
from keras.models import Sequential
import scipy.io as sio
import pdb
import math

model = Sequential()
model.add(Dense(10, input_dim=2))
model.add(Activation('relu'))
model.add(Dense(10))
model.add(Activation('relu'))
model.add(Dense(2))

model.compile(loss = 'mse', optimizer = 'rmsprop')
model.load_weights('weights.h5')

def offline_nn(in_value):
	global model
	return -model.predict(in_value)

class Dac_Controller:
# init the parameters in dac
	def __init__(self):
		self.dt = 0.01
		self.x_cur = np.array([[0, 0]])
		self.x_m_cur = np.array([[0, 0]])

		self.theta_hat = np.array([[1, 0],
							  [0, 1]])
		self.theta = self.theta_hat

		self.k_x_hat = np.array([[-5, 0],
							[0, -5]])
							
		self.k_r_hat = np.array([[5, 0],
							[0, 5]])
							
		self.gamma_x = np.array([[5, 0],
							[0, 0.1]])
							
		self.gamma_r = np.array([[0.1, 0],
							[0, 0.2]])

		self.P = np.array([[1, 0],
					  [0, 1]])
					  
		self.x_set = self.x_cur
		self.x_m_set = self.x_m_cur
		
	def sim_sys(self, y_cur, dt, u_cur):
		y_next = np.array([[y_cur[0][0] + dt*(-y_cur[0][0] - y_cur[0][1] - np.sin(y_cur[0][0])                 + u_cur[0]),
		                    y_cur[0][1] + dt*(-y_cur[0][0] + y_cur[0][1] - np.sin(y_cur[0][0]) + np.sin(y_cur[0][1]) + u_cur[1])]])
		#pdb.set_trace()
		return y_next
	
	def sim_ref(self, y_cur, dt, u_cur):
		T_const = 20
		
		temp = y_cur[0][0] + dt*T_const*(-y_cur[0][0] + u_cur[0])
		#pdb.set_trace()
		y_next = np.array([[y_cur[0][0] + dt*T_const*(-y_cur[0][0] + u_cur[0][0]),
		                    y_cur[0][1] + dt*T_const*(-y_cur[0][1] + u_cur[0][1])]])
		return y_next
	
	def sim(self, time_span):
		for i in range(time_span):
			r = np.array([[1, 1]])
			DL_x_r = np.dot(offline_nn(self.x_cur), self.theta_hat).T + np.dot(self.k_x_hat, self.x_cur.T) + np.dot(self.k_r_hat, r.T)
			#pdb.set_trace()
			x_next = self.sim_sys(self.x_cur, self.dt, DL_x_r)[0].T
			
			x_m_next = self.sim_ref(self.x_m_cur, self.dt, r)[0].T			
			self.x_cur = x_next.reshape((1, 2))
			self.x_m_cur = x_m_next.reshape((1, 2))
			#pdb.set_trace()
			self.x_set = np.vstack((self.x_set, self.x_cur))
			self.x_m_set = np.vstack((self.x_m_set, self.x_m_cur))
			
			e = self.x_cur - self.x_m_cur
			
			self.theta_hat = self.theta_hat -self.dt*np.dot(np.dot(np.dot(self.gamma_x, self.x_cur.T), e), self.P)
			self.k_x_hat = self.k_x_hat -    self.dt*np.dot(np.dot(np.dot(self.gamma_r, r.T), e), self.P)
			self.k_r_hat = self.k_r_hat -    self.dt*np.dot(np.dot(offline_nn(self.x_cur).T, e), self.P)
			#pdb.set_trace()
	def visualize(self):
		plt.plot(self.x_set[:, 0], 'r')
		plt.plot(self.x_set[:, 1], 'y')
		plt.show()
dac = Dac_Controller()
dac.sim(4000)
dac.visualize()
	