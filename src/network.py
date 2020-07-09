from multiprocessing import Pool
from src.node import neuron
import numpy as np
import src.actives as acv
import time
import dill as pickle
import os

# network class to create and change neural networks
class network:
    def __init__(self, inputLayer, hiddenLayer, outputLayer, learnRate=0.1, bias=True, batch=128, \
            actFun="sig", loss="mse", opt="gd"):
        #set activation functions
        if actFun == "sig":
            self.act = lambda x: acv.sig(x, a=1)
            self.dAct = lambda x: acv.dSig(x)
            self.rAct = lambda y: acv.rSig(y)
            self.out = self.act
        elif actFun == "LeReLu":
            self.act = lambda x: acv.LeReLu(x, 0.01)
            self.dAct = lambda x: acv.dLeReLu(x, 0.01)
            self.rAct = lambda y: acv.LeReLu(y, 100)
            self.out = lambda x: acv.softmax(x)

        #set optimizers
        if loss == "mse":
            self.loss = lambda outs, expt: sum([(outs[-1][i] - expt[i])**2 for i in range(len(expt))])
            self.dloss = lambda outs, expt, node: 2*(outs[-1][node]- expt[node])
        elif loss == "cel":
            self.loss = lambda outs, expt: sum([-expt[i]*np.log(outs[-1][i]) for i in range(len(expt))])
            self.dloss = lambda outs, expt, node: -expt[node]/(outs[-1][node])

        # configuation variables
        self.testingTimes = []
        self.cost = 1
        self.learnRate = learnRate
        self.bias = bias
        self.batch = batch
        self.batchCount = 0
        self.aveNablaC = np.zeros(len(hiddenLayer)+1)
        self.network = self.crete_network(inputLayer, hiddenLayer, outputLayer, opt)
        self.biggestin = self.most_weights(hiddenLayer, inputLayer)
        self.biggestout = self.most_weights(hiddenLayer, outputLayer)

    def most_weights(self, *args):
        biggest = 0
        comb = []
        for x in args:
            if type(x) == list:
                comb += x
            else:
                comb += [x]
        for i in range(len(comb)-1):
            if comb[i] *comb[i+1] > biggest:
                biggest = comb[i] *comb[i+1]
        return biggest

    def find_largest(self, *args):
        biggest = 0
        for y in args:
            if type(y) == list:
                for x in y:
                    if x > biggest:
                        biggest = x
            else:
                if y > biggest:
                    biggest = x
        return biggest

    def crete_network(self, inputLayer, hiddenLayer, outputLayer, opt):
        '''  crete_network to given size '''
        network_creation = []
        lastLen = inputLayer + self.bias
        for layer in range(len(hiddenLayer)):
            neurons = [neuron(lastLen, self.learnRate, optimizer=opt) \
                    for i in range(hiddenLayer[layer])]
            network_creation.append(neurons)
            lastLen = hiddenLayer[layer] + self.bias
        network_creation.append([neuron(lastLen, self.learnRate, optimizer=opt) for i in range(outputLayer)])
        return network_creation

    def guess(self, inp):
        ''' guesses an output with a given input '''
        self.inputs = np.zeros((len(self.network),self.biggestin^2))
        self.outputs = np.zeros((len(self.network),self.biggestout^2))
        a = inp.reshape(len(inp), 1)
        self.updateMatrix()
        #print(self.matrixes)
        for i in range(len(self.matrixes)):
            # add bias
            if self.bias:
                a = np.concatenate((a,[[1]]))
            #print(self.inputs)
            #print(i)
            #print(a)
            for j in range(len(a)-1):
                self.inputs[i][j] = a[j]
            b = self.matrixes[i]
            #print(f"a:\n{a.shape}\n{a.T}")
            #print(f"b:\n{b.shape}\n{b.T}")
            a = self.act(b.dot(a))
            for j in range(len(a)-1):
                self.outputs[i][j] = a[j]
        #print("OUT TIME")
        #print(self.rAct(a))
        a = self.out(self.rAct(a))
        for j in range(len(a)-1):
            self.outputs[-1][j] = a[j]
        #print(f"guess: {a}")
        return a

    def updateBatch(self, nablaC):
        pass

    def learn(self, ans):
        ''' learns from the last guess with a given output '''
        nablaC = self.backprop(ans)
        if self.batchCount == 0:
            self.aveNablaC = nablaC
        else:
            self.aveNablaC += nablaC
        self.batchCount += 1
        if self.batchCount >= self.batch:
            self.aveNablaC = self.aveNablaC/self.batch
            for layer in range(len(self.network)):
                for neuron in range(len(self.network[layer])):
                    self.network[layer][neuron].learn(self.aveNablaC[layer][neuron], self.batch)
            self.aveNablaC = None
            self.batchCount = 0

    def backprop(self, expt):
        ''' function to return the gradient of the loss function '''
        self.j = 0
        startTime = time.time()
        self.cost = self.loss(self.outputs, expt)
        nablaC = np.zeros((len(self.network), self.find_largest([len(i) for i in self.network]), self.biggestin))
        for matrix in range(len(self.matrixes)):
            for node in range(len(self.matrixes[matrix])):
                for weight in range(len(self.matrixes[matrix][node])):
                    nablaC[matrix][node][weight] = self.partial_sum(expt, matrix, node, weight)
        self.resetAC()
        endTime = time.time() - startTime
        self.testingTimes.append(endTime)
        print(f"ave backprop end time:{sum(self.testingTimes)/len(self.testingTimes)}s")
        return nablaC

    def partial_sum(self, expt, matrix, node, weight):
        weightedImportance= self.inputs[matrix][weight]* \
                self.dAct(self.outputs[matrix][node])* \
                self.partCpartA(matrix, node, expt)
        return weightedImportance

    #partial c / parial a
    #speed fix by saving them to the node
    # they currently belive they change the bias
    def partCpartA(self, layer, node, expt):
        startTime = time.time()
        if layer == len(self.matrixes)-1:
            return self.dloss(self.outputs, expt, node)
        else:
            if self.network[layer][node].AC == 0:
                AC = [self.matrixes[layer+1][j][node]* \
                    self.dAct(self.rAct(self.outputs[layer+1][j]))* \
                    self.partCpartA(layer+1, j, expt)
                    for j in range(len(self.matrixes[layer+1]))]
                sumAC = sum(AC)
                self.network[layer][node].AC = sumAC
                return sumAC
            else:
                #print(f"cached endTime {time.time()-startTime}")
                return self.network[layer][node].AC

    def updateMatrix(self):
        matrixes = np.array([np.resize(np.array([node.weights for node in layer]), \
                (len(layer),len(layer[0].weights))) for layer in self.network])
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

    def mutate(self, chance):
        for layer in self.network:
            for node in layer:
                node.mutate(chance)

    def writeNetwork(self, path):
        self.updateMatrix()
        with open(path, "wb+") as f:
            pickle.dump(self, f)

    @staticmethod
    def readNetwork(path):
        print(path)
        print(os.getcwd())
        with open(path, "rb") as f:
            self = pickle.load(f)
        return self

