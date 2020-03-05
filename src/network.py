from src.node import neuron, bias
import numpy as np
import src.actives as acv

class network:
    def __init__(self, inputLayer, hiddenLayer, outputLayer, learnRate=0.1, bias=True):
        self.learnRate = learnRate
        self.network = []
        self.bias = bias
        lastLen = inputLayer
        if self.bias:
            lastLen +=1
        for layer in hiddenLayer:
            neurons = [neuron(lastLen, self.learnRate) for i in range(layer)]
            self.network.append(neurons)
            lastLen = layer
            #print(self.network)
        self.network.append([neuron(lastLen, self.learnRate) for i in range(outputLayer)])
   
    def guess(self, inputs):
        self.inputs = []
        a = inputs.reshape(len(inputs),1)
        self.updateMatrix()
        # print(self.matrixes)
        for i in range(len(self.matrixes)):
            # add bias
            if self.bias:
                a = np.concatenate((a,[[1]]))
            self.inputs.append(a)
            b = self.matrixes[i]
            #print(f"a:\n{a.shape}\n{a.T}") 
            #print(f"b:\n{b.shape}\n{b.T}") 
            a = acv.LeReLu(b.dot(a), 0.01)
        a = acv.tanh(acv.LeReLu(a, 100))
        #print(f"guess: {a}") 
        return a

    def learn(self, ans):
        for layer in range(len(self.network)):
            for neuron in self.network[layer]:
                neuron.learn(ans, self.inputs[layer])

    def updateMatrix(self):
        matrixes = [np.resize(np.array([node.weights for node in layer]), (len(layer),len(layer[0].weights))) for layer in self.network]
        self.matrixes = matrixes
        return self.matrixes
