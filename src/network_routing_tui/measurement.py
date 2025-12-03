from network_routing_tui.graph import Graph
from network_routing_tui.routing_table import RoutingTable
from network_routing_tui.link_state import link_state

def evaluate_routing(G):
    error = 0
    for u in G.nodes():
        gT = link_state(G, u)
        for v in G.nodes():
            d = G.send_msg(u,v)
            if d != gT.get_distance(v):
                error += 1
    return error

def evaluate_table_distance(G):
    error = 0
    for u in G.nodes():
        gT = G.get_routing_table(u)
        for v in G.nodes():
            d = G.send_msg(u,v)
            if d != gT.get_distance(v):
                error += 1
    return error
