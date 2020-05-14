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
    def __init__(self, numInputs, learnRate, val=0, optimizer="gd", momrate=0):
        self.weights=np.array([random.uniform(-0.1,0.1) for i in range(numInputs)])
        self.learnRate = learnRate
        self.val = val
        self.AC = 0
        self.z = 0
        self.momrate = momrate
        self.optimizer = optimizer
        return super().__init__("neuron")

    def learn(self, grad):
        for weight in range(len(self.weights)):
            if self.optimizer == "gd":
                self.weights[weight] -= grad[weight]*self.learnRate
            elif self.optimizer == "mom":
                self.z = self.z*self.momrate + grad[weight]
                self.weights[weight] -= self.learnRate*self.z
    def mutate(chance):
        for weight in range(len(self.weights)):
            if chance> random.random():
                self.weights[weight] += random.uniform(-1,1)*self.learnRate

