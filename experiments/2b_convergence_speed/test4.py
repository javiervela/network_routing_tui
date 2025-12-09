import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings("ignore")

import json

from network_routing_tui.graph import Graph
from network_routing_tui.graph_generator import gen_random, damage_list, damage, worsen
from network_routing_tui.measurement import evaluate_convergence, evaluate_routing

EXPERIMENT_DIR = "./experiments/2b_convergence_speed/"

def show(l):
    res = ""
    for a in l:
        res += " " + a + " &"
    return res[:-1]

results = []
for k in range(4,17,2):
    results.append([])
    for p in [0.1,0.5,0.9]:
        n = 0
        for i in range(500):
            G = gen_random(k)
            G.save_file(f"{EXPERIMENT_DIR}/temp.txt")
            l = damage_list(G, 1)
            d = [0,0]
            for a in range(2):
                G.load_file(f"{EXPERIMENT_DIR}/temp.txt")    
                for j in range(20):
                    G.distance_vector()
                G = worsen(G, l, 100 + 50 * a)
                d[a] = evaluate_convergence(G, True)

            if d[1] > d[0] and d[1] != -1:
                n += 1
            elif d[1] < d[0]:
                print("OMG",i,"Damage:",l)
                print("  damage 100:", d[0]," damage 150:",d[1])
                G.load_file(f"{EXPERIMENT_DIR}/temp.txt")
                G.save_file(f"{EXPERIMENT_DIR}/counter" + str(i) + ".txt")
                G.show()
        results[-1].append(str(100 * n / 500.) + "%")
    print(k,":",show(results[-1]))

with open(EXPERIMENT_DIR + "table.json", "w") as fp:
    json.dump(results, fp)

       
