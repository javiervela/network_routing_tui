from network_routing_tui.graph import Graph
from network_routing_tui.routing_table import RoutingTable
from network_routing_tui.link_state import link_state

def evaluate_routing(G):
    error = 0
    n = G.number_of_nodes()
    for u in G.nodes():
        gT = link_state(G, u)
        for v in G.nodes():
            d = G.send_msg(u,v, n)
            if d != gT.get_distance(v):
                error += 1
    return error

def evaluate_table_distance(G):
    error = 0
    n = G.number_of_nodes()
    for u in G.nodes():
        gT = G.get_routing_table(u)
        for v in G.nodes():
            d = G.send_msg(u,v,n)
            if d != gT.get_distance(v):
                error += 1
    return error

def evaluate_convergence(G, legacy = False, convergence_limit = 1000):
    """ This function modifies G, be careful !!!"""
    d = evaluate_routing(G) + evaluate_table_distance(G)
    i = 0
    while d != 0:
        G.distance_vector(legacy)
        d = evaluate_routing(G) + evaluate_table_distance(G)
        i += 1
        if i > convergence_limit:
            return -1
    return i     

def evaluate_weak_edge(G, legacy = False, convergence_limit = 200):
    longest = 0
    bu,bv = "A", "A"
    G.save_file("temp.txt")
    for u, v, weight in G.edges.data("weight"):
        H = Graph()
        H.load_file("temp.txt")
        for i in range(50):
            H.distance_vector()
        H.add_edge(u,v, 100)   
        d = evaluate_convergence(H, legacy, convergence_limit)
        if d == -1:
            d = convergence_limit
        if d > longest:
            longest = d
            bu, bv = u,v
    return bu,bv,longest




