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
        self.weights = np.array([0 for i in range(numInputs)])
        return super().__init__("bias")

    def learn(self, *args):
        pass

class neuron(node):
    def __init__(self, numInputs, learnRate, val=0):
        self.weights=np.array([random.uniform(-1,1) for i in range(numInputs)])
        self.learnRate = learnRate
        self.val = val
        self.AC = 0
        return super().__init__("neuron")

    def learn(self, inputs, grad):
        #print(f"inputs:\n{inputs}")
        #print(grad)
        for weight in range(len(self.weights)):
            #print(error*inputs[i,0]*self.learnRate)
            #print(grad[i]*inputs[i,0]*self.learnRate)
            self.weights[weight] -= grad[weight]*self.learnRate
    def mutate(chance):
        for weight in range(len(self.weights)):
            if chance> random.random():
                self.weights[weight] += random.uniform(-1,1)*self.learnRate

