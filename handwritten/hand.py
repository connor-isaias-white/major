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

def graphing(graphData):
    plt.close()
    plt.ion()
    plt.show()
    plt.plot(range(len(graphData)), graphData)
    plt.draw()
    plt.pause(0.00001)


def train(runs, nn, images, labels, batch, graph):
    startTime = int(time())
    epoch = 0
    epochList = []
    aveCost = 0
    for run in range(runs):
        correct = 0
        for image in range(len(images)):
            guess = nn.guess(np.array(images[image])/255)
            #print(guess)
            numguess = np.where(guess == np.amax(guess))[0][0]
            #print(numguess)
            #print(labels[image])
            nn.learn([0 if labels[image] != i else 1.0 for i in range(10)])
            if numguess == labels[image]:
                correct +=1
            epoch += nn.cost
            if nn.batchCount == 0:
                    aveCost = epoch/batch
                    epoch = 0
                    epochList.append(aveCost)
                    if graph:
                        graphing(epochList)
            print(f"dataset percentage: {(correct/(1+image))*100}%, image: {image}, run:{run}, cost per last epoch: {aveCost}, elapsed time: {timedelta(seconds=int(time())-startTime)}          ", end="\r")
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

def getNetwork(path, learnRate, batch, loss, opt, hiddenLayers):
    if p.exists(path):
        print("Using previous found network\n")
        nn = network.readNetwork(path)
        nn.batch = batch
        nn.learnRate = learnRate
    else:
        nn = network(784, hiddenLayers, 10, learnRate=learnRate, bias=True, batch=batch, actFun="LeReLu", opt=opt, loss=loss)
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
        hiddenLayers = list(map(lambda x: int(x, ), sys.argv[8].split(",")))
    else:
        learnRate = 0.1
        batch = 128
        runs = 10
        loss = "mse"
        opt = "gd"
        io = "./neteorks/mnist.obj"
        graph = False
        hiddenLayers = [16,16]

    print(f"learnRate: {learnRate}")
    print(f"batch: {batch}")
    print(f"runs: {runs}")
    print(f"loss: {loss}")
    print(f"optimizer: {opt}")
    print(f"io: {io}")
    print(f"graph: {graph}\n")
    print(f"architecture: 784, {hiddenLayers}, 10")
    mndata = MNIST('./samples')
    trainImages, trainLabels = mndata.load_training()

    convnn = getNetwork(io, learnRate, batch, loss,opt, hiddenLayers)
    convnn = train(runs, convnn, trainImages, trainLabels, batch, graph)
    convnn.writeNetwork(io)
    print("training done")
    print(" ")
    testImages, testLabels = mndata.load_testing()
    results = test(convnn, testImages, testLabels)
    print(f"final percentage: {results}")
