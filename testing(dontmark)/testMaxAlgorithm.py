import time
import random


def tester(function):
    methodTotal = 0
    for i in range(1000):
        newList = []
        for j in range(10):
            newList.append(random.random())
        start = time.time()
        function(newList)
        methodTotal += time.time()- start
    return methodTotal/1000

def method2(guess):
    highest = 0
    for i in range(len(guess)):
        if guess[i] > highest:
            highest = guess[i]
            numguess = i

method1per = tester(lambda x: x.index(max(x)))
method2per = tester(lambda x: method2(x))
print(f"method1: {method1per}")
print(f"method2: {method2per}")
