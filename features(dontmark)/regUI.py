import os
import sys
sys.path.append("..")
from tkinter import *
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageOps
import scipy.ndimage as ndi
from src.network import network

def clear():
    ''' clear the revtangle and image '''
    cv.delete("all")
    draw.rectangle([(0, 0), image1.size], fill='black')
    data = []
    labels = []

def activate_paint(e):
    ''' draw dot '''
    width = 3
    x, y = e.x,e.y
    data.append([x/300,y/300])
    labels.append(int(colour.get() == "blue"))
    cv.create_oval(x-width, y-width, x+width, y+width, outline=colour.get(), fill=colour.get())
    nn.batch = len(data)
    netGuess(data)

def netGuess(data):
    ''' feed the data through the network to output guess '''
    percent = 0
    while percent != 1:
        total = 0
        for point in range(len(data)):
            print(f"Point: {point}, data = {data[point]}")
            guess = nn.guess(np.array(data[point]))
            print(guess)
            numguess = np.where(guess == np.amax(guess))[0][0]
            if numguess == labels[point]:
                total += 1
            nn.learn([0.0 if labels[point] != i else 1.0 for i in range(len(guess))])
        percent = total/len(data)
        print(percent)

    rounded = round(np.amax(guess) * 100,2)
    info['text'] = "Guess: "+str(numguess)+ "\nCertainty: "+str(rounded)+"%"

def reg_page():
    global colour
    colour = StringVar()
    title['text'] = "Regression Network"
    image_number = 0
    cv.bind('<1>', activate_paint)
    colour_select_red = Radiobutton(root, variable=colour, value="red", text="Red")
    colour_select_blue = Radiobutton(root, variable=colour, value="blue", text="Blue")
    info.pack()
    cv.pack(expand=False, fill=None, side="top")
    colour_select_red.select()
    colour_select_red.pack()
    colour_select_blue.pack()
    btn_clear.pack()

if __name__ == "__main__":
    # get data
    data = []
    labels = []
    nn = network(2,[3], 2, learnRate=0.1, bias=True, batch=1, actFun="LeReLu", opt="gd", loss="mse")

    root = Tk()
    root.resizable(False, False)
    root.geometry("550x550")
    title = Label(root, text="Test Network", height=2, font=("./font/rb.ttf", 40))
    title.pack()

    info = Label(root, justify='left', text="Guess: 0\nCertainty: 00.00%")
    cv = Canvas(root, width=300, height=300, bg='black')
    btn_clear = Button(text="clear", command=clear)
    image1 = Image.new('L', (300, 300), 'black')
    draw = ImageDraw.Draw(image1)
    reg_page()
    root.mainloop()
