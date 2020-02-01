import random
import math
trainData = [
    [[1,1,1,1], 1],
    [[1,1,1,0], 1],
    [[1,1,0,1], 1],
    [[1,0,1,1], 1],
    [[1,0,1,0], 0],
    [[1,0,0,1], 0],
    [[1,0,0,0], 0],
    [[0,1,1,0], 1],
    [[0,1,0,1], 0],
    [[0,1,0,0], 0],
    [[0,0,1,1], 1],
    [[0,0,0,0], 0],
]
testData = [
    [[1,1,0,0], 1],
    [[0,1,1,1], 1],
    [[0,0,1,0], 0],
    [[0,0,0,1], 0],

]
config = {
    'layers': 2,
    'neuroninlayer': [3, 1],
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
    for run in range (20000):
        layers = []
        for hiddenlayer in range(config['layers']):
            layer = []
            for neuro in range(config['neuroninlayer'][hiddenlayer]):
                if hiddenlayer != 0:
                    inputLength = config['neuroninlayer'][hiddenlayer-1]
                else:
                    inputLength = len(trainData[0][0])
                layer.append(neuron(neuro,inputLength))
            layers.append(layer)

        percent = network(trainData, layers)
        if percent == 100:
            print(f'correct: {percent}%')
            return layers
    return 0

def network(datas, layers):
    score = 0
    for data in datas:
        input = data[0]
        for layer in layers:
            output = []
            for nero in layer:
                nero.value(input)
                output.append(nero.val)
            input = output
        if round(output[0]) == data[1]:
            score += 1
    percent = round(score/len(datas)*100)
    return percent

def test(best):
    final = network(trainData, best)
    print(f"testing score: {final}%")

if __name__ == "__main__":
    best = train()
    if best != 0:
        test(best)
