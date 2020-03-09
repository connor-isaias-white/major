# Activation functions
import numpy as np

# Sigmiod
def sig(x):
    y =1/(np.exp(-x)+1)
    return y

def dSig(x):
    y = sig(x)*(1-sig(x))
    return y

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
