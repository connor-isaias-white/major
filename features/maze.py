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
    cv.pack(expand=False, fill=None, side="top")
    btn_start.pack(side="bottom", pady=20)
    randomness.pack(side="left", padx=60, anchor="n")
    speed.pack(side="left", padx=0, anchor="n")
    pop_num.pack(side="left", padx=60, anchor="n")

def activate_paint(e):
    ''' start keydown '''
    global lastx, lasty
    cv.bind('<ButtonRelease-1>', paint)
    lastx, lasty = e.x, e.y

def paint(e):
    global lastx, lasty
    cv.create_rectangle(lastx,lasty, e.x, e.y, fill="white")
    if e.x > lastx:
        x1, x2 = lastx, e.x
    else:
        x1, x2 = e.x, lastx
    if e.y > lasty:
        y1, y2 = lasty, e.y
    else:
        y1, y2 = e.y, lasty
    generation.create_boundry(x1, y1, x2, y2)

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
    if i.itter % speed.get() ==0 or i.itter == generation.instructions - 1:
        cv.update()
    return total_alive

def run():
    while True:
        for i in range(generation.instructions):
            generation.move()
            #clear()
            total_alive = show_gen(False)
            if not total_alive:
                break
            if i == generation.instructions - 1:
                for brain in generation.brains:
                    cv.delete(brain.canvasobj)
        generation.mutation_rate = randomness.get()
        generation.population = pop_num.get()
        generation.new()
        make_goal(250,250)
        show_gen(True)

def make_goal(x,y):
    width = 3
    generation.goal(x,y, width)
    cv.create_oval(x-width, y-width, x+width, y+width, fill="yellow", outline="yellow")

if __name__ == "__main__":
    # get data
    root = Tk()
    root.resizable(False, False)
    root.geometry("550x550")
    title = Label(root, text="Test Network", height=2, font=("futura", 40))
    title.pack()

    generation = gen(200, start=[50,50])
    generation.create_boundry(0, 0, 300, 300, out=True)
    generation.populate(100)

    cv = Canvas(root, width=300, height=300, bg='black')
    cv.bind('<1>', activate_paint)
    btn_start = Button(text="start", command=run, height=2, width=30)
    randomness = Scale(root, from_=0, to=1, orient=HORIZONTAL, resolution=0.01, label="Randomness")
    randomness.set(0.1)
    pop_num = Scale(root, from_=2, to=1000, orient=HORIZONTAL, label="Population")
    pop_num.set(100)
    speed = Scale(root, from_=1, to=20, orient=HORIZONTAL, label="Speed")
    speed.set(1)
    show_gen(True)
    maze_page()
    make_goal(250, 250)
    root.mainloop()
