# Activation functions
import numpy as np

# Sigmiod
def sig(x, a=1):
    y = np.exp(x+a)/(1 + np.exp(x+a))
    return y
# derivative of sigmoid
def dSig(x):
    y = sig(x)*(1-sig(x))
    return y

#reverse sigmoid
def rSig(y):
    x = np.log(y/(1-y))
    return x

# Hyperbolic Tangent
def tanh(x):
    y = (1-np.exp(-2*x))/(1+np.exp(-2*x))
    return y

# Leaky Rectified Linear units
def LeReLu(x, a):
    if type(x)== np.ndarray:
        y = []
        for i in x:
            if i<0:
                i = i*a
            else:
                i=i
            y.append(i)
        y = np.resize(y, x.shape)
    else:
        if x<0:
            y=x
        else:
            y=a*x
    return y

# derivative of leaky relu
def dLeReLu(x, a):
    if x<0:
        y=a
    else:
        y=1
    return y

# Rectified Linear units
def ReLu(x):
    if x>0:
        y=x
    else:
        y=0
    return y

# Binary Threshold
def bi(x):
    if x>0:
        y=1
    else:
        y=0
    return y

# converts a range of numbers to positive
def pos(x, a):
    if type == int:
        y=(x+a)/2
    else:
        y=x
        for i in range(len(y)):
            y[i] = (y[i]+a)/2
    return y
# Softmax where x is an array of outputs
def softmax(x):
    #y = [(np.exp(j)/sum(list(map(np.exp,x))))[0] for j in x]
    a = np.exp(x)
    b= np.sum(np.exp(x))
    if b == 0:
        print("\ndivision by 0 error")
        print(x)
        print(np.exp(x))
        print(b)
    y = np.divide(a,b, out=np.zeros_like(a), where=b!=0)
    return y
