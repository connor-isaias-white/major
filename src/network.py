from src.node import neuron, bias
import numpy as np
import src.actives as acv
import time

class network:
    def __init__(self, inputLayer, hiddenLayer, outputLayer, learnRate=0.1, bias=True, batch=20, actFun="sig"):
        #set activation functions
        if actFun == "sig":
            self.act = lambda x: acv.sig(x, a=1)
            self.dAct = lambda x: acv.dSig(x)
            self.rAct = lambda y: acv.rSig(y)
            self.out = self.act
        if actFun == "LeReLu":
            self.act = lambda x: acv.LeReLu(x, 0.01)
            self.dAct = lambda x: acv.dLeReLu(x, 0.01)
            self.rAct = lambda y: acv.LeReLu(y, 100)
            self.out = lambda x: acv.softmax(x)

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
    # currently extremely inefficient
    def backprop(self, expt):
        startTime = time.time()
        #print(f"backprop start time:{startTime}")
        cost = sum([(self.outputs[-1][j][0] - expt[j])**2 for j in \
                range(len(self.outputs[-1][0]))])
        nablaC = []
        #midTime = time.time()-startTime
        #print(f"backprop mid1 time:{midTime}s")
        for matrix in range(len(self.matrixes)):
            layeredImportance = []
            for node in range(len(self.matrixes[matrix])):
                nodelImportance = []
                # this is broken
                for weight in range(len(self.matrixes[matrix][node])):
                    #weightStart = time.time()
                    ak = self.inputs[matrix][weight][0]
                    #akTime = time.time()-weightStart
                    #print(f"    ak time: {akTime}s")
                    do = self.dAct(self.outputs[matrix][node][0])
                    #doTime = time.time()-akTime-weightStart
                    #print(f"    do time: {doTime}s")
                    pcpa = self.partCpartA(matrix, node, expt)
                    #pcpaTime = time.time() - doTime -akTime -weightStart
                    #print(f"   pcpa time: {pcpaTime}s")
                    weightImportance = ak*do*pcpa
                    nodelImportance.append(weightImportance)
                    #print(f"  matrix: {matrix} node: {node} weight: {weight} done, time:{time.time() - weightStart}s")
                layeredImportance.append(nodelImportance)
            nablaC.append(layeredImportance)
        self.resetAC()
        endTime = time.time() - startTime
        #print(f"backprop end time:{endTime}s")
        return nablaC

    #partial c / parial a
    #speed fix by saving them to the node
    # they currently belive they change the bias
    def partCpartA(self, layer, node, expt):
        if layer == len(self.matrixes)-1:
            return 2*(self.outputs[-1][node][0]- expt[node])
        else:
            if self.network[layer][node].AC == 0:
                AC = [self.matrixes[layer+1][j][node]* \
                    self.dAct(self.rAct(self.outputs[layer+1][j][0]))* \
                    self.partCpartA(layer+1, j, expt)
                    for j in range(len(self.matrixes[layer+1]))]
                sumAC = sum(AC)
                self.network[layer][node].AC = sumAC
                return sumAC
            else:
                return self.network[layer][node].AC

    def updateMatrix(self):
        matrixes = [np.resize(np.array([node.weights for node in layer]), (len(layer),len(layer[0].weights))) for layer in self.network]
        self.matrixes = matrixes
        return self.matrixes

    def randomize(self):
        for layer in self.network:
            for node in layer:
                for weight in node:
                    weight = random.random()

    def resetAC(self):
        for layer in self.network:
            for node in layer:
                node.AC =0


