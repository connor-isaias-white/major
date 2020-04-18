from mnist import MNIST
import random
from src.network import network
import numpy as np

def train():
    run = 0
    while True:
        correct = 0
        run += 1
        for image in range(len(images)):
            guess = nn.guess(np.array(images[image])/255)
            print(guess)
            print(f"answer: {labels[image]}")
            highest = 0
            for i in range(len(guess)):
                if guess[i] > highest:
                    highest = guess[i]
                    numguess = i
            nn.learn([0 if labels[image] != i else 1 for i in range(10)])
            if numguess == labels[image]:
                print("correct")
                correct +=1
            print(f"dataset percentage: {correct/(1+image)}, image: {image}, run:{run}")


if __name__ == "__main__":
    mndata = MNIST('samples')
    images, labels = mndata.load_training()

    nn = network(784, [16,16], 10, learnRate=0.1, bias=True, batch=100, actFun="sig")
    train()
