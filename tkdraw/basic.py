"""Basic interface to the tkdraw.screen module.

This module provides four elementary functions to:
- open a window
- plot a pixel at a given position in the window
- refresh the window (at any step of your program)
- wait for the user to close the window

Python3 will fail with an "AssertionError" if any precondition of those
functions is not met.

Copyright 2019-2020, Vincent Loechner <loechner@unistra.fr>
Distributed under the MIT license (see LICENSE)

Source: https://github.com/vincentloechner/pytkdraw.git
"""
import tkdraw.screen as tkd


"""window (global): main window of this simplified version."""
window = None


def open(height, width):
    """Open a window of the given height, width.

    _Parameters_
    - height, width (int) : size of the window (in pixels)

    _Preconditions_
    - this function can be called only once, but if you wait() for the user to
      close a previously opened window you can open a new one.
    """
    global window
    assert window is None, "ERROR : function open() was called twice\
 in your program!"
    window = tkd.open((height, width), 1, grid=False)


def plot(line, column, color="black"):
    """Plot a pixel at position (line, column).

    Usage notice : the effective rendering of this pixel will only be done once
    you call refresh() or wait().

    _Parameters_
    - line, column (int): position of the pixel to plot
      (0, 0) is the top-left position.
    Optional:
    - color (str): a color (default value: "black").
      This string shall contain a tkinter-compatible color string -
      for a list of predefined color names see for example:
      https://www.wikipython.com/tkinter-ttk-tix/summary-information/colors/
      You can also specify an RGB-style color such as "#FF0000" for red.

    _Preconditions_
    - the window must have been opened with a call to open(height, width)
    - 0 <= line < height
    - 0 <= column < width
    """
    assert window, "ERROR: trying to plot in a non-existing window!"
    window.draw_tile((line, column), color=color, refresh=False)


def refresh():
    """Refresh the window.

    All plots that you did before this call will be displayed for real in the
    window.

    _Parameters_
    None

    _Preconditions_
    - the window must have been opened
    """
    assert window, "ERROR: trying to refresh a non existing window!"
    window.refresh()


def wait():
    """Wait for the user to close the window.

    This function is blocking, it will return once the user has (1) closed the
    window using the mouse, or (2) hit the 'escape' or 'q' key.

    Usage notice: you have to call this function before the end of your
    program, or you won't be able to see the content of the window. If you
    don't call this function, the window will just disapear when the program
    exits.

    _Parameters_
    None

    _Preconditions_
    - the window must have been opened
    """
    global window

    assert window, "ERROR: trying to close a non existing window!"
    window.refresh()
    while True:
        p = window.wait_event()
        if p[0] == "END":
            break
        if p[0] == "key" and (p[1] == "Escape" or p[1] == "q"):
            break
        # ignore all other events
    window.close()
    window = None


##############################################################################
# test module
##############################################################################
if __name__ == "__main__":
    HEIGHT = 300
    WIDTH = 400
    open(HEIGHT, WIDTH)
    for i in range(HEIGHT):
        for j in range(WIDTH):
            plot(i, j,
                 color=["black", "red", "white", "green"][((i+j)//15) % 4])
        refresh()
    wait()
