import numpy as np
import scipy.io as sio

data = sio.loadmat('data_openai_cart_pole.mat')
data = data['data']
print(data.shape)
