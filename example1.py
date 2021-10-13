"""Basic example usage of the tkdraw module, board version."""
import tkdraw

SIZE=20
# open a window containing a SIZExSIZE board, each tile is 50 pixels wide,
# with a black grid separating the tiles
g = tkdraw.screen((SIZE, SIZE), 50, grid=True)

# draw checkered tiles in it
for i in range(SIZE):
    for j in range(SIZE):
        if (i+j) % 2 == 0:
            g.draw_tile((i, j), "grey")

# draw a black piece in tile (SIZE//10, SIZE//5)
g.draw_piece((SIZE//10, SIZE//5))
# draw a green piece below
g.draw_piece((SIZE//10+1, SIZE//5), color="green")

# wait for the user to close the window
while g.wait_event()[0] != "END":
    pass

g.close()
