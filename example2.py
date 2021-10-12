"""Basic example usage of the graph module, pixels version."""
import graph

# 1 = green, 2 = lightgreen
image = [
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 1, 2, 1, 0, 0],
    [0, 1, 0, 0, 2, 1, 0],
    [1, 1, 1, 1, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0],
]
ENLARGE = 50

VSIZE=ENLARGE*len(image)
HSIZE=ENLARGE*len(image[0])
# open a window of VSIZExHSIZE pixels
g = graph.fenetre((VSIZE, HSIZE), 1, grid=False)

# draw the enlarged image
for y in range(VSIZE):
    for x in range(HSIZE):
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
