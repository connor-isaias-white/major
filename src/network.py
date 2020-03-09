from src.node import neuron, bias
import numpy as np
import src.actives as acv

class network:
    def __init__(self, inputLayer, hiddenLayer, outputLayer, learnRate=0.1, bias=True, batch=20):
        self.learnRate = learnRate
        self.network = []
        self.bias = bias
        self.batch = batch
        self.batchCount = 0
        self.aveNablaC = []
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
        self.outputs = []
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
            a = acv.sig(b.dot(a))
            self.outputs.append(a)
        #a = acv.sig(acv.LeReLu(a, 100))
        self.outputs[-1] = a
        #print(f"guess: {a}") 
        return a

    def updateBatch(self, nablaC):
        pass

    def learn(self, ans):
        nablaC = self.backprop(ans)
        for layer in range(len(nablaC)):
            if self.batchCount == 0:
                self.aveNablaC.append([])
            for node in range(len(nablaC[layer])):
                if self.batchCount == 0:
                    self.aveNablaC[layer].append([])
                for deltaWeight in range(len(nablaC[layer][node])):
                    if self.batchCount == 0:
                        self.aveNablaC[layer][node].append(0)
                    self.aveNablaC[layer][node][deltaWeight] += nablaC[layer][node][deltaWeight]
        self.batchCount +=1
        if self.batchCount == self.batch:
            for layer in range(len(self.network)):
                for neuron in range(len(self.network[layer])):
                    for deltaWeight in range(len(nablaC[layer][node])):
                        self.aveNablaC[layer][neuron][deltaWeight] = self.aveNablaC[layer][neuron][deltaWeight]/self.batch
                    self.network[layer][neuron].learn(self.inputs[layer], nablaC[layer][neuron])
            self.aveNablaC = []
            self.batchCount = 0


    # This is very confusing maths that is hard to explain in a comment
    # To gain an understanding, watch https://www.youtube.com/watch?v=tIeHLnjs5U8
    # currently quite inefficient
    def backprop(self, expt):
        cost = (self.outputs[-1][0][0] - expt)**2
        nablaC = []
        for matrix in range(len(self.matrixes)):
            layeredImportance = []
            #print(f"matrix pos:\n{matrix}")
            #print(f"matrix :\n{self.matrixes[matrix]}") 
            #print(f"in:\n{self.inputs[matrix]}")
            #print(f"out:\n{self.outputs[matrix]}") 
            for node in range(len(self.matrixes[matrix])):
                nodelImportance = []
                for weight in range(len(self.matrixes[matrix][node])):
                    #print(self.inputs[matrix-1][weight])
                    weightImportance = self.inputs[matrix-1][weight][0] * \
                            acv.dSig(self.inputs[matrix][node][0]) *\
                            self.partCpartA(matrix+1, weight, expt)
                    #print(f"weight:\n{self.matrixes[matrix][node][weight]}") 
                    #print(f"weight importance:\n{weightImportance}")
                    #print(f"prev node:\n{self.inputs[matrix-1][weight][0]}")
                    #print(f"d active:\n{acv.dSig(self.inputs[matrix][node])}")
                    #print(f"CA:\n{self.partCpartA(matrix+1, weight, expt)}")
                    nodelImportance.append(weightImportance)
                layeredImportance.append(nodelImportance)
            nablaC.append(layeredImportance) 
        #print(f"nablaC: {nablaC}")
        return nablaC
    #partial c / parial a
    def partCpartA(self, layer, weight, expt):
        if layer == len(self.matrixes):
            return 2*(self.outputs[-1][0][0]- expt)
        else:
            AC = [self.matrixes[layer][j][weight]* \
                acv.dSig(self.outputs[layer][j])[0]* \
                self.partCpartA(layer+1, weight, expt)
                for j in range(len(self.matrixes[layer]))]  
            sumAC = sum(AC)
            return sumAC

    def updateMatrix(self):
        matrixes = [np.resize(np.array([node.weights for node in layer]), (len(layer),len(layer[0].weights))) for layer in self.network]
        self.matrixes = matrixes
        return self.matrixes
