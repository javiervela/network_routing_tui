import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings("ignore")

from network_routing_tui.graph import Graph
from network_routing_tui.measurement import evaluate_convergence, evaluate_weak_edge
from network_routing_tui.graph_generator import gen_mesh, concatenate_graph, gen_tree, gen_random, link_graph

EXPERIMENT_DIR = "./experiments/4_remarkable_graphs/"

print(" & 10 & 12 & 14 & 16 & 18 ")
for m in ["mesh", "random", "tree"]:
    res = m + "&"
    for i in range(10,20,2):
        su = 0
        for j in range(100):
            if m == "mesh":
                G = gen_mesh(i)
            elif m == "random":
                G = gen_random(i)
            elif m == "tree":
                G = gen_tree()
            u,v,d = evaluate_weak_edge(G)
            su += d
        res = res + str(su / 100) + " & "
    print(res[:-1])


