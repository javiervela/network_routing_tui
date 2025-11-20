from network_routing_tui.graph import Graph
import random

def get_name(i):
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if i == 0:
        return alpha[i]
    k = len(alpha)
    res = ""
    n = 1
    while i != 0:
        j = i%pow(k,n)
        i -= j
        res = alpha[j] + res
        n += 1
    return res

def gen_random(n = 10, p = 0.5):
    G = Graph()
    for i in range(n):
        for j in range(i+1,n):
            if random.random() < p:
                G.add_edge( get_name(i), get_name(j), random.randrange(1,10))
    return G

def gen_damage(G, n = 1):
    while n > 0:
        k = random.randrange(G.size())
        u,v = [a for a in G.edges()][k]
        G.remove_edge(u,v)
        n -= 1  
    return G      





        
