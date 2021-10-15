"""Testing the tkdraw screen module, board version."""
import tkdraw.screen

HEIGHT = 6
WIDTH = 8
TILE_SIZE = 100

grid = [
    [0, 1, 2, 3, 4, 5, 6, 7],
    [None]*8,
    [None, 8, 9, None, None, None, None, None],
    [None]*8,
    [0]*8,
    [2]*8,
]
# open a window containing a HEIGHTxWIDTH board,
# each tile is TILE_SIZE pixels wide,
g = tkdraw.screen.open((HEIGHT, WIDTH), TILE_SIZE)

# draw checkered tiles in it
for i in range(HEIGHT):
    for j in range(WIDTH):
        if (i+j) % 2 == 0:
            g.draw_tile((i, j), "grey")
g.message("""This is a message box.
You should see a checkered board in the window.
Just click anywhere to continue.
""")

g_objects = g.draw_grid(grid)

g.message("""You should see a board containing colored tiles in the window.
<click>
""")

t_object = g.draw_text((TILE_SIZE*(HEIGHT+1)//2, TILE_SIZE*WIDTH//2),
    "this is a text inside the window.\n<click to remove>")
g.wait_event()
g.rm(t_object)

t_object = g.draw_text((TILE_SIZE*(HEIGHT+1)//2, TILE_SIZE*WIDTH//2),
    "<click to remove the pieces>")
g.wait_event()
for o in g_objects:
    g.rm(o)
g.rm(t_object)

g.draw_text((TILE_SIZE*(HEIGHT+1)//2, TILE_SIZE*WIDTH//2),
    "close the window to quit")

# wait for the user to close the window
while g.wait_event()[0] != "END":
    pass

g.close()
