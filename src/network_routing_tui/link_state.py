from network_routing_tui.routing_table import RoutingTable


def link_state(G, node):
    """Perform link state algorithm for graph G and return the routing table"""
    resR = RoutingTable(node)
    toVisit = G.get_neighbors_distance(node)
    visited = [node]

    while len(toVisit) > 0:
        newV = toVisit.pop(0)
        oldD = resR.get_distance(newV[0])
        if (oldD <= 0 or oldD > newV[1]) and not newV[0] in visited:
            resR.add_route(newV[0], newV[1], newV[2])
            visited.append(newV[0])
            neighb = G.get_neighbors_distance(newV[0])
            neighb = [a for a in neighb if not a[0] in visited]
            neighb = [[a[0], a[1] + newV[1], a[2]] for a in neighb]

            toVisit = toVisit + neighb
            toVisit.sort(key=lambda edge: edge[1])

    return resR
