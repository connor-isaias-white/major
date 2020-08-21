# Connor Isaias-White
# Major work 2020
## Installation guide
Open a terminal emulator, this can be done on macOS by searching for terminal in spotlight

Clone this reposotory using `git clone https://github.com/connor-isaias-white/major.git`

If you do not have git than you can install git using `brew install git`

If you do not have brew you can get it at [brew.sh](brew.sh)

It may take a couple of minutes to clone as for ease of installation, the libraries are included

Change directories into the file by typeing `cd major`

Activate the python enviroment using `source bin/activate`

run the main file using `python3 main.py`

A window looking like this should appear:
![Homepage](./readmeIMGs/home.png)

If any module import errors occur, ensure you are in the python enviroment.
    If the error still occurs, try installing the missing packages with pip

## Processes
### Help
![Help](./readmeIMGs/help.png)

The help page can be reached by clicking the help button

This will give the you a description of what you can do

This user guide will also provide help

To go back click the home button
### Deep learning
![Deep](./readmeIMGs/deep.png)

This page can be accessed by clicking the Deep learing button on the home page

On this page you are able to draw a SINGLE digit

Bellow the home button, the network will display the Guess and how certain it is

You need to draw your digits large to take up most of the canvas

You can draw by holding down the mouse/trackpad and draging

You can clear with the clear button

To go home click the home button

### Reinforced Learning
![Reinforced](./readmeIMGs/reinforced.png)

On this page you can witness an AI reach a goal through reinforced learning

You can start by clicking the 'start' button

Using sliders you can change the population, which determines how many different indervidual AIs there are in a generation

Changing randomness effects how different the next generation was from the previous, the fittest AIs are more likely to reproduce

Changing speed speeds up the simulation by updating the graphics less, increasing this makes it faster but more choppy

You are able to create obsitcals for the AIs to adapt to:
![Reinforced2](./readmeIMGs/reinforced2.png)

By clicking down with the mouse and draging, a rectangle is created with two opposite corners at the position you clicked down the mouse
and another at the location where you released the mouse

You can go home by clicking the Home button
