import sys
sys.path.append("..")
from mnist.loader import MNIST
import random
import numpy as np
from os import path as p
import matplotlib.pyplot as plt
from time import time
from datetime import timedelta
from threading import Thread
from src.network import network

def temp_graph_data(data, labels):
    plt.scatter([i[0] for i in data], \
            [i[1] for i in data],
            c=[[0,0,i] for i in labels])
    plt.show()


def graphing(graphData, percentage):
    plt.close()
    plt.ion()
    plt.show()
    plt.plot(range(len(graphData)), graphData, range(len(graphData)), percentage)
    plt.draw()
    plt.pause(0.00001)


def train(runs, nn, images, labels, batch, graph):
    startTime = int(time())
    aveCost = 0
    epoch = 0
    epochCorrect = 0
    if graph:
        epochList = []
        epochPercentages = []
    for run in range(runs):
        correct = 0
        for image in range(len(images)):
            guess = nn.guess(np.array(images[image])/255)
            print(f"guess:\n{guess}")
            numguess = np.where(guess == np.amax(guess))[0][0]
            print(f"numguess: {numguess}")
            print(f"Answer: {labels[image]}")
            #print([0.0 if labels[image] != i else 1.0 for i in range(len(guess))])
            nn.learn([0.0 if labels[image] != i else 1.0 for i in range(len(guess))])
            if numguess == labels[image]:
                correct +=1
                epochCorrect += 1
            epoch += nn.cost
            #print(f"cost: {nn.cost}")
            if nn.batchCount == 0:
                aveCost = epoch/batch
                if graph:
                    epochList.append(aveCost)
                    epochPercentages.append(epochCorrect/batch)
                    graphing(epochList, epochPercentages)
                epoch = 0
                epochCorrect = 0
            print(f"dataset percentage: {(correct/(1+image))*100}%, image: {image}, run:{run}, cost per last epoch: {aveCost}, elapsed time: {timedelta(seconds=int(time())-startTime)}          ", end="\n")
        print("\n")
    return nn

def test(nn, images, labels):
    correct = 0
    for image in range(len(images)):
        guess = nn.guess(np.array(images[image])/255)
        numguess = np.where(guess == np.amax(guess))[0][0]
        if numguess == labels[image]:
            correct +=1
        print(f"dataset percentage: {(correct/(1+image))*100}%           ", end="\r")
    percentage = correct/len(images)
    return percentage

def getNetwork(path, learnRate, batch, loss, opt, hiddenLayers, input_size):
    if p.exists(path):
        print("Using previous found network\n")
        nn = network.readNetwork(path)
        nn.batch = batch
        nn.learnRate = learnRate
    else:
        nn = network(input_size, hiddenLayers[:-1], hiddenLayers[-1], learnRate=learnRate, bias=True, batch=batch, actFun="LeReLu", opt=opt, loss=loss)
    return nn


if __name__ == "__main__":
    if len(sys.argv) > 8:
        learnRate = float(sys.argv[1])
        batch = int(sys.argv[2])
        runs = int(sys.argv[3])
        loss = sys.argv[4]
        opt = sys.argv[5]
        io = sys.argv[6]
        graph = bool(int(sys.argv[7]))
        layers = list(map(lambda x: int(x, ), sys.argv[8].split(",")))
    else:
        learnRate = 0.1
        batch = 128
        runs = 10
        loss = "mse"
        opt = "gd"
        io = "../networks/mnist.obj"
        graph = False
        layers = [16,16,10]

    print(f"learnRate: {learnRate}")
    print(f"batch: {batch}")
    print(f"runs: {runs}")
    print(f"loss: {loss}")
    print(f"optimizer: {opt}")
    print(f"io: {io}")
    print(f"graph: {graph}")
    mndata = MNIST('./samples/numbers')
    trainData, trainLabels = mndata.load_training()
    #trainData = [[(random.random()*2)-1, (random.random()*2)-1] for i in range(1000)]
    #trainLabels = [int(i[0]-0.5>i[1] or i[0]+0.5<i[1]) for i in trainData]
    input_size = len(trainData[0])
    print(f"architecture: {input_size}, {layers}\n")

    convnn = getNetwork(io, learnRate, batch, loss,opt, layers, input_size)
    convnn = train(runs, convnn, trainData, trainLabels, batch, graph)
    convnn.writeNetwork(io)
    print("training done")
    print(" ")
    testData, testLabels = mndata.load_testing()
    #testData = [[random.random()*2-1, random.random()*2-1] for i in range(20)]
    #testLabels = [int(i[0]-0.5>i[1]or i[0]+0.5<i[1]) for i in testData]
    results = test(convnn, testData, testLabels)
    print(f"final percentage: {results}")
