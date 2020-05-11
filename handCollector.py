from tkinter import *
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageOps
import os
import pickle
import random

''' a program for collecting hand data '''
motivationalMessages = ["Keep going!", "You can do it!", "You are on a roll!", "Great work!", "Keep it up!", "Thats the spirit!", "Come on!", "a little harder now!", \
        "You are doing great!", "Don't give up now", "Nice moves", "All right!", "Nice!", "Slam dunk!", "Alright!", "Amazing!", "Another one", "You did it!", "Unbelivable!",\
        "Great approach!", "Hole in one!", "Nice on!", "Nice Shot!", "Knockout!", "Thats the Game!", "Nice Throw!", "Great Shot!", "Nice Spare!", "Perfect", \
        "Double Play!", "Its Out of the park!", "Home run!", "Exelent!", "Good!", "Great!", "Ok!", "Challenge Round!", "All for the win!", "Great Air!", "Wow!"]

def imgData():
    ''' interperates and saves the data drawn'''
    global image1
    global ans
    img = image1
    img = img.convert("L")
    extImg = img.convert('1', dither=Image.NONE)
    if extImg.getcolors()[0][0]<extImg.getcolors()[1][0]:
        img = ImageOps.invert(img)
    if img.size != (28,28):
        img = img.resize((28,28), Image.LANCZOS)
    data = np.array(img.getdata())
    data = data/255
    if not os.path.exists("savedData.p"):
        savedData = np.array([])
    else:
        with open("savedData.p", "rb") as f:
            savedData = pickle.load(f)
    savedData = np.append(savedData, [data, ans])
    with open("savedData.p", "wb") as f:
        pickle.dump(savedData, f)
    reset()

def clear():
    cv.delete("all")
    draw.rectangle([(0, 0), image1.size], fill='black')

def reset():
    ''' Resets screen and number '''
    global ans
    ans = random.randint(0,9)
    clear()
    if random.random() < 0.15:
        print(motivationalMessages[random.randint(0, len(motivationalMessages)-1)])
    print(f"Draw a \"{ans}\"", end = '\r')

def activate_paint(e):
    ''' turns paint on while mouse is down '''
    global lastx, lasty
    cv.bind('<B1-Motion>', paint)
    lastx, lasty = e.x, e.y

def paint(e):
    ''' fills the areas being painted '''
    global lastx, lasty
    x, y = e.x, e.y
    width = 2
    cv.create_line((lastx, lasty, x, y), fill="white", width=5)
    cv.create_oval(x-width, y-width, x+width, y+width,outline="white", fill="white")
    #  --- PIL
    draw.line((lastx, lasty, x, y), fill='white', width=5)
    draw.ellipse([(x-width, y-width),(x+width, y+width)], outline='white', fill='white')
    lastx, lasty = x, y

if __name__ == "__main__":
    ''' setup '''
    root = Tk()
    lastx, lasty = None, None
    image_number = 0
    cv = Canvas(root, width=122, height=122, bg='black')
    image1 = Image.new('L', (122, 122), 'black')
    draw = ImageDraw.Draw(image1)
    cv.bind('<1>', activate_paint)
    cv.pack(expand=YES, fill=BOTH)
    btn_save = Button(text="Save", command=imgData)
    btn_save.pack()
    btn_clr = Button(text="Clear", command=clear)
    btn_clr.pack()
    ans = random.randint(0,9)
    print("\nTop button is to submit, Bottom button is to clear")
    print(f"Draw a \"{ans}\" then click the empty button below it")
    root.mainloop()
