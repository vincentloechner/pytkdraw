"""Testing the tkdraw basic module."""
import tkdraw.basic as graph

def test_basic():
    HEIGHT = 200
    WIDTH = 400

    graph.open(HEIGHT, WIDTH)

    for i in range(HEIGHT):
        for j in range(WIDTH):
            if ((i-j)//50) % 2 == 0:
                graph.plot(i, j, color="red")
        graph.refresh()

    graph.wait()
