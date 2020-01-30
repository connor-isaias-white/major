import random
trainData = {
    [1,1,1]: 1,
    [1,0,1]: 1,
    [0,1,1]: 0,
    [0,0,1]: 0,
    [0,0,0]: 0,
}
testData = {
    [1,1,0]: 1,
    [0,1,0]: 0,
    [1,0,0]: 1,
}
first = random.randint(0, 3)

c1 = random.random()
c2= random.random()
c3 = random.random()
