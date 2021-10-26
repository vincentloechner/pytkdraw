"""Example usage of the tkdraw screen module, board version."""
import tkdraw.screen

HEIGHT = 10
WIDTH = 15
TILE_SIZE = 100

# open a window containing a HEIGHTxWIDTH board,
# each tile is TILE_SIZE pixels wide,
g = tkdraw.screen.Screen((HEIGHT, WIDTH), TILE_SIZE)

# draw checkered tiles in it
for i in range(HEIGHT):
    for j in range(WIDTH):
        if (i+j) % 2 == 0:
            g.draw_tile((i, j), "grey")

# draw a black piece in tile (SIZE//10, SIZE//5)
g.draw_piece((HEIGHT//10, WIDTH//5))
# draw a green piece below
g.draw_piece((HEIGHT//10+1, WIDTH//5), color="green")

# wait for the user to close the window
while g.wait_event()[0] != "END":
    pass

g.close()
