import os
import sys
sys.path.append("..")
from tkinter import *
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageOps
import scipy.ndimage as ndi
from src.network import network


def getNetwork(path):
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
    if img.size != (20,20):
        img = img.resize((20,20), Image.LANCZOS)
    data = np.array(img.getdata())
    data = data/255
    centre = ndi.measurements.center_of_mass(np.reshape(data, (20,20)))
    img2 = Image.new("L", (28,28), 0)
    img2.paste(img, (int(round(14-centre[1])), int(round(14-centre[0]))))
    data2 = np.array(img2.getdata())
    data2 = data2/255
    netGuess(data2)
    return data

def clear():
    cv.delete("all")
    draw.rectangle([(0, 0), image1.size], fill='black')


def activate_paint(e):
    global lastx, lasty
    cv.bind('<B1-Motion>', paint)
    lastx, lasty = e.x, e.y

def paint(e):
    global lastx, lasty
    x, y = e.x, e.y
    width = 4
    cv.create_line((lastx, lasty, x, y), fill="white", width=10)
    cv.create_oval(x-width, y-width, x+width, y+width,outline="white", fill="white")
    #  --- PIL
    draw.line((lastx, lasty, x, y), fill='white', width=10)
    draw.ellipse([(x-width, y-width),(x+width, y+width)], outline='white', fill='white')
    lastx, lasty = x, y
    imgData()

def netGuess(data):
    guess = net.guess(data)
    numguess = np.where(guess == np.amax(guess))[0][0]
    print(f"Guess: {numguess} Certainty: {round(np.amax(guess) * 100,2)}%", end='\r')
    #answer = int(input("Input the number that it was meant to be: "))
    #if numguess == answer:
    #    net.batch += 1
    #else:
    #    net.batch = 1
    #net.learn([int(i==answer) for i in range(10)])

if __name__ == "__main__":
    net = getNetwork("../networks/mist.obj")
    net.batch = 1
    net.learnRate = 0.001

    root = Tk()
    lastx, lasty = None, None
    image_number = 0
    cv = Canvas(root, width=120, height=120, bg='black')
    image1 = Image.new('L', (120, 120), 'black')
    draw = ImageDraw.Draw(image1)
    cv.bind('<1>', activate_paint)
    cv.pack(expand=YES, fill=BOTH)
    btn_save = Button(text="clear", command=clear)
    btn_save.pack()

    root.mainloop()

