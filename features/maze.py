from tkinter import *
import random
import time
import os
import sys
sys.path.append("..")
import numpy as np
from src.gen import gen

def clear():
    ''' clear the revtangle and image '''
    cv.delete("all")

def maze_page():
    title['text'] = "Maze Network"
    image_number = 0
    info.pack()
    cv.pack(expand=False, fill=None, side="top")
    btn_clear.pack()
    btn_start.pack()

def show_gen(first):
    width = 1
    total_alive = 0
    for i in generation.brains:
        if i.alive:
            total_alive += 1
            if first:
                if i == generation.brains[0]:
                    outline = "yellow"
                    width = 2
                else:
                    outline = i.colour
                    width = 1
                i.canvasobj = cv.create_oval(i.x -width, i.y-width, i.x+width, i.y+width, fill=i.colour, outline=outline)
            else:
                cv.move(i.canvasobj, i.xmov, i.ymov)
    if random.random()<1 or i.itter == 199:
        cv.update()
    return total_alive

def run():
    while True:
        for i in range(generation.instructions):
            generation.move()
            #clear()
            total_alive = show_gen(False)
            print(total_alive)
            if not total_alive:
                break
        generation.new()
        clear()
        make_goal(250,250)
        show_gen(True)

def make_goal(x,y):
    generation.goal(x,y)
    width = 3
    cv.create_oval(x-width, y-width, x+width, y+width, fill="yellow", outline="yellow")

if __name__ == "__main__":
    # get data
    root = Tk()
    root.resizable(False, False)
    root.geometry("550x550")
    title = Label(root, text="Test Network", height=2, font=("./font/rb.ttf", 40))
    title.pack()

    generation = gen(200, start=[50,50])
    generation.create_boundry(0, 0, 300, 300, out=True)
    generation.populate(100)

    info = Label(root, justify='left', text="Guess: 0\nCertainty: 00.00%")
    cv = Canvas(root, width=300, height=300, bg='black')
    btn_clear = Button(text="clear", command=clear)
    btn_start = Button(text="start", command=run)
    show_gen(True)
    maze_page()
    make_goal(250, 250)
    root.mainloop()
