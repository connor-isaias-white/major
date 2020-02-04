import random
import math
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas
import tkinter as tk

config = {
    # 'layers': 2,
    # 'neuroninlayer': [3, 1],
    'initinputLength': 5,
}

class Network:
    def __init__(self):
        self.numlayers = random.randint(2, config['initinputLength'])
        self.neuroninlayer = [random.randint(2, config['initinputLength']+1) for i in range(self.numlayers - 1)]
        self.neuroninlayer.append(1)
        self.layers = []
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
        y = 1/(1+math.exp(-x))
        return y

def train():
    perfectNotFount = True
    run = 0
    bestPer= [0,0]
    while perfectNotFount:
        newNetwork = Network()
        percent = network(trainData, newNetwork.layers)
        if percent == 100 or percent ==0:
            print(f'correct: {percent}%, after {run} tries, {newNetwork.numlayers-1} hidden layers and setup like {newNetwork.neuroninlayer}')
            testResults = test(newNetwork)
            if testResults == 100 or testResults== 0:
                perfectNotFount = False
                return newNetwork
        elif percent > bestPer[0]:
            bestPer=[percent,1]
        elif percent == bestPer[0]:
            bestPer[1] += 1
        print(f'run num: {run} correct: {percent}% top: {bestPer[0]}%, gotten {bestPer[1]} times', end="\r")
        run += 1

def network(datas, layers):
    score = 0
    for data in datas:
        guess = putInNetwork(data[0], layers)
        if round(guess[0]) == data[1]:
            score += 1
    percent = round(score/len(datas)*100)
    return percent

def putInNetwork(input, layers):
    for layer in layers:
        output = []
        for nero in layer:
            nero.value(input)
            output.append(nero.val)
        input = output
    return output


def test(best):
    final = network(testData, best.layers)
    print(f"testing score: {final}%")
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
    network = network.layers
    canvas_width = 720
    canvas_height = 720
    w = tk.Canvas(master,
               width=canvas_width,
               height=canvas_height)
    w.pack()
    # w.create_line(0, 50, 50, 50, fill="black")
    network.insert(0, range(config['initinputLength']))
    for layer in range(len(network)):
        totalNerons = len(network[layer])
        for neron in range(len(network[layer])):
            distance = canvas_height/(config['initinputLength']*3-totalNerons+1)
            colour = colour = "#"+''.join([hex(random.randint(15, 255))[2:] for i in range(3)])
            x = int(((layer+1)/(len(network)+1))*canvas_width)+10
            y = int( (canvas_height/2) +((-1)**(neron+1)) *distance*(int((neron+1+((totalNerons+1) % 2))/2) ))
            #print(f"x: {x}, y:{y}, distance: {distance}")
            if layer > 0:
                radius = network[layer][neron].sig(network[layer][neron].bias)*10+5
                for input in range(len(network[layer-1])):
                    weight = network[layer][neron].sig(network[layer][neron].weights[input])
                    distance2 = canvas_height/(config['initinputLength']*3-len(network[layer-1])+1)
                    x2 = int(((layer)/(len(network)+1))*canvas_width)+10
                    y2 = int( (canvas_height/2) +((-1)**(input+1)) *distance2*(int((input+1+((len(network[layer-1])+1) % 2))/2) ))
                    w.create_line(x2,y2,x,y, width = weight*10, fill=colour)
            else:
                radius = 10
            circle(w, x,  y, radius, colour)
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
