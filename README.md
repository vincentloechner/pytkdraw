# A basic draw GUI for Python3 based on tkinter, synchroneous.

[](---------------------------------------------------------------------------)
## CONTENT

This repository contains a Python3 module that was developed as an easy to use
tkdrawical library for Python3 beginners or for people who just wish to draw
simple graphical objects in a window. It is synchronous, which means that you
don't have to handle asynchronous calls to predefined functions to react to
the interface events. It provides a basic "screen" class, that opens a simple
tkinter window containing a canvas. The single function waiting for an event
to occur is wait_event(), and there are various drawing functions.

[](---------------------------------------------------------------------------)
## USAGE

- install tkinter for pyhton3
  ('sudo apt install python3-tk' on most linux distributions)
- install tkdraw
  **TODO**: explain howto

- Try the following code:
```py
import tkdraw

g = tkdraw.screen((10, 10))
for i in range(10):
    for j in range(10):
        if (i+j) % 2 == 0:
            g.draw_tile((i, j))

while g.wait_event()[0] != "END":
    pass

g.close()
```
Run with python3.

[](---------------------------------------------------------------------------)
## HISTORY

This module was first written in 2018, when Vincent was in charge of the
"algorithms & programming" course based on python3, in the first year of
Strasbourg University Bachelor degree in Computer Science. It's original
name was graph.py.

Since then various version have been given to some 400 students applying to
this diploma each year.

[](---------------------------------------------------------------------------)
## COPYRIGHT

Copyright 2018-2021, Vincent Loechner.
Distributed under the MIT license.
