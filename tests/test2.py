import matplotlib.pyplot as plt
import numpy as np

from network_routing_tui.graph import Graph
from network_routing_tui.link_state import link_state
from network_routing_tui.graph_generator import gen_random, gen_damage
from network_routing_tui.measurement import evaluate_routing

def test_graph(d_weight = 50, steps = 500):
    G = Graph()
    G.load_file("./tests/devious_triangle.txt")

    for i in range(10):
        G.distance_vector()

    G.apply_input("D C -")
    G.apply_input("A D " + str(d_weight))

    l = []
    for i in range(steps):
        G.distance_vector()
        d = evaluate_routing(G)
        l.append(d)
    return l

G = Graph()
G.load_file("./tests/devious_triangle.txt")
G.show()

for i in range(4):
    x = np.arange(500)
    y = test_graph([50,100,200,400][i])
    plt.subplot(2,2,i + 1)
    plt.plot(x,y)
plt.show()
