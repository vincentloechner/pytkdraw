"""Example usage of the tkdraw module, pixels version."""
from tkdraw import screen

# 1 = green, 2 = lightgreen
image = [
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 1, 2, 1, 0, 0],
    [0, 1, 0, 0, 2, 1, 0],
    [1, 1, 1, 1, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0],
]
ENLARGE = 50

HEIGHT=ENLARGE*len(image)
WIDTH=ENLARGE*len(image[0])
# open a window of HEIGHTxWIDTH pixels (1-pixel sized tiles, no grid)
g = screen.screen((HEIGHT, WIDTH), 1, grid=False)

# draw the enlarged image
for y in range(HEIGHT):
    for x in range(WIDTH):
        l, c = y//ENLARGE, x//ENLARGE
        if image[l][c] == 1:
            g.draw_tile((y, x), "green", refresh=False)
        elif image[l][c] == 2:
            g.draw_tile((y, x), "lightgreen", refresh=False)
g.refresh()

# wait for the user to close the window
while g.wait_event()[0] != "END":
    pass

g.close()
