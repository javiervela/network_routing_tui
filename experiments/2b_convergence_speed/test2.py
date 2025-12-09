import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings("ignore")

from network_routing_tui.graph import Graph
from network_routing_tui.measurement import evaluate_convergence, evaluate_routing, evaluate_table_distance

EXPERIMENT_DIR = "./experiments/2b_convergence_speed/"

G = Graph()
G.load_file(f"{EXPERIMENT_DIR}/devious2.txt")
G.show()
for i in range(10):
    G.distance_vector()
G.apply_input("A B 500")
for i in range(10):
    print("-----")
    for e in ["A", "B", "C"]:
        rt = G.get_routing_table(e)
        print(e,":",rt.get_distance("D"), "via", rt.get_seq("D"), "(actual distance:", G.send_msg(e,"D"),")")
    print(evaluate_routing(G) + evaluate_table_distance(G))
    G.distance_vector(True)


G.show()

n = 200
DISTANCES = [7 + i*1 for i in range(n)]
y_enhanced = []
y_legacy = []
for i, d_weight in enumerate(DISTANCES):
    for a in [False, True]:
        G = Graph()
        G.load_file(f"{EXPERIMENT_DIR}/devious2.txt")

        for i in range(10):
            G.distance_vector()

        G.apply_input("A B " + str(d_weight))

        j = evaluate_convergence(G, a)
        if a:
            y_legacy.append(j)
        else:
            y_enhanced.append(j)

plt.plot(DISTANCES, y_legacy, color='red')
plt.plot(DISTANCES, y_enhanced, color='blue')
plt.xlabel("New weight of A-D")
plt.ylabel("Iterations needed for convergence")
plt.show()

        
