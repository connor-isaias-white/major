import random
import maths
import numpy as np

class node:
    def __init__(self, numInputs, learnRate):
        self.weights = np.array([random.random for i in range(len(numInputs)+1)])
        self.learnRate = learnRate
        self.val = 0

    def output(self, input):
        self.val = self.sig(np.dot(input, self.weights)+self.bias)
        return self.val

    def sig(self, x):
        y = 1/(maths.e(-x)+1)
        return y
    
    def learn(self, ans, input):
        error = ans - self.output(input)
        for i in range(len(self.weights)):
            self.weights[i] += error*input[i]*self.learnRate

class bias(node):
    def __init__(self):
        self.val = 1
        return super().__init__(0, 0)

