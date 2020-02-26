from src.network import network
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import numpy as np

config = {
        "size":[5,5],
    }

def createData(num):
    data = []
    grad = random.uniform(-10,10)
    interspt = random.uniform(-1, 1)
    for point in range(num):
        x = random.uniform(-1,1)
        y = random.uniform(-1,1)
        #if y <= grad*x+interspt:
        if y <= x:
            val = 1
        else:
            val = 0
        data.append([[x,y], val])
    return data

def train():
    total = 0
    while True:
        for point in trainData:
            guess = percy.guess(np.array(point[0]))
            print(guess)
            if round(guess) == point[1]:
                percy.learn(point[1], point[0])
                total += 1
        print(total/len(trainData))
    '''    if correct:
            total += 1
    b = percy.bias#-(int(percy.bias>0)*2-1)
    line = ax.plot([-config["size"][0],config["size"][0]],[-config["size"][0]*(-1*percy.weights[0]+b)/percy.weights[1],-config["size"][0]*(1*percy.weights[0]+b)/percy.weights[1]], c=[0,0,1])
    return line, total/len(percy.trainData)'''

def draw(data):
    line = ax.plot([-config["size"][0],config["size"][0]], [0.75, -0.25])
    ax.scatter([i[0][0]*config["size"][0] for i in data], [i[0][1]*config["size"][1] for i in data], c=[[0,i[1],0]for i in data])
    ax.set_xlabel("")
    ani = animation.FuncAnimation(fig, changeLine,)# blit=True)
    plt.show()

if __name__ == "__main__":
    trainData = createData(255)
    percy = network(2,[],1)
    train()

