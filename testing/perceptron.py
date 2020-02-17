import random
import math
import tkinter as tk
import time

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

class screen:
    def __init__(self, points):
        self.width = config["width"]
        self.height = config["height"]
        master = tk.Tk()
        self.w =tk.Canvas(master, width=config["width"], height=config["height"]) 
        self.line= self.w.create_line(0,0,self.width,self.height)
        self.w.pack()
        self.points = points

    def circle(self, x,y,r, colour):
        self.w.create_oval(x-r,y-r,x+r,y+r, fill=colour)
    
    def update(self):
        self.w.update_idletasks()
        self.w.update()
    
    def drawPoints(self):
        for point in self.points:
            if point[1]==1:
                colour = "#00ff00"
            else:
                colour="#ff0000"
            self.circle(round(point[0][0]*config["width"]), round(point[0][1]*config["height"]), 3, colour)

    def drawLine(self, rise, run):
        #self.w.delete("all")
        #self.drawPoints()
        gradient = rise/run
        self.w.create_line(0,self.lineEquation(gradient, 0), self.width, self.lineEquation(gradient, self.width))
        #self.w.update()

    def lineEquation(self, m,x):
        y=m*x
        return y

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

def train(trainData, Screen):
    percy = perceptron(0.1)
    for i in range(10):
        total = 0
        for point in trainData:
            correct = percy.guess(point)
            if correct:
                total += 1
        Screen.update()
        Screen.drawLine(percy.weights[0], percy.weights[1])
        Screen.update()
        #time.sleep(1)
        #print(f"{total/len(trainData)}%")

if __name__ == "__main__":
    trainData = createData(255)
    Screen = screen(trainData)
    Screen.drawPoints()
    Screen.drawLine(1,2) 
    train(trainData, Screen)
