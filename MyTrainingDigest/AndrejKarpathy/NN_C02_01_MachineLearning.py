import NN_C01_03_Ex_SingleNeuron as prevModule
import numpy as np
import numpy.random as rd

# A circuit: it takes 5 Units (x,y,a,b,c) and outputs a single Unit
# It can also compute the gradient w.r.t. its inputs
class Circuit:
    # create some gates
    def __init__(self):
        self.mulg0 = prevModule.multiplyGate()
        self.mulg1 = prevModule.multiplyGate()
        self.addg0 = prevModule.addGate()
        self.addg1 = prevModule.addGate()

    def forward(self,x,y,a,b,c):
        self.ax = self.mulg0.forward(a, x) # a*x
        self.by = self.mulg1.forward(b, y) # b*y
        self.axpby = self.addg0.forward(self.ax, self.by) # a*x + b*y
        self.axpbypc = self.addg1.forward(self.axpby, c) # a*x + b*y + c
        return self.axpbypc
    
    def backward(self,gradient_top): # takes pull from above
        self.axpbypc.grad = gradient_top
        self.addg1.backward() # sets gradient in axpby and c
        self.addg0.backward() # sets gradient in ax and by
        self.mulg1.backward() # sets gradient in b and y
        self.mulg0.backward() # sets gradient in a and x

# SVM class
class SVM:
    # random initial parameter values
    def __init__(self):
        self.a = prevModule.Unit(1.0, 0.0)
        self.b = prevModule.Unit(-2.0, 0.0)
        self.c = prevModule.Unit(-1.0, 0.0)

        self.circuit = Circuit()
    
    def forward(self, x, y): # assume x and y are Units
        self.unit_out = self.circuit.forward(x, y, self.a, self.b, self.c)
        return self.unit_out

    def backward(self,label): # label is +1 or -1
    # reset pulls on a,b,c
        self.a.grad = 0.0
        self.b.grad = 0.0
        self.c.grad = 0.0
        # compute the pull based on what the circuit output was
        pull = 0.0
        if label == 1 and self.unit_out.value < 1:
            pull = 1.0 # the score was too low: pull up
        if label == -1 and self.unit_out.value > -1:
            pull = -1 # the score was too high for a positive example, pull down
        self.circuit.backward(pull) # writes gradient into x,y,a,b,c
        # add regularization pull for parameters: towards zero and proportional to value
        self.a.grad += -self.a.value
        self.b.grad += -self.b.value
        
    def learnFrom(self,x, y, label):
        self.forward(x, y) # forward pass (set .value in all Units)
        self.backward(label) # backward pass (set .grad in all Units)
        self.parameterUpdate() # parameters respond to tug

    def parameterUpdate(self,step_size=0.01):
        self.a.value += step_size * self.a.grad
        self.b.value += step_size * self.b.grad
        self.c.value += step_size * self.c.grad

# SVM Training with Stochastic Gradient Descent
data = [[1.2,0.7],[-0.3,-0.5],[3.0,0.1],[-0.1,-1.0],[-1.0, 1.1],[2.1, -3]]
labels = [1,-1,1,-1,-1,1]
svm = SVM()

# a function that computes the classification accuracy
def evalTrainingAccuracy():
    num_correct = 0
    for i in range(len(data)):
        x = prevModule.Unit(data[i][0],0.0)
        y = prevModule.Unit(data[i][1],0.0)
        true_label = labels[i]
        # see if the prediction matches the provided label
        predicted_label = svm.forward(x,y).value
        if predicted_label > 0: predicted_label=1
        else: predicted_label=-1
        if predicted_label == true_label: num_correct+=1
    return num_correct/len(data)

# the learning loop
for iter in range(3000):
    # pick a random data point
    i = int(np.floor(rd.rand()*len(data)))
    x = prevModule.Unit(data[i][0],0.0)
    y = prevModule.Unit(data[i][1],0.0)
    label = labels[i]
    svm.learnFrom(x,y,label)
    if iter%150==0: print('accuracy at i =',iter,':',evalTrainingAccuracy())