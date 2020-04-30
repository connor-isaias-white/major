from tkinter import *
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageOps
import os
from src.network import network

def getNetwok(path):
    if not os.path.exists(path):
        exec(open("hand.py").read())
    nn = network.readNetwork(path)
    return nn

def imgData():
    global image1
    img = image1
    img = img.convert("L")
    extImg = img.convert('1', dither=Image.NONE)
    if extImg.getcolors()[0][0]<extImg.getcolors()[1][0]:
        img = ImageOps.invert(img)
    if img.size != (28,28):
        img = img.resize((28,28), Image.LANCZOS)
    img = ImageEnhance.Contrast(img)
    img = img.enhance(1.5)
    data = np.array(img.getdata())
    data = data/255
    netGuess(data)
    cv.delete("all")
    draw.rectangle([(0, 0), image1.size], fill='black')
    return data


def activate_paint(e):
    global lastx, lasty
    cv.bind('<B1-Motion>', paint)
    lastx, lasty = e.x, e.y

def paint(e):
    global lastx, lasty
    x, y = e.x, e.y
    width = 2
    cv.create_line((lastx, lasty, x, y), fill="white", width=5)
    cv.create_oval(x-width, y-width, x+width, y+width,outline="white", fill="white")
    #  --- PIL
    draw.line((lastx, lasty, x, y), fill='white', width=5)
    draw.ellipse([(x-width, y-width),(x+width, y+width)], outline='white', fill='white')
    lastx, lasty = x, y

def netGuess(data):
    guess = net.guess(data)
    numguess = np.where(guess == np.amax(guess))[0][0]
    print(numguess)
    answer = int(input("Input the number that it was meant to be: "))
    if numguess == answer:
        net.batch += 1
    else:
        net.batch = 1
    net.learn([int(i==answer) for i in range(10)])

if __name__ == "__main__":
    net = getNetwok("networks/mist.obj")
    net.batch = 1
    net.learnRate = 0.001

    root = Tk()
    lastx, lasty = None, None
    image_number = 0
    cv = Canvas(root, width=122, height=122, bg='black')
    image1 = Image.new('L', (122, 122), 'black')
    draw = ImageDraw.Draw(image1)
    cv.bind('<1>', activate_paint)
    cv.pack(expand=YES, fill=BOTH)
    btn_save = Button(text="save", command=imgData)
    btn_save.pack()

    root.mainloop()

