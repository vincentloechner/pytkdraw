"""Example usage, same as in the README."""
import tkdraw.screen

# open a window containing a 8x8 board,
# each tile is 100 pixels wide,
g = tkdraw.screen.Screen((8, 8), 100)

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
