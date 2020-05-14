import sys
sys.path.append("..")
from mnist.loader import MNIST
import random
from src.network import network
import numpy as np
import os

def train(runs, nn, images, labels, batch):
    epoch = 0
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
            print(f"dataset percentage: {correct/(1+image)}, image: {image}, run:{run}, cost: {nn.cost}, per last epoch: {aveCost}          ", end="\r")
    return nn

def test(nn, images, labels):
    correct = 0
    for image in range(len(images)):
        guess = nn.guess(np.array(images[image])/255)
        numguess = np.where(guess == np.amax(guess))[0][0]
        if numguess == labels[image]:
            correct +=1
        print(f"dataset percentage: {correct/(1+image)}           ", end="\r")
    percentage = correct/len(images)
    return percentage

def getNetwork(path, learnRate, batch, loss, opt):
    if os.path.exists(path):
        print("Using previous found network\n")
        nn = network.readNetwork(path)
        nn.batch = batch
        nn.learnRate = learnRate
    else:
        nn = network(784, [16,16], 10, learnRate=learnRate, bias=True, batch=batch, actFun="LeReLu", opt=opt, loss=loss)
    return nn


if __name__ == "__main__":
    random.seed(3)
    if len(sys.argv) > 5:
        learnRate = float(sys.argv[1])
        batch = int(sys.argv[2])
        runs = int(sys.argv[3])
        loss = sys.argv[4]
        opt = sys.argv[5]

    else:
        learnRate = 0.01
        batch = 128
        runs = 10
        loss = "mse"
        opt = "gd"
    print(f"learnRate: {learnRate}")
    print(f"batch: {batch}")
    print(f"loss: {loss}")
    print(f"optimizer: {opt}\n")
    mndata = MNIST('./samples')
    trainImages, trainLabels = mndata.load_training()

    convnn = getNetwork("./networks/mist2.obj", learnRate, batch, loss,opt)
    convnn = train(runs, convnn, trainImages, trainLabels, batch)
    convnn.writeNetwork("./networks/mist2.obj")
    print("training done")
    print(" ")
    testImages, testLabels = mndata.load_testing()
    results = test(convnn, testImages, testLabels)
    print(f"final percentage: {results}")
