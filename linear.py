from src.network import network
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import numpy as np
import src.actives as acv

config = {
        "size":[1,1,1],
    }

def createData(num):
    data = []
    grad = random.uniform(-10,10)
    interspt = random.uniform(-1, 1)
    for point in range(num):
        x = random.uniform(0,1)
        y = random.uniform(0,1)
        #z = random.uniform(-1,1)
        if y<x+0.25 and y > x-0.25:
        #if x+y+z >= 0:
            val = 1
        else:
            val = 0
        data.append([np.array([x,y]), val])
    return data

def train():
    running = True
    #while running:
    #for i in range(100):
    total = 0
    guesses = []
    for point in trainData:
        guess = percy.guess(point[0])
        guesses.append(round(guess[0][0]) == point[1])
        #print(percy.matrixes)
        percy.learn(point[1])
        if round(guess[0][0]) == point[1]:
            total+= 1
    percent = total/len(trainData)
    print(f'percent: {percent}', end='\r')
    if percent == 1:
        running = False
    #line = ax.plot([0,1],[percy.guess(np.array([0,-1]))[0][0],percy.guess(np.array([0,1]))[0][0]],  c=[0,0,1])
    return percent, guesses
        #print(percy.matrixes)

def draw(data):
    #ax.plot_wireframe(np.array([-5,5]),np.array([-5,5]),np.array([[0,-10],[10,0]]))
    #line = ax.plot([0, 1], [0,1])
    scatter = ax.scatter([i[0][0] for i in data], [i[0][1] for i in data], c=[[0.5,0,i[1]]for i in data])
    ax.set_xlabel("")
    ani = animation.FuncAnimation(fig, changeLine)# blit=True)
    plt.show()

def changeLine(frame):
    percent, guesses = train()
    #print(guesses)
    title = ax.set_xlabel(f'correct: {percent}')
    scatter = ax.scatter([i[0][0] for i in trainData], [i[0][1] for i in trainData], c=[[0.5,0,i[1]]for i in trainData], edgecolors=[[0,i,0] for i in guesses], linewidths=1.5)
    #ax.lines = ax.lines[1:]
    return title, scatter#, line

if __name__ == "__main__":
    trainData = createData(100)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    percy = network(len(trainData[0][0]),[3],1,batch =100, learnRate=1, actFun="LeReLu", bias=True)
    draw(trainData)
