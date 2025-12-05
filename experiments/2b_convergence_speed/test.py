import matplotlib.pyplot as plt
import numpy as np

from network_routing_tui.graph import Graph
from network_routing_tui.measurement import evaluate_convergence

EXPERIMENT_DIR = "./experiments/2b_convergence_speed/"

n = 500
DISTANCES = [10 + i for i in range(n)]
y_enhanced = []
y_legacy = []
for i, d_weight in enumerate(DISTANCES):
    for a in [False, True]:
        G = Graph()
        G.load_file(f"{EXPERIMENT_DIR}/devious_triangle.txt")

        for i in range(10):
            G.distance_vector()

        G.apply_input("C D -")
        G.apply_input("A D " + str(d_weight))

        j = evaluate_convergence(G, a)
        if a:
            y_legacy.append(j)
        else:
            y_enhanced.append(j)

plt.plot(DISTANCES, y_legacy)
plt.plot(DISTANCES, y_enhanced)
plt.show()

        
