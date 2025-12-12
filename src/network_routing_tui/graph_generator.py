from network_routing_tui.graph import Graph
import random
import math

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
        res = alpha[int(j / pow(k, n -1))] + res
        n += 1
    return res

def gen_random(n = 10, p = 0.5):
    G = Graph()
    for i in range(n):
        for j in range(i+1,n):
            if random.random() < p:
                G.add_edge( get_name(i), get_name(j), random.randrange(1,10))
    return G

def gen_mesh(n = 10, p = 1):
    G = Graph()
    k = math.ceil(math.sqrt(n))
    for x in range(k):
        for y in range(k):
            for i in range(2):
                neigh = x + (1 - i) + (y + i) * k
                if neigh < n and x + (1 - i) < k and y + i < k:
                    G.add_edge( get_name(x + y * k), get_name(neigh), random.randrange(1,10))
    return G

def gen_tree(n = 10):
    G = Graph()
    for i in range(1,n):
        j = random.randrange(0,i)
        G.add_edge(get_name(i), get_name(j), random.randrange(1,10))
    return G

def link_graph(G, H):
    C = concatenate_graph(G,H)
    k = random.randrange(0, G.number_of_nodes())
    j = random.randrange(G.number_of_nodes(), G.number_of_nodes() + H.number_of_nodes())
    C.add_edge(get_name(k), get_name(j), random.randrange(1,10))
    return C

def gen_star(n = 10):
    G = Graph()
    for i in range(1,n):
        j = 0
        G.add_edge(get_name(i), get_name(j), random.randrange(1,10))
    return G

def get_rename(u,l,n=0):
    if not u in l:
        l.append(u)
    return get_name(l.index(u) + n)

def concatenate_graph(G,H):
    C = Graph()
    l = []
    for u, v, weight in G.edges.data("weight"):
        C.add_edge(get_rename(u,l), get_rename(v,l), weight)
    n = len(l)
    l = []
    for u, v, weight in H.edges.data("weight"):
        C.add_edge(get_rename(u,l,n), get_rename(v,l,n), weight)
    return C

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

def worsen(G, l, dmg = 500):
    for a in l:
        u,v = a
        G.add_edge(u, v, weight=dmg)
    return G


        
