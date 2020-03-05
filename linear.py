from src.network import network
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import numpy as np
import src.actives as acv

config = {
        "size":[5,5,5],
    }

def createData(num):
    data = []
    grad = random.uniform(-10,10)
    interspt = random.uniform(-1, 1)
    for point in range(num):
        x = random.uniform(-1,1)
        y = random.uniform(-1,1)
        #z = random.uniform(-1,1)
        if y <= grad*x+0.5:# and y>=grad*x-0.5:
        #if x+y+z >= 0:
            val = 1
        else:
            val = 0
        data.append([np.array([x,y]), val])
    return data

def train():
    running = True
    while running:
        total = 0
        for point in trainData:
            guess = percy.guess(point[0])
            if acv.bi(guess[0][0]) != point[1]:
                percy.learn(point[1])
            else:
                total+= 1
        percent = total/len(trainData)
        print(f"{percent}  ", end="\r")
        if percent == 1: 
            running = False
    print(percy.matrixes)


if __name__ == "__main__":
    trainData = createData(255)
    percy = network(len(trainData[0][0])-1,[],1, learnRate=0.5)
    train()

