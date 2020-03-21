from src.node import neuron, bias
import numpy as np
import src.actives as acv

class network:
    def __init__(self, inputLayer, hiddenLayer, outputLayer, learnRate=0.1, bias=True, batch=20, actFun="sig"):
        #set activation functions
        if actFun == "sig":
            self.act = lambda x: acv.sig(x)
            self.dAct = lambda x: acv.dSig(x)
            self.rAct = lambda y: acv.rSig(y)
            self.out = self.act
        if actFun == "LeReLu":
            self.act = lambda x: acv.LeReLu(x, 0.01)
            self.dAct = lambda x: acv.dLeReLu(x, 0.01)
            self.rAct = lambda y: acv.LeReLu(y, 100)
            self.out = lambda x: acv.sig(x)

        self.learnRate = learnRate
        self.network = []
        self.bias = bias
        self.batch = batch
        self.batchCount = 0
        self.aveNablaC = []
        lastLen = inputLayer + self.bias
        for layer in hiddenLayer:
            neurons = [neuron(lastLen, self.learnRate) for i in range(layer)]
            self.network.append(neurons)
            #print(layer + self.bias)
            lastLen = layer + self.bias
            #print(self.network)
        self.network.append([neuron(lastLen, self.learnRate) for i in range(outputLayer)])

    def guess(self, inputs):
        self.inputs = []
        self.outputs = []
        a = inputs.reshape(len(inputs),1)
        self.updateMatrix()
        #print(self.matrixes)
        for i in range(len(self.matrixes)):
            # add bias
            if self.bias:
                a = np.concatenate((a,[[1]]))
            self.inputs.append(a)
            b = self.matrixes[i]
            #print(f"a:\n{a.shape}\n{a.T}")
            #print(f"b:\n{b.shape}\n{b.T}")
            a = self.act(b.dot(a))
            self.outputs.append(a)
        a = self.out(self.rAct(a))
        self.outputs[-1] = a
        #print(f"guess: {a}")
        return a

    def updateBatch(self, nablaC):
        pass

    def learn(self, ans):
        nablaC = self.backprop(ans)
        if self.batchCount == 0:
            self.aveNablaC = nablaC
        else:
            for layer in range(len(nablaC)):
                for node in range(len(nablaC[layer])):
                    for deltaWeight in range(len(nablaC[layer][node])):
                        self.aveNablaC[layer][node][deltaWeight] += nablaC[layer][node][deltaWeight]
        self.batchCount +=1
        #this is broken
        if self.batchCount == self.batch:
            for layer in range(len(self.network)):
                for neuron in range(len(self.network[layer])):
                    for deltaWeight in range(len(self.aveNablaC[layer][neuron])):
                        self.aveNablaC[layer][neuron][deltaWeight] = self.aveNablaC[layer][neuron][deltaWeight]/self.batch
                    self.network[layer][neuron].learn(self.inputs[layer], self.aveNablaC[layer][neuron])
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
                # this is broken
                for weight in range(len(self.matrixes[matrix][node])):
                    #print(self.inputs)
                    #print(matrix-1, weight)
                    #print(self.inputs[matrix][weight])
                    weightImportance = self.inputs[matrix][weight][0] * \
                            self.dAct(self.outputs[matrix][node][0]) *\
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
        #print(self.matrixes)
        #print(len(self.matrixes[layer][0]))
        if layer == len(self.matrixes):
            return 2*(self.outputs[-1][0][0]- expt)
        else:
            AC = [self.matrixes[layer][j][weight]* \
                self.dAct(self.outputs[layer][j][0])* \
                self.partCpartA(layer+1, weight, expt)
                for j in range(len(self.matrixes[layer]))]
            sumAC = sum(AC)
            return sumAC

    def updateMatrix(self):
        matrixes = [np.resize(np.array([node.weights for node in layer]), (len(layer),len(layer[0].weights))) for layer in self.network]
        self.matrixes = matrixes
        return self.matrixes
