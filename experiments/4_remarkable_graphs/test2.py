import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings("ignore")

from network_routing_tui.graph import Graph
from network_routing_tui.measurement import evaluate_convergence, evaluate_weak_edge
from network_routing_tui.graph_generator import gen_mesh, concatenate_graph, gen_tree, gen_random, link_graph, gen_star

EXPERIMENT_DIR = "./experiments/4_remarkable_graphs/"

print(" & 10 & 12 & 14 & 16 & 18 ")
for m in ["tree","mesh","star", "random"]:
    res = m + "&"
    y = []
    for i in range(10,100,5):
        su = 0
        for j in range(100):
            if m == "mesh":
                G = gen_mesh(i)
            elif m == "random":
                G = gen_random(i)
            elif m == "tree":
                G = gen_tree(i)
            elif m == "star":
                G = gen_star(i)
            u,v,d = evaluate_weak_edge(G)
            su += d
        y.append(su)
        res = res + str(su / 100) + " & "
    print(res[:-1])
    x = list(range(10,100,5))
    plt.plot(x,y)
    plt.show()


