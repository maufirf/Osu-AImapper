import numpy as np
from numpy import random as rd
import NN_C01_03_Ex_SingleNeuron as pma # pm = previous module
import NN_C02_01_MachineLearning as pmb

# initial parameters
a = 1
b = -2
c = -1
data = [[1.2, 0.7],[-0.3, -0.5],[3.0, 0.1],[-0.1, -1.0],[-1.0, 1.1],[2.1, -3]]
labels = [1,-1,1,-1,-1,1]

for iter in range(100000):
    i = int(np.floor(rd.rand()*len(data)))
    x = data[i][0]
    y = data[i][1]
    label = labels[i]

    score = a*x + b*y + c
    pull = 0.0
    if label == 1 and score < 1: pull = 1.0
    if label == -1 and score > -1: pull -1.0

    step_size = 0.01
    a += step_size * (x * pull - a)
    b += step_size * (y * pull - b)
    c += step_size * (1.0 * pull)
    if iter%1000==0: print('iter =',iter,':',[np.round(a,5),np.round(b,5),np.round(c,5)])