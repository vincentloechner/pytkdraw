"""Example usage of the basic module."""
import tkdraw.basic as graph

# size of the window (number of pixels)
HEIGHT = 400
WIDTH = 600

# open the window
graph.open_win(HEIGHT, WIDTH)

# plot some red diagonals in it
for i in range(HEIGHT):
    for j in range(WIDTH):
        if ((i-j)//50) % 2 == 0:
            graph.plot(i, j, color="red")
    # refresh the window every line (if you don't, it refreshes in the wait())
    graph.refresh()

# wait for the user to close the window
graph.wait()
