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
            actFun="LeReLu", loss="mse", opt="gd"):
        #set activation functions
        if actFun == "sig":
            self.act = lambda x: acv.sig(x, a=1)
            self.dAct = lambda x: acv.dSig(x)
            self.rAct = lambda y: acv.rSig(y)
            self.out = lambda x: acv.sig(x,a=1)
        elif actFun == "LeReLu":
            self.act = lambda x: acv.LeReLu(x, 0.01)
            self.dAct = lambda x: acv.dLeReLu(x, 0.01)
            self.rAct = lambda y: acv.LeReLu(y, 100)
            self.out = lambda x: acv.softmax(x)

        #set optimizers
        if loss == "mse":
            self.loss = lambda outs, expt: sum([(outs[-1][i][0] - expt[i])**2 for i in range(len(expt))])
            self.dloss = lambda outs, expt, node, ins: 2*(outs[-1][node][0]- expt[node])
        elif loss == "cel":
            self.loss = lambda outs, expt: sum([-expt[i]*np.log(outs[-1][i][0]) - (1-expt[i])*np.log(1-outs[-1][i][0]) for i in range(len(expt))])
            self.dloss = lambda outs, expt, node, ins: (-expt[node]+(outs[-1][node][0]))*ins[-1][node][0]

        # configuation variables
        self.testingTimes = []
        self.cost = 1
        self.learnRate = learnRate
        self.bias = bias
        self.batch = batch
        self.batchCount = 0
        self.aveNablaC = []
        self.network = self.crete_network(inputLayer, hiddenLayer, outputLayer, opt)


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
        self.inputs = []
        self.outputs = []
        self.z = []
        a = inp.reshape(len(inp),1)
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
            a = b.dot(a)
            self.z.append(a)
            if i != len(self.matrixes) -1:
                a = self.act(a)
            else:
                a = self.out(a)
            self.outputs.append(a)
        #print(f"guess: {a}")
        return a

    def learn(self, ans):
        ''' learns from the last guess with a given output '''
        nablaC = self.backprop(ans)
        if self.batchCount == 0:
            self.aveNablaC = nablaC
        else:
            for layer in range(len(nablaC)):
                for node in range(len(nablaC[layer])):
                    for deltaWeight in range(len(nablaC[layer][node])):
                        self.aveNablaC[layer][node][deltaWeight] += nablaC[layer][node][deltaWeight]
        self.batchCount +=1
        if self.batchCount >= self.batch:
            #print(self.batchCount)
            for layer in range(len(self.network)):
                for neuron in range(len(self.network[layer])):
                    for deltaWeight in range(len(self.aveNablaC[layer][neuron])):
                        self.aveNablaC[layer][neuron][deltaWeight] = self.aveNablaC[layer][neuron][deltaWeight]/self.batch
                    self.network[layer][neuron].learn(self.aveNablaC[layer][neuron], self.batch)
            self.aveNablaC = []
            self.batchCount = 0

    def backprop(self, expt):
        ''' preforms the backpropogation algorithm, required to learn '''
        startTime = time.time()
        self.cost = self.loss(self.outputs, expt)
        nablaC = []
        for matrix in range(len(self.matrixes)):
            layeredImportance = []
            for node in range(len(self.matrixes[matrix])):
                nodelImportance = []
                for weight in range(len(self.matrixes[matrix][node])):
                    ak = self.inputs[matrix][weight][0]
                    do = self.dAct(self.outputs[matrix][node][0])
                    pcpa = self.partCpartA(matrix, node, expt)
                    weightImportance = ak*do*pcpa
                    nodelImportance.append(weightImportance)
                layeredImportance.append(nodelImportance)
            nablaC.append(layeredImportance)
        self.resetAC()
        endTime = time.time() - startTime
        #print(f"backprop end time:{endTime}s")
        return nablaC

    def partial_sum(self, expt, matrix, node, weight):
        ''' a dirvation of the sum to find the gradient '''
        weightedImportance= self.inputs[matrix][weight]* \
                self.dAct(self.outputs[matrix][node])* \
                self.partCpartA(matrix, node, expt)
        return weightedImportance

    #partial c / parial a
    def partCpartA(self, layer, node, expt):
        startTime = time.time()
        if layer == len(self.matrixes)-1:
            return self.dloss(self.outputs, expt, node, self.inputs)
        else:
            if self.network[layer][node].AC == 0:
                AC = [self.matrixes[layer+1][j][node]* \
                    self.dAct((self.z[layer+1][j]))* \
                    self.partCpartA(layer+1, j, expt)
                    for j in range(len(self.matrixes[layer+1]))]
                sumAC = sum(AC)
                self.network[layer][node].AC = sumAC
                return sumAC
            else:
                #print(f"cached endTime {time.time()-startTime}")
                return self.network[layer][node].AC

    def updateMatrix(self):
        ''' update the matrix to the new values '''
        matrixes = [np.resize(np.array([node.weights for node in layer]), (len(layer),len(layer[0].weights))) for layer in self.network]
        self.matrixes = matrixes
        return self.matrixes

    def randomize(self):
        ''' randomise values '''
        for layer in self.network:
            for node in layer:
                for weight in node:
                    weight = random.random()

    def resetAC(self):
        ''' reset cached values '''
        for layer in self.network:
            for node in layer:
                node.AC =0

    def mutate(self, chance):
        ''' change random parts of network '''
        for layer in self.network:
            for node in layer:
                node.mutate(chance)

    def writeNetwork(self, path):
        ''' save network to a file '''
        self.updateMatrix()
        with open(path, "wb+") as f:
            pickle.dump(self, f)

    @staticmethod
    def readNetwork(path):
        ''' read a network from file and inherate its values '''
        print(path)
        print(os.getcwd())
        with open(path, "rb") as f:
            self = pickle.load(f)
        return self
