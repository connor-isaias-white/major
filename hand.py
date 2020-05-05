from mnist.loader import MNIST
import random
from src.network import network
import numpy as np
import sys
import os

def train(runs, nn, images, labels):
    for run in range(runs):
        correct = 0
        for image in range(len(images)):
            guess = nn.guess(np.array(images[image])/255)
            #print(guess)
            numguess = np.where(guess == np.amax(guess))[0][0]
            #print(numguess)
            #print(labels[image])
            nn.learn([0 if labels[image] != i else 1 for i in range(10)])
            if numguess == labels[image]:
                correct +=1
            print(f"dataset percentage: {correct/(1+image)}, image: {image}, run:{run}          ", end="\r")
            #print("")
    return nn

def test(nn, images, labels):
    correct = 0
    for image in range(len(images)):
        guess = nn.guess(np.array(images[image])/255)
        numguess = np.where(guess == np.amax(guess))[0][0]
        if numguess == labels[image]:
            correct +=1
        print(f"dataset percentage: {correct/(1+image)}         ", end="\r")
    percentage = correct/len(images)
    return percentage

def getNetwork(path, learnRate, batch):
    if os.path.exists(path):
        print("Using previous found network\n")
        nn = network.readNetwork(path)
        nn.batch = batch
        nn.learnRate = learnRate
    else:
        nn = network(784, [16,16], 10, learnRate=learnRate, bias=True, batch=batch, actFun="LeReLu")
    return nn


if __name__ == "__main__":
    if len(sys.argv) > 3:
        learnRate = float(sys.argv[1])
        batch = int(sys.argv[2])
        runs = int(sys.argv[3])
    else:
        learnRate = 0.1
        batch = 128
        runs = 10
    print(f"learnRate: {learnRate}")
    print(f"batch: {batch}\n")
    mndata = MNIST('samples')
    trainImages, trainLabels = mndata.load_training()

    convnn = getNetwork("./networks/mist.obj", learnRate, batch)
    convnn = train(runs, convnn, trainImages, trainLabels)
    convnn.writeNetwork("./networks/mist.obj")
    print("training done")
    print(" ")
    testImages, testLabels = mndata.load_testing()
    results = test(convnn, testImages, testLabels)
    print(f"final percentage: {results}")
