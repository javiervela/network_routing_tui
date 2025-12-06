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





