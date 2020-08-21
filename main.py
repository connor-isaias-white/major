from os import path as find_path
from tkinter import Scale, Canvas, Tk, Label, Button
from PIL import Image, ImageDraw, ImageOps
from scipy.ndimage import measurements
import numpy as np
from src.network import network
from src.gen import gen

def get_network(path):
    ''' locate and return network that will be used for guessing'''
    if not find_path.exists(path):
        exec(open("handwritten/hand.py").read())
    neural_network = network.readNetwork(path)
    return neural_network

def imgData():
    ''' convert the drawn image into a formated 28*28 array '''
    global image1
    img = image1
    img = img.convert("L")
    extImg = img.convert('1', dither=Image.NONE)
    if extImg.getcolors()[0][0] < extImg.getcolors()[1][0]:
        img = ImageOps.invert(img)
    if img.size != (20, 20):
        img = img.resize((20, 20), Image.LANCZOS)
    data = np.array(img.getdata())
    data = data/255
    centre = measurements.center_of_mass(np.reshape(data, (20, 20)))
    img2 = Image.new("L", (28, 28), 0)
    img2.paste(img, (int(round(14-centre[1])), int(round(14-centre[0]))))
    data2 = np.array(img2.getdata())
    data2 = data2/255
    netGuess(data2)
    return data

def netGuess(data):
    ''' feed the data through the network to output guess '''
    guess = net.guess(data)
    numguess = np.where(guess == np.amax(guess))[0][0]
    rounded = round(np.amax(guess) * 100, 2)
    info['text'] = "Guess: "+str(numguess)+ "\nCertainty: "+str(rounded)+"%"

def activate_paint(e):
    ''' start keydown '''
    global lastx, lasty, fluid_draw
    if fluid_draw:
        cv.unbind('<ButtonRelease-1>')
        cv.bind('<B1-Motion>', paint)
    else:
        cv.unbind('<B1-Motion>')
        cv.bind('<ButtonRelease-1>', draw_rect)
    lastx, lasty = e.x, e.y

def draw_rect(e):
    ''' draws a rectangle on release '''
    global lastx, lasty
    cv.create_rectangle(lastx, lasty, e.x, e.y, fill="white")
    if e.x > lastx:
        x1, x2 = lastx, e.x
    else:
        x1, x2 = e.x, lastx
    if e.y > lasty:
        y1, y2 = lasty, e.y
    else:
        y1, y2 = e.y, lasty
    generation.create_boundry(x1, y1, x2, y2)

def paint(e):
    ''' apply lines to image and canvas '''
    global lastx, lasty
    x, y = e.x, e.y
    width = 15
    cv.create_line((lastx, lasty, x, y), fill="white", width=30)
    cv.create_oval(x-width, y-width, x+width, y+width, outline="white", fill="white")
    #  --- PIL
    draw.line((lastx, lasty, x, y), fill='white', width=30)
    draw.ellipse([(x-width, y-width), (x+width, y+width)], outline='white', fill='white')
    lastx, lasty = x, y
    imgData()


def show_gen(first):
    ''' displays the position of all the brains '''
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
    btn_start.pack_forget()
    ''' runs the maze renforced learning '''
    while not fluid_draw:
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
        show_gen(True)

def main_page():
    ''' Set up the UI of the main navigation page '''
    title['text'] = "Neural Networks"
    clear()
    cv.pack_forget()
    btn_clear.pack_forget()
    randomness.pack_forget()
    pop_num.pack_forget()
    speed.pack_forget()
    info.pack_forget()
    btn_start.pack_forget()
    navigation['text'] = 'Deep Learning'
    navigation['command'] = draw_page
    navigation['width'], navigation['height'] = 20, 2
    navigation['font'] = ('futura', 30)
    navigation.pack()
    navigation2['command'] = maze_page
    navigation2['width'], navigation2['height'] = 20, 2
    navigation2['font'] = ('futura', 30)
    navigation2.pack()
    navigation3['command'] = help_page
    navigation3['width'], navigation3['height'] = 20, 2
    navigation3['font'] = ('futura', 30)
    navigation3.pack()
    generation.boundries = []

def help_page():
    navigation2.pack_forget()
    navigation3.pack_forget()
    navigation['text'] = "home"
    navigation['width'], navigation['height'] = 20, 1
    navigation['font'] = ('futura', 12)
    navigation['command'] = main_page
    title['text'] = "Help page"
    info['font'] = ('futura', 9)
    with open('help.txt') as f:
        info['text'] = f.read()
    info.pack()

def draw_page():
    ''' Set up the UI of the handwritten numerals guesser '''
    global lastx, lasty, fluid_draw
    clear()
    info['font'] = ('futura', 14)
    title['text'] = "Deep Learning"
    info['text'] = "Guess: 0\nCertainty: 0.00%"
    navigation2.pack_forget()
    navigation3.pack_forget()
    lastx, lasty = None, None
    cv.bind('<1>', activate_paint)
    info.pack()
    cv.pack(expand=False, fill=None, side="top")
    navigation['text'] = 'home'
    navigation['command'] = main_page
    navigation['width'], navigation['height'] = 20, 1
    navigation['font'] = ('futura', 12)
    btn_clear.pack()
    fluid_draw = True

def maze_page():
    ''' Set up the UI of the renforced learning pathfinding '''
    global fluid_draw
    clear()
    fluid_draw = False
    navigation2.pack_forget()
    navigation3.pack_forget()
    navigation['text'] = "home"
    navigation['command'] = main_page
    navigation['width'], navigation['height'] = 20, 1
    navigation['font'] = ('futura', 12)
    title['text'] = "Reinforced Learning"
    randomness.set(0.1)
    speed.set(1)
    pop_num.set(100)
    cv.pack(expand=False, fill=None, side="top")
    cv.bind('<1>', activate_paint)
    btn_start.pack(side="bottom", pady=20)
    randomness.pack(side="left", padx=60, anchor="n")
    speed.pack(side="left", padx=0, anchor="n")
    pop_num.pack(side="left", padx=60, anchor="n")
    show_gen(True)
    make_goal(250, 250)

def make_goal(x, y):
    ''' setup the goal for the brains to find '''
    width = 3
    generation.goal(x, y, width)
    cv.create_oval(x-width, y-width, x+width, y+width, fill="yellow", outline="yellow")

def clear():
    ''' clear the revtangle and image '''
    cv.delete("all")
    draw.rectangle([(0, 0), image1.size], fill='black')

if __name__ == "__main__":
    ''' When code is first run '''
    # Collect neural network
    net = get_network("networks/mnist2.obj")
    generation = gen(200, start=[50, 50])
    generation.create_boundry(0, 0, 300, 300, out=True)
    generation.populate(100)

    # Set up UI
    root = Tk()
    root.title("NETLEARN :)")
    root.resizable(False, False)
    root.geometry("550x575")
    title = Label(root, text="Test Network", height=2, font=("futura", 40))
    title.pack()

    cv = Canvas(root, width=300, height=300, bg='black')
    navigation = Button(root, text="Deep Learning", command=draw_page)
    navigation2 = Button(root, text="Renforced Learning", command=draw_page)
    navigation3 = Button(root, text="Help", command=help_page)
    info = Label(root, justify='left', text="Guess: 0\nCertainty: 00.00%")
    btn_clear = Button(text="clear", command=clear)
    btn_start = Button(text="start", command=run, height=2, width=30)

    speed = Scale(root, from_=1, to=20, orient="horizontal", label="Speed")
    pop_num = Scale(root, from_=2, to=500, orient="horizontal", label="Population")
    randomness = Scale(root, from_=0, to=1, orient="horizontal", resolution=0.01, label="Randomness")

    fluid_draw = False
    image1 = Image.new('L', (300, 300), 'black')
    draw = ImageDraw.Draw(image1)

    main_page()
    root.mainloop()
