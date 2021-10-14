"""Basic draw graphical user interface (GUI) based on tkinter, synchroneous.

Test this module using `python -m tkdraw.screen`
The online documentation is available under python3:
```
$ python3
>>> import tkdraw.screen as tdk
>>> help(tkd.open)
or
>>> help(tkd.FUNC_NAME)
```

Copyright 2018-2021, Vincent Loechner.
Distributed under the MIT license (see LICENSE)

GIT source: https://github.com/vincentloechner/pytkdraw.git
"""

import tkinter as tk
import queue


class open(tk.Canvas):
    """Main class for a window containing a board (2D grid).

    _Parameters_
    Optional creation parameters:
    - size ((int, int)): a couple (height, width) specifying the size of the
                         grid (default: (8, 8))
    - pixels (int): number of pixels of a square (default: 100)
    - grid (bool): if True, prints a one-pixel large grid : horizontal and
                   vertical lines separating the squares (default: True)

    This class inherits from tkinter's canvas class, you can directly call the
    canvas methods to perform advanced drawings in this canvas (expert mode).
    You may refer to the documentation of tkinter describing the Canvas widget.
    """

    def __init__(
        self, size=(8, 8), pixels=100, grid=True
    ):
        """Initialize the window instance.

        Create a tkinter root object and a canvas (from which we inherit).
        Redirects all events to the appropriate functions.
        Arguments are described in the "open" main class.
        """
        # some private methods below, to react to asynchronous events:

        # private: the user clicked on a square
        def click(evenement):
            # min to handle user clicking on the last pixel:
            i = min((evenement.y-1)//self.pixels, self.size[0]-1)
            j = min((evenement.x-1)//self.pixels, self.size[1]-1)
            # add the event (line, column) to the queue
            self.eventq.put(("click", (i, j)))
            # and leave the mainloop
            self.root.quit()

        # private: the user hit a key
        def key(evenement):
            # put the event in the queue
            self.eventq.put(("key", evenement.keysym))
            # and leave the mainloop
            self.root.quit()

        # private: the user closed the window
        def async_end():
            # put the END event in the queue
            self.eventq.put(("END", None))
            # and close
            self.close()

        # private: regularily check if some events are pending in the queue
        # and wake up
        def checke():
            self.after_id = self.root.after(1000, checke)
            # stop mainloop
            self.root.quit()

        #################################
        # INIT
        self.size = size
        self.pixels = pixels
        self.root = None
        self.after_id = None

        self.eventq = queue.Queue()

        self.root = tk.Tk()
        self.root.grid()
        # you can create other frames here if you want to
        # self.frame = tk.Frame(root)

        # creates THE canvas:
        tk.Canvas.__init__(
                self,
                self.root,
                height=self.size[0]*self.pixels,
                width=self.size[1]*self.pixels,
                background="#ddd",
                takefocus=True,
                borderwidth=0,
                highlightthickness=1)
        self.grid(row=0, column=0)
        self.focus_set()

        # binds the click function to the click event
        self.bind("<Button-1>", click)
        # binds the key function to the keypress event
        self.bind("<Any-KeyPress>", key)

        # checke will be called once per second
        self.after_id = self.root.after(1000, checke)
        # ensure that async_end is called if the window is killed
        self.root.protocol("WM_DELETE_WINDOW", async_end)

        # prints the original state
        self.print_grid(grid=grid)

    def __enter__(self):
        """internal: With -as: statement compatibility."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """internal: With -as: statement compatibility."""
        self.close()

    def __del__(self):
        """internal: if the object is freeed from Python."""
        self.close()

    def close(self):
        """Close this window."""
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        if self.root is not None:
            self.root.destroy()
            self.root = None

    def message(self, message):
        """Print a message in a box and wait for the user to click somewhere.

        - message (str): the string to print

        _Return_value_
        - (boolean) True if the user just clicked on the box,
          False if the user killed the window.
        """
        # private: the user clicked in the box
        def c(event):
            self.eventq.put("ok")
            self.root.quit()

        assert self.root, "ERROR: window killed!"
        m = tk.Message(
                self.root, text=message,
                padx=20, pady=20,
                relief=tk.RAISED, borderwidth=5,
                )
        # mouse click:
        m.bind("<Button-1>", c)
        m.grid(row=0, column=0)
        while True:
            s = self.wait_event()
            if s[0] == "END":
                # the window has been closed
                # put the end msg back in the queue and return False
                self.eventq.put(s)
                return False
            # all the other events just close the message box and return True:
            m.destroy()
            return True

    ###########################################################################
    # HIGH LEVEL INTERFACE                                                    #
    # This function can be used to print whole standard boards.               #
    # Matrices should contain integers (-> representing pieces colors/players)#
    # or the None special value (-> nothing there)                            #
    ###########################################################################

    # by default define those 10 colors:
    DEFAULT_COLOR = ["black", "white", "red", "green", "blue",
                     "yellow", "cyan", "magenta", "orange", "darkgrey"]

    def print_grid(
        self, matrix=None, grid=True
    ):
        """Print a complete grid of pieces, using the 10 default colors.

        _Parameters_
        If matrix is None (default), just prints the grid
        If grid is True (default) prints the horizontal+vertical grid

        _Return_value_
        - a list of the graphical objects that were created (grid excluded).
        """
        assert self.root, "ERROR: window closed!"
        # erase everything for a start
        self.erase()
        # gap is used by draw_tile to fill the inside of a tile (including
        # borders, or not
        if grid:
            self.gap = 1
            for i in range(self.size[0]):
                self.create_line(1, i*self.pixels+1,
                                 self.size[1]*self.pixels+1, i*self.pixels+1,
                                 width=1)
            for i in range(self.size[1]):
                self.create_line(i*self.pixels+1, 1,
                                 i*self.pixels+1, self.size[0]*self.pixels+1,
                                 width=1)
        else:
            self.gap = 0
        # draw the pieces
        o = []
        if matrix is not None:
            for i in range(self.size[0]):
                for j in range(self.size[1]):
                    if matrix[i][j] is not None:
                        o.append(self.draw_piece((i, j), matrix[i][j],
                                 refresh=False))
        # update just once at the end, for performance
        self.update()
        return o

    def erase(
        self
    ):
        """Erase everything from the window.

        All graphical objects that were created are deleted.
        """
        assert self.root, "ERROR: window closed!"
        self.delete(tk.ALL)

    ###########################################################################
    # INTERMEDIATE LEVEL INTERFACE                                            #
    # draw various objects on a board (2D grid)                               #
    ###########################################################################
    def draw_piece(
        self, p, player=0,
        color=None,
        refresh=True
    ):
        """Draw a piece in position p=(line, column), player-colored.

        Usage notice: don't use this function if your tiles are too small, you
        won't see the piece.

        _Parameters_
        - p ((int, int)): grid position (line, column)
        Optional:
        - player (int): player number (default: 0)
          player is used only if color is NOT given.
        OR
        - color (str): fill color of the piece. If a color is given, player
          is ignored.
        - refresh (bool): refresh the window after drawing (default: True)

        _Return_value_
        - the ID of the graphical object that was created (int).
        """
        assert self.root, "ERROR: window closed!"
        if color is None:
            if isinstance(player, int):
                color = self.DEFAULT_COLOR[player % len(self.DEFAULT_COLOR)]
            else:
                color = self.DEFAULT_COLOR[0]

        bord = self.pixels//10+1
        i, j = p
        assert 0 <= i < self.size[0] and 0 <= j < self.size[1], \
            "ERROR: trying to draw outside the window!"

        o = self.create_oval(j*self.pixels+bord+1,
                             i*self.pixels+bord+1,
                             (j+1)*self.pixels-bord+1,
                             (i+1)*self.pixels-bord+1,
                             width=1, fill=color)
        if refresh:
            self.update()
        return o

    def move_piece(
        self, obj, pos, refresh=True
    ):
        """Move a piece (obj ID) in grid position pos (couple).

        _Parameters_
        - obj (int): a previously created piece ID
        - pos ((int, int)): new grid position (line, column)
        Optional:
        - refresh (bool): refresh the window after drawing (default: True)

        _Return_value_
        - None
        """
        assert self.root, "ERROR: window closed!"
        i, j = pos
        assert 0 <= i < self.size[0] and 0 <= j < self.size[1], \
            "ERROR: trying to move a piece outside the window!"
        bord = self.pixels//10+1
        self.coords(
            obj,
            j*self.pixels+bord+1,
            i*self.pixels+bord+1,
            (j+1)*self.pixels-bord+1,
            (i+1)*self.pixels-bord+1
            )
        if refresh:
            self.update()

    def draw_tile(
        self, p,
        color="black",
        border=0,
        refresh=True
    ):
        """Fill the inside of a tile in position p=(line, column) with a color.

        _Parameters_
        - p ((int, int)): grid position (line, column)
        Optional:
        - color (str): color of the tile (default: "black")
        - border (int): border thickness (default: 0) - borders will overlap on
          neighboring tiles
        - refresh (bool): refresh the window after drawing (default: True)

        _Return_value_
        - the colored tile ID (int).
        """
        assert self.root, "ERROR: window closed!"
        i, j = p
        assert 0 <= i < self.size[0] and 0 <= j < self.size[1], \
            "ERROR: trying to fill a tile outside the window!"
        o = self.create_rectangle(j*self.pixels+1+self.gap,
                                  i*self.pixels+1+self.gap,
                                  (j+1)*self.pixels+1,
                                  (i+1)*self.pixels+1,
                                  width=border, fill=color)
        if refresh:
            self.update()
        return o

    def move_tile(
        self, obj, pos, refresh=True
    ):
        """Move a colored tile to another grid position.

        _Parameters_
        - obj (int): a previously created tile ID
        - pos ((int, int)): new position in the grid (line, column)
        Optional:
        - refresh (bool): refresh the window after drawing (default: True)

        _Return_value_
        - None
        """
        assert self.root, "ERROR: window closed!"
        i, j = pos
        assert 0 <= i < self.size[0] and 0 <= j < self.size[1], \
            "ERROR: trying to move a tile outside the window!"
        self.coords(
            obj,
            j*self.pixels+1++self.gap,
            i*self.pixels+1++self.gap,
            (j+1)*self.pixels+1,
            (i+1)*self.pixels+1
            )
        if refresh:
            self.update()

    ###########################################################################
    # low level interface:                                                    #
    # draw pixels, lines, circles, etc.                                       #
    ###########################################################################
    def draw_line(
        self, x1, x2, color="black", thickness=1, refresh=True
    ):
        """Draw a line between x1=(l1,c1) and x2=(l2,c2) (excluded).

        _Parameters_
        - x1, x2 (two couples (int, int)): pixel-wise positions (line, column)
          of the two points. (0,0) = top-left position.
        Optional:
        - color (str): line color (default: "black")
        - thickness (int): thickness of the line (default: 1)
        - refresh (bool): refresh the window after drawing (default: True)

        _Return_value_
        - the ID of the graphical object that was created (int).
        """
        assert self.root, "ERROR: window closed!"
        o = self.create_line(x1[1]+1, x1[0]+1, x2[1], x2[0],
                             width=thickness, fill=color)
        if refresh:
            self.update()
        return o

    def draw_circle(
        self, x1, x2,
        color="black", border=1, refresh=True
    ):
        """Draw a circle in the bounding box of x1=(l1,c1) and x2 (excluded).

        _Parameters_
        - x1, x2 (two couples (int, int)): pixel-wise positions (line, column)
          of the two points. (0,0) = top-left position.
        Optional:
        - color (str): color of the inside (default: "black")
                       if color == None, don't fill the circle.
        - border (int): border thickness (default: 1) - borders can overflow
          over the given pixels coordinates
        - refresh (bool): refresh the window after drawing (default: True)

        _Return_value_
        - the ID of the graphical object that was created (int).
        """
        assert self.root, "ERROR: window closed!"
        o = self.create_oval(x1[1]+1, x1[0]+1, x2[1], x2[0],
                             width=border, fill=color)
        if refresh:
            self.update()
        return o

    def draw_text(
        self, position, text,
        color="black", fontname="Purisa", fontsize=11, refresh=True
    ):
        """Draw a text centered at a given position=(l1,c1).

        _Parameters_
        - position (couple (int,int)): pixel-wise position (line, column).
          (0,0) = top-left position.
        - text (str): text to print
        Optional:
        - color (str): text color (default: "black")
        - fontname (str): font name (default: "Purisa")
        - fontsize (int): font size (default: 11pt)
        - refresh (bool): refresh the window after drawing (default: True)

        _Return_value_
        - the ID of the graphical object that was created (int).
        """
        assert self.root, "ERROR: window closed!"
        o = self.create_text(position[1]+1, position[0]+1,
                             text=text,
                             font=(fontname, fontsize),
                             fill=color)
        if refresh:
            self.update()
        return o

    def bg(
        self, obj, before=1, refresh=True
    ):
        """Send a graphical object (ID) to background.

        _Parameters_
        - obj (int): object ID returned by an object creation method
        Optional:
        - before (int): the object behind which to hide (default: 1 = all)
        - refresh (bool): refresh the window after drawing (default: True)

        _Return_value_
        - None
        """
        assert self.root, "ERROR: window closed!"
        # se met en fond, derrière l'objet 'before':
        self.tag_lower(obj, before)
        if refresh:
            self.update()

    def refresh(
        self
    ):
        """Refresh all objects previously drawn in the window.

        Usage note: you can create several successive objects without
        refreshing by passing the extra argument "refresh=False" to the drawing
        functions, and then refresh only once using this function.
        Good for speed, especially if you draw many things.

        _Return_value_
        - None
        """
        assert self.root, "ERROR: window closed!"
        self.update()

    def rm(
        self, obj, refresh=True
    ):
        """Delete a graphical object (ID).

        _Parameters_
        - obj (int): object ID returned by an object creation method
        Optional:
        - refresh (bool): refresh the window after drawing (default: True)

        _Return_value_
        - None
        """
        assert self.root, "ERROR: window closed!"
        self.delete(obj)
        if refresh:
            self.update()

    ###########################################################################
    # Main I/O function                                                       #
    ###########################################################################
    def wait_event(self, delay=None):
        """Wait for the user to interact with the window.

        The tracked events are only keypress and mouse click (left button).
        _Parameters_
        Optional:
        - delay (int): waiting time in ms (default: wait forever)

        _Return_value_
        - if the user clicks on a tile of the board, return the couple
          ("click", (line, column))
          where (line, column) are the coordinates of the clicked tile
        - if the user hits a key, return the couple
          ("key", letter)
          where letter is a string containing a description of the key.
          If you're looking for a specific key, just give a try to the demo:
          `python3 -m tkdraw` will print all occuring events in the console
        - if the user closes the window, return the couple
          ("END", None)
        - if the delay expires (when given), the special value
          None
        """
        # private: called when the timer expires
        def delay_expire():
            self.eventq.put(None)
            self.idd = None
            self.root.quit()

        # trigger the timer
        self.idd = None
        if delay is not None:
            assert self.root, "ERROR: window closed!"
            self.idd = self.root.after(delay, delay_expire)
        # This is Tk's main loop
        # checks the events and get out if something happens
        while True:
            ####################
            try:
                # get something from the event queue
                r = self.eventq.get(False)
                # cancels the timer if I got something
                if self.idd is not None and self.root is not None:
                    self.root.after_cancel(self.idd)
                return r
            except queue.Empty:
                # no event in the queue, continue waiting (go to mainloop)
                pass
            ####################
            assert self.root, "ERROR: window closed!"
            # mainloop stops if I get an event
            self.root.mainloop()
            ####################

    def mouse_position(self):
        """Return the mouse position (pixel-wise).

        Usage notice: if a coordinate is negative or greater than the window
        size, the mouse is out of the window.

        _Return_value_
        - a couple (int,int): pixel-wise position (line, column) relative to
          (0,0) = top-left position in the window.
        """
        # private: the mouse moved
        def motion(event):
            self.souris = (event.y, event.x)

        assert self.root, "ERROR: window closed!"
        self.refresh()
        try:
            return self.souris
        except AttributeError:
            self.bind("<Motion>", motion)
            self.souris = (0, 0)  # initial position if the mouse doesn't move
            return self.souris


###########################################################################
# Test program: 8x8 board, click to place/remove black/white pieces       #
###########################################################################
if __name__ == "__main__":
    # open the window containing a board
    SIZE = 8
    PIXEL_SIZE = 100
    # use tkdraw.screen.open() if you include this as a module with
    # 'import tkdraw.screen'
    g = open((SIZE, SIZE), PIXEL_SIZE)

    # checkered tiles:
    for i in range(SIZE):
        for j in range(i % 2, SIZE, 2):
            g.draw_tile((i, j), color="yellow", refresh=False)
    # refresh only once for performance
    g.refresh()

    # welcome message
    msg = g.draw_text((PIXEL_SIZE//2, PIXEL_SIZE+PIXEL_SIZE//2),
                      "Hello!\nclick here ->")

    # main loop: wait for user clicks and draw pieces.
    # tab = 2D grid containing the graphical object IDs
    # if you click again on a piece it will be deleted, same player plays
    tab = [[None]*SIZE for i in range(SIZE)]
    player = 1  # white player starts, black = -1.
    while True:
        p = g.wait_event()
        # demo: print the content of the event couple
        print(p)

        # stop when:
        if p[0] == "END":
            break
        # or when:
        if p[0] == "key" and p[1] in ["q", "Q", "Escape"]:
            break

        # ignore all events other than mouse click
        if p[0] != "click":
            continue

        lig, col = p[1]
        if tab[lig][col] is None:
            tab[lig][col] = g.draw_piece(p[1], player)
            # player : 1 -> -1 -> 1 -> ...
            player = -player
        else:
            # remove the piece at position (lig, col)
            g.rm(tab[lig][col])
            tab[lig][col] = None

        # remove the previous message
        g.rm(msg)
        # and put a new one
        msg = g.draw_text((PIXEL_SIZE//2, PIXEL_SIZE+PIXEL_SIZE//2),
                          [0, "white player", "black player"][player])

    # at the end, close the window properly
    g.close()
