import random
import math
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas
import copy
import tkinter as tk

config = {
    # 'layers': 2,
    # 'neuroninlayer': [3, 1],
    'initinputLength': 8,
}

class Network:
    def __init__(self, pos, *argv, **kwargs):
        self.pos = pos
        self.numlayers = 2#random.randint(2, config['initinputLength'])
        self.neuroninlayer = [config["initinputLength"]-1]#[random.randint(2, config['initinputLength']+1) for i in range(self.numlayers - 1)]
        self.neuroninlayer.append(1)
        self.layers = []
        self.fitness = 0
        self.childrenMade = 0
        if len(kwargs) is not 0:
            #print(id(kwargs['layers']))
            #print(id(self.layers))
            self.layers = copy.deepcopy(kwargs['layers'])
            #print(id(self.layers))
        else:
            self.createNetwork()


    def createNetwork(self):
        for hiddenlayer in range(self.numlayers):
            layer = []
            for neuro in range(self.neuroninlayer[hiddenlayer]):
                if hiddenlayer != 0:
                    inputLength = self.neuroninlayer[hiddenlayer-1]
                else:
                    inputLength = config['initinputLength']
                layer.append(neuron(neuro,inputLength))
            self.layers.append(layer)

    def createChild(self, pos, rate, chance):
        copyChild = Network(pos, layers=self.layers)
        #print(f"1: {copyChild.layers == net.layers}")
        newChild = self.mutateBaby(copyChild, rate, chance)
        #print(f"2: {newChild.layers == net.layers}")
        self.childrenMade +=1
        return newChild

    def keepInRange(self, value):
        if value > 6:
            value = 6
        elif value < -6:
            value = -6
        return value

    def mutateBaby(self, baby, rate, chance):

        for layer in baby.layers:
            for neuron in layer:
                if random.random() < chance:
                    neuron.bias += rate*random.uniform(-1,1)
                    neuron.bias = self.keepInRange(neuron.bias)
                for weight in range(len(neuron.weights)):
                    if random.random() < chance:
                        neuron.weights[weight] += rate*random.uniform(-1,1)
                        neuron.weights[weight] = self.keepInRange(neuron.weights[weight])
        return baby




class generation:
    def __init__(self, num):
        self.popSize = num
        self.gen = [Network(net) for net in range(num)]
        self.genNum = 0
        self.genAv = 0

    def fittest(self, champion, rate, chance):
        #champion remains unchanged
        total = 0
        # print(champion)
        # print(f"1: {champion.layers[0][0].bias}")
        for net in self.gen:
            total += net.fitness
        newGen = [self.pickParrent(total, i, champion, rate, chance) for i in range(self.popSize-1)]
        self.gen = newGen
        # print(champion)
        # print(f"3: {champion.layers[0][0].bias}")
        self.gen.insert(0, champion)
        self.genNum +=1
        self.genAv = 0

    def pickParrent(self, total, num, champion, rate, chance):
        rand = random.randint(0, total)
        runningSum = 0
        for net in self.gen:
            runningSum += net.fitness
            if runningSum > rand:
                #print(f"2: {champion.layers[0][0].bias}")
                return net.createChild(num, rate, chance)
        print("no")



class neuron:

    def __init__(self, pos, inputLength):
        self.bias = random.uniform(-6, 6)
        self.pos = pos
        self.weights = [random.uniform(-6, 6) for i in range(inputLength)]

    def value(self, layer):
        val = self.bias
        numPrev = len(layer)
        val = self.bias
        for neral in range(len(layer)):
            weight = self.weights[neral]
            val += weight*layer[neral]
        self.val = self.sig(val)


    def sig(self, x):
        #print(x)
        y = 1/(1+math.exp(-x))
        return y

def train():
    perfectNotFount = True
    run = 0
    bestPer= [0,0]
    gen = generation(100)
    while perfectNotFount:
        for net in gen.gen:
            percent, raw = network(trainData, net.layers)
            net.fitness = raw**7

            if percent == 100 or percent ==0:
                print(f'\ncorrect: {round(percent)}%, after {run} tries, generation: {gen.genNum} {net.numlayers-1} hidden layers and setup like {net.neuroninlayer}', end = '\r')
                testResults = test(net)[0]
                if testResults == 100 or testResults== 0:
                    perfectNotFount = False
                    return net
            if percent > bestPer[0]:
                bestPer=[percent,1, net]
            elif percent == bestPer[0]:
                bestPer=[percent,bestPer[1] + 1, net]

            gen.genAv = (gen.genAv*(run % len(gen.gen))+percent)/((run % len(gen.gen))+1)
            print(f'run num: {run} generation: {gen.genNum} correct: {round(percent)}% genAv: {round(gen.genAv)}% top: {round(bestPer[0])}%, gotten {bestPer[1]} time(s), champ made {bestPer[2].childrenMade} children', end="\r")
            run += 1
        gen.fittest(bestPer[2], 0.6, 0.6)

def network(datas, layers):
    score = 0
    for data in datas:
        guess = putInNetwork(data[0], layers)
        if round(guess[0]) == data[1]:
            score += 1
    percent = score/len(datas)*100
    return percent, score

def putInNetwork(input, layers):
    #print(len(layers))
    for layer in layers:
        output = []
        for nero in layer:
            nero.value(input)
            output.append(nero.val)
        input = output
    return output


def test(best):
    final = network(testData, best.layers)
    print(f"\ntesting score: {round(final[0])}%", end="\r")
    return final

def createData():
    length = config["initinputLength"]
    testData = []
    trainData = []
    for i in range(2**length):
        num = bin(i)[2:]
        datavalue = [0 for i in range(length-len(str(num)))]
        for i in str(num):
            datavalue.append(int(i))

        ans = 0
        for binary in range(length-1):
            if datavalue[binary+1] == datavalue[binary] and datavalue[binary] == 1:
                ans = 1
        if random.random() > 0.80:
            testData.append([datavalue, ans])
        else:
            trainData.append([datavalue, ans])
    return trainData, testData


def plot(network):
    master = tk.Tk()
    NN = network.layers
    canvas_width = 720
    canvas_height = 720
    w = tk.Canvas(master,
               width=canvas_width,
               height=canvas_height)
    w.pack()
    # w.create_line(0, 50, 50, 50, fill="black")
    NN.insert(0, range(config['initinputLength']))
    for layer in range(len(NN)):
        totalNerons = len(NN[layer])
        for neron in range(len(NN[layer])):
            distance = canvas_height/(config['initinputLength']*3-totalNerons+1)
            colour = colour = "#"+''.join([hex(random.randint(16, 255))[2:] for i in range(3)])
            x = int(((layer+1)/(len(NN)+1))*canvas_width)+10
            y = int( (canvas_height/2) +((-1)**(neron+1)) *distance*(int((neron+1+((totalNerons+1) % 2))/2) ))
            #print(f"x: {x}, y:{y}, distance: {distance}")
            if layer > 0:
                radius = NN[layer][neron].sig(NN[layer][neron].bias)*10+5
                for input in range(len(NN[layer-1])):
                    weight = NN[layer][neron].sig(NN[layer][neron].weights[input])
                    distance2 = canvas_height/(config['initinputLength']*3-len(NN[layer-1])+1)
                    x2 = int(((layer)/(len(NN)+1))*canvas_width)+10
                    y2 = int( (canvas_height/2) +((-1)**(input+1)) *distance2*(int((input+1+((len(NN[layer-1])+1) % 2))/2) ))
                    w.create_line(x2,y2,x,y, width = weight*10, fill=colour)
            else:
                radius = 10
            circle(w, x,  y, radius, colour)
    network.layers = NN[1:]
    tk.mainloop()

def circle(canvas,x,y, r, colour):
   id = canvas.create_oval(x-r,y-r,x+r,y+r, fill=colour)
   return id

if __name__ == "__main__":
    trainData, testData = createData()
    while len(testData)*len(trainData) == 0:
        trainData, testData = createData()
    print(f"train data length: {len(trainData)}, test data length: {len(testData)}")

    best = train()
    if best != []:
        plot(best)
        '''print(f"input {config['initinputLength']} 1s or 0s seperated by commas and the network will tell if 2 1s are ajacent")
        manData = input("> ")
        while manData:
            manData = manData.replace(" ", '').split(",")
            data = [int(i) for i in manData]
            output = round(putInNetwork(data, best)[0])
            if output == final/100:
                print("at least 2 adjacent 1s")
            else:
                print("No adjacent 1s")
            manData = input("> ")'''
