from mnist import MNIST
import random
from src.network import network
import numpy as np
import sys

def train(runs, nn, images, labels):
    for run in range(runs):
        correct = 0
        for image in range(len(images)):
            guess = nn.guess(np.array(images[image])/255)
            numguess = np.where(guess == np.amax(guess))[0][0]
            nn.learn([0 if labels[image] != i else 1 for i in range(10)])
            if numguess == labels[image]:
                correct +=1
            print(f"dataset percentage: {correct/(1+image)}, image: {image}, run:{run}          ", end="\r")
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


if __name__ == "__main__":
    if len(sys.argv) > 1:
        learnRate = sys.argv[0]
        batch = sys.argv[1]
    else:
        learnRate = 0.1
        batch = 100
    mndata = MNIST('samples')
    trainImages, trainLabels = mndata.load_training()

    convnn = network(784, [16,16], 10, learnRate=learnRate, bias=True, batch=batch, actFun="LeReLu")
    convnn = train(10, convnn, trainImages, trainLabels)
    convnn.writeNetwork("./networks/mist")
    print("training done")
    print(" ")
    testImages, testLabels = mndata.load_testing()
    results = test(convnn, testImages, testLabels)
    print(f"final percentage: {results}")
