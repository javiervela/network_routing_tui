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
    l = damage_list(G,n) 
    return damage(G,l)

def damage_list(G, n=1):
    l = [a for a in G.edges()]
    random.shuffle(l)
    return l[:n]

def damage(G, l):
    for a in l:
        u,v = a
        G.remove_edge(u,v)
    return G

def worsen(G, l):
    for a in l:
        u,v = a
        G.add_edge(u, v, weight=500)
    return G


        
