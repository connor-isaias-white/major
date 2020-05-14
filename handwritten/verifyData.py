from PIL import Image
from pickle import load:

def makeImg(dataz):
    img = Image.new("L", (28, 28), color="black")
    formed = np.resize(datz, (28,28)).tolist()
    for x in range(len(dataz)):
        for y in range(x):
            img.putpixel((x,y), formed[x],[y])
