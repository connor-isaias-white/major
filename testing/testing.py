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

if __name__ == "__main__":

    for run in range (6000):
        for i in trainData:
            pass



class neuron:

    def __init__(self):
        self.bias = random.random()

    def value(self, layer):
        val = self.bias
        numPrev = len(layer)
        val = bias
        for neral in layer:
            weight = random.random()
            val += weight*layer[neral]
        self.value = self.sig(val)


    def sig(x):
        y = 1/(1+math.exp(-x))
        return y
