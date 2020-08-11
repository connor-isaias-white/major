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
    def __init__(self, numInputs, learnRate, val=0, optimizer="gd", b1=0.9, b2=0.999):
        self.weights=np.array([random.uniform(-0.1,0.1) for i in range(numInputs)])
        self.learnRate = learnRate
        self.val = val
        self.AC = 0
        self.v = 0
        self.s = 0
        self.b1 = b1
        self.b2 = b2
        self.t = 1
        self.optimizer = optimizer
        return super().__init__("neuron")

    def learn(self, grad, batch):
        for weight in range(len(self.weights)):
            if self.optimizer == "gd":
                self.weights[weight] -= grad[weight]*self.learnRate
            elif self.optimizer == "mom":
                self.v = self.v*self.b1 + grad[weight]
                self.weights[weight] -= self.learnRate*self.v
            elif self.optimizer == "adam":
                self.v = self.b2*self.v+(1-self.b2)*grad[weight]
                self.s = self.b1*self.s + (1-self.b1)*((grad[weight])**2)
                vhat = self.v/(1-self.b1**self.t)
                shat = self.s/(1-self.b2**self.t)
                self.t +=1
                self.weights[weight] -= self.learnRate*(vhat)/((shat)**(1/2)+1*10**(-8))

    def mutate(chance):
        for weight in range(len(self.weights)):
            if chance> random.random():
                self.weights[weight] += random.uniform(-1,1)*self.learnRate

