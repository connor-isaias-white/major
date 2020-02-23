import random
import math
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

config = {
        "size":[5,5],
    }

class perceptron:
    def __init__(self, learningRate, trainData):
        self.weights = [random.random(), random.random()]
        self.bias = 0
        self.learningRate = learningRate
        self.trainData = trainData
    def sig(self, x):
        y = 1/(1+math.exp(-x))
        return y

    def learn(self, guess, point):
        #print(self.weights)
        ans = point[1]
        #print(ans, guess)
        error = ans - guess
        for i in range(len(self.weights)):
            self.weights[i] += error*point[0][i] * self.learningRate
        self.bias += error *self.learningRate

    def guess(self, point):
        output = 0
        for i in range(len(point[0])):
            output += self.weights[i]*(point[0][i])
        output = self.sig(output+self.bias)
        if round(output) != point[1]:
            self.learn(output, point)
        return (round(output) == point[1])

def createData(num):
    data = []
    grad = random.uniform(-10,10)
    interspt = random.uniform(-1, 1)
    for point in range(num):
        x = random.uniform(-1,1)
        y = random.uniform(-1,1)
        #if y <= grad*x+interspt:
        if y <= x**2:
            val = 1
        else:
            val = 0
        data.append([[x,y], val])
    return data

def train():
    total = 0
    for point in percy.trainData:
        correct = percy.guess(point)
        if correct:
            total += 1
    b = percy.bias#-(int(percy.bias>0)*2-1)
    line = ax.plot([-config["size"][0],config["size"][0]],[-config["size"][0]*(-1*percy.weights[0]+b)/percy.weights[1],-config["size"][0]*(1*percy.weights[0]+b)/percy.weights[1]], c=[0,0,1])
    return line, total/len(percy.trainData)

def draw(data):
    line = ax.plot([-config["size"][0],config["size"][0]], [0.75, -0.25])
    ax.scatter([i[0][0]*config["size"][0] for i in data], [i[0][1]*config["size"][1] for i in data], c=[[0,i[1],0]for i in data])
    ax.set_xlabel("")
    ani = animation.FuncAnimation(fig, changeLine,)# blit=True)
    plt.show()

def changeLine(frame):
    line, percent = train()
    title = ax.set_xlabel(f'correct: {percent},  bias: {percy.bias},\n weights: {percy.weights}, intersept: {-percy.bias/percy.weights[1]}')
    ax.lines = ax.lines[1:]
    return line, title

if __name__ == "__main__":
    trainData = createData(255)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    percy = perceptron(0.1, trainData)
    draw(trainData)

