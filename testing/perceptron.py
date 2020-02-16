import random
import math
import tkinter as tk

config = {
        "width": 255,
        "height": 255,
    }

class perceptron:
    def __init__(self, learningRate):
        self.weights = [random.random(), random.random()]
        self.bias = random.random()
        self.learningRate = learningRate
    
    def sig(self, x):
        y = 1/(1+math.exp(-x))
        return y

    def learn(self, guess, point):
        ans = point[1]
        error = ans - guess
        for i in range(len(self.weights)):
            self.weights[i] += error*point[0][i] * self.learningRate

    def guess(self, point):
        output = self.bias
        for i in range(len(point[0])):
            output += self.weights[i]*point[0][i]
        output = round(self.sig(output))
        if output != point[1]:
            self.learn(output, point)
        return (output == point[1])

def createData(num):
    data = []
    for point in range(num):
        x = random.random()
        y = random.random()
        if y > x:
            val = 1
        else:
            val = 0
        data.append([[x,y], val])
    return data

def train(trainData):
    percy = perceptron(0.1)
    for i in range(100):
        total = 0
        for point in trainData:
            correct = percy.guess(point)
            if correct:
                total += 1
        print(f"{total/len(trainData)}%")

def drawPoints(points):
    master = tk.Tk()
    w = tk.Canvas(master, width=config["width"], height=config["height"])
    w.pack()
    for point in points:
        circle(w, round(point[0][0]*config["width"]), round(point[0][1]*config["height"]), 5)
    tk.mainloop()

def circle(canvas, x,y,r):
    id = canvas.create_oval(x-r,y-r,x+r,y+r, fill="#000000")
    return id

if __name__ == "__main__":
    trainData = createData(255)
    drawPoints(trainData)
    # train(trainData)
