# A basic draw GUI for Python3.

[](---------------------------------------------------------------------------)
## CONTENT

This python3 package contains two modules that were developed as easy to use
graphical libraries for programming beginners or for people who just wish to
easily draw simple graphical objects in a window. They are based on the tkinter
canvas object, but unlike tkinter they are synchronous.

The main module is tkdraw.screen. It is synchronous, which means that you don't
have to handle asynchronous calls to predefined functions to react to the
interface events. It provides a basic class, that opens a simple tkinter window
containing a canvas where you can draw boards or pixels. There is a single
function waiting for an event to occur and there are various drawing functions.
It is also very convenient to draw rectangular boards and simple pieces (as
colored circles). Check the examples or run the demo:
`python3 -m tkdraw.screen`.

The tkdraw.basic module provides four elementary functions: to open a window,
plot a pixel, refresh the window, and wait for the user to close it. It can be
used by complete python beginners to learn how to write loops, and get a visual
immediate result. Check the demo:
`python3 -m tkdraw.basic`

[](---------------------------------------------------------------------------)
## USAGE

- If you don't have it yet, install tkinter for python3
  (`sudo apt install python3-tk` on most linux distributions)

- Install tkdraw using pip:
```
python3 -m pip install tkdraw
```

- Try the following code:
```py
"""Example usage of the tkdraw screen module."""
import tkdraw.screen

# open a window containing a 8x8 board, each tile is 100 pixels wide
g = tkdraw.screen.open((8, 8), 100)

# draw checkered tiles
for i in range(8):
    for j in range(8):
        if (i+j) % 2 == 0:
            g.draw_tile((i, j), "grey")

# draw a black piece in tile (1, 5)
g.draw_piece((1, 5))
# draw a green piece below
g.draw_piece((2, 5), color="green")

# wait for the user to close the window
while g.wait_event()[0] != "END":
    pass

# cleanup
g.close()
```
Run with python3.

[](---------------------------------------------------------------------------)
## HISTORY

The `screen` module was first written in 2018, when Vincent was in charge of
the *Algorithms & Programming* course based on python3, in the first year of
Strasbourg University Bachelor degree in Computer Science. It's original
name was `graph.py`. The simplified `basic` module was written in 2019, for
complete python3 beginners to feel more comfortable with basic function calls.

Since then it was used by some 400 students applying to this diploma each year.

[](---------------------------------------------------------------------------)
## COPYRIGHT

Copyright 2018-2021, Vincent Loechner.

Distributed under the MIT license.
