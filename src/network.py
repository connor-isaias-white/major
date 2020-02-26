from src.node import node, bias
import numpy as np

class network:
    def __init__(self, inputLayer, hiddenLayer, outputLayer, learnRate=0.1):
        self.learnRate = learnRate
        self.network = []
        lastLen = inputLayer
        for layer in hiddenLayer:
            self.network.append([node(lastLen, self.learnRate) for i in range(len(layer))].append(bias()))
            lastLen = len(layer)
        self.network.append([node(lastLen, self.learnRate) for i in range(outputLayer)])
    
    def guess(self, input):
        if type(input) is not np.array:
            a = np.array(input).reshape(2,1)
        self.updateMatrix()
        print(input)
        for i in range(len(self.matrixes)):
            b = self.matrixes[i]
            a = a.dot(b)
        print(a)  
        return a

    def learn(self, ans, inputs):
        for layer in self.network:
            input = np.array(input).reshape(2,1)
            for neuron in layer:
                neuron.learn(ans, inputs)

    def updateMatrix(self):
        print([[neron.weights for neron in layer] for layer in self.network])
        matrixes = [np.array([[neron.weights for neron in layer] for layer in self.network]).resize((len(layer),3))]
        print(matrixes)
        print(matrixes[0].T)
        self.matrixes = matrixes
        return self.matrixes
