import random
import math

config = {
    'layers': 2,
    'neuroninlayer': [3, 1],
    'initinputLength': 4,
}

class neuron:

    def __init__(self, pos, inputLength):
        self.bias = random.randint(-6, 6)
        self.pos = pos
        self.weights = [random.randint(-6, 6) for i in range(inputLength)]

    def value(self, layer):
        val = self.bias
        numPrev = len(layer)
        val = self.bias
        for neral in range(len(layer)):
            weight = self.weights[neral]
            val += weight*layer[neral]
        self.val = self.sig(val)


    def sig(self, x):
        y = 1/(1+math.exp(-x))
        return y

def train():
    perfectNotFount = True
    run = 0
    while perfectNotFount:
        layers = []
        for hiddenlayer in range(config['layers']):
            layer = []
            for neuro in range(config['neuroninlayer'][hiddenlayer]):
                if hiddenlayer != 0:
                    inputLength = config['neuroninlayer'][hiddenlayer-1]
                else:
                    inputLength = config['initinputLength']
                layer.append(neuron(neuro,inputLength))
            layers.append(layer)

        percent = network(trainData, layers)
        if percent == 100 or percent ==0:
            print(f'correct: {percent}%, after {run} tries')
            perfectNotFount = False
            return layers
        run += 1

def network(datas, layers):
    score = 0
    for data in datas:
        guess = putInNetwork(data[0], layers)
        if round(guess[0]) == data[1]:
            score += 1
    percent = round(score/len(datas)*100)
    return percent

def putInNetwork(input, layers):
    for layer in layers:
        output = []
        for nero in layer:
            nero.value(input)
            output.append(nero.val)
        input = output
    return output


def test(best):
    final = network(trainData, best)
    print(f"testing score: {final}%")
    return final

def createData():
    length = config["initinputLength"]
    testData = []
    trainData = []
    for i in range(2**length):
        num = bin(i)[2:]
        datavalue = [0 for i in range(length-len(str(num)))]
        for i in str(num):
            datavalue.append(int(i))

        ans = 0
        for binary in range(length-1):
            if datavalue[binary+1] == datavalue[binary] and datavalue[binary] == 1:
                ans = 1
        if random.random() > 0.80:
            testData.append([datavalue, ans])
        else:
            trainData.append([datavalue, ans])
    return trainData, testData


if __name__ == "__main__":
    trainData, testData = createData()

    best = train()
    if best != 0:
        final = test(best)

        if final == 100 or final == 0:
            print(f"input {config['initinputLength']} 1s or 0s seperated by commas and the network will tell if 2 1s are ajacent")
            manData = input("> ")
            while manData:
                manData = manData.replace(" ", '').split(",")
                data = [int(i) for i in manData]
                output = round(putInNetwork(data, best)[0])
                if output == final/100:
                    print("2 at least adjacent 1s")
                else:
                    print("No adjacent values")
                manData = input("> ")
