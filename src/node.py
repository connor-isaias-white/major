import random
import numpy as np
import src.actives as acv

class node:
    def __init__(self, name):
        self.name = name

    def output(self, inputs):
        out = acv.tanh(self.weights.dot(np.squeeze(inputs)))
        self.val = out
        return out

class bias(node):
    def __init__(self, numInputs):
        self.val = 1
        self.weights = np.array([0 for i in range(numInputs)]+[255])
        return super().__init__("bias")

    def learn(self, *args):
        pass

class neuron(node):
    def __init__(self, numInputs, learnRate, val=0):
        self.weights=np.array([random.random() for i in range(numInputs+1)])
        self.learnRate = learnRate
        self.val = val
        return super().__init__("neuron")
    
    def learn(self, inputs, grad):
        #print(f"inputs:\n{inputs}")
        print(grad)
        for i in range(len(self.weights)):
            #print(error*inputs[i,0]*self.learnRate)
            #print(grad[i]*inputs[i,0]*self.learnRate)
            self.weights[i] += grad[i]*self.learnRate

