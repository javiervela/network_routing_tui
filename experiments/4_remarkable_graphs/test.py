import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings("ignore")

from network_routing_tui.graph import Graph
from network_routing_tui.measurement import evaluate_convergence, evaluate_weak_edge
from network_routing_tui.graph_generator import gen_mesh, concatenate_graph, gen_tree, gen_random, link_graph, gen_star

EXPERIMENT_DIR = "./experiments/4_remarkable_graphs/"

G = gen_star(10)
G.show()

"""
G = gen_mesh(12)
H = gen_random(10)
C = link_graph(G,H)
D = gen_random(12)
E = link_graph(D,C)

u,v,d = evaluate_weak_edge(E)
print("Worse edge ", u+"-"+v,"("+str(d)+")")
E.show()
"""
