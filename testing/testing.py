import random
import math
trainData = {
    [1,1,1,1]: 1,
    [1,1,1,0]: 1,
    [1,1,0,1]: 1,
    [1,0,1,1]: 1,
    [1,0,1,0]: 0,
    [1,0,0,1]: 0,
    [1,0,0,0]: 0,
    [0,1,1,0]: 1,
    [0,1,0,1]: 0,
    [0,1,0,0]: 0,
    [0,0,1,1]: 1,
    [0,0,0,0]: 0,
}
testData = {
    [1,1,0,0]: 1,
    [0,1,1,1]: 1,
    [0,0,1,0]: 0,
    [0,0,0,1]: 0,

}

def neuron(layer):
    bias = random.random()
    numPrev = len(layer)
    val = bias
    for neral in layer:
        weight = random.random()
        val += weight*layer[neral]
    val = sig(val)

if __name__ == "__main__":

    for run in range (6000):
        for i in trainData:
            pass



class neuron:

    def __init__(self):
        self.bias = random.random()

    def value(self):
        pass

    def sig(x):
        y = 1/(1+math.exp(-x))
        return y
