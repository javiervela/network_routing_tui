import matplotlib.pyplot as plt
import numpy as np

from network_routing_tui.graph import Graph
from network_routing_tui.measurement import evaluate_routing

EXPERIMENT_DIR = "./experiments/3a_dv_enhanced_performance/"

G = Graph()
G.load_file(f"{EXPERIMENT_DIR}/graph.txt")
G.draw()
plt.savefig(f"{EXPERIMENT_DIR}/initial_graph.png")
plt.close()

results = []

d = evaluate_routing(G)
results.append(d)

dv_steps = G.number_of_nodes()
for i in range(dv_steps):
    G.distance_vector()
    d = evaluate_routing(G)
    results.append(d)

# TODO good event

# TODO bad event

STEPS = 1 + dv_steps  # TODO + good_event_steps + bad_event_steps

plt.plot(np.arange(STEPS), results)
plt.show()
