from src.node import node, bias
import numpy

class network:
    def __init__(self, inputLayer, hiddenLayer, outputLayer, learnRate=0.1):
        self.learnRate = learnRate
        self.network = []
        lastLen = len(inputLayer)
        for layer in hiddenLayer:
            self.network.append([node(lastLen, self.learnRate) for i in range(len(layer))].append(bias()))
            lastLen = len(layer)
        self.network.append([node(lastLen, self.learRate) for i in range(len(outputLayer))])
    
    def matrix(self):
        pass

