import tkdraw.basic as graph

HEIGHT = 400
WIDTH = 600

graph.open(HEIGHT, WIDTH)

for i in range(HEIGHT):
    for j in range(WIDTH):
        if ((i-j)//50) % 2 == 0:
            graph.plot(i, j, color="red")
    graph.refresh()

graph.wait()
