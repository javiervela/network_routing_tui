class RoutingTable:
    def __init__(self, n):
        self.id = n
        self.routes = {}
        self.routes[n] = [n, 0]

    def show(self):
        res = ""
        l = []
        for r in self.routes:
            m = self.routes[r][0]
            if r == m:
                m = "-"
            l.append([r, m, self.routes[r][1]])

        l.sort(key=lambda route: route[2])

        for e in l:
            res += e[0] + " " + e[1] + " " + str(e[2]) + "\n"

        return res[:-1]

    def copy(self):
        c = RoutingTable(self.id)
        c.routes = self.routes.copy()
        return c

    def get_routes(self):
        return self.routes

    def get_distance(self, n):
        if n in self.routes:
            return self.routes[n][1]
        return -666

    def get_seq(self, n):
        if n in self.routes:
            return self.routes[n][0]
        return "ERROR"

    def add_route(self, n, w, seq):
        if not n in self.routes or w < self.get_distance(n):
            self.routes[n] = [seq, w]

    def update_dv(self, routable, w):
        for dest in routable.get_routes():
            d = routable.get_distance(dest)
            if d == 0:
                seq = self.id
            else:
                seq = routable.get_seq(dest)
            self.add_route(dest, w + d, seq)

    def get_table_as_list(self):
        return [
            (node, next_hop[0], str(next_hop[1]))
            for node, next_hop in self.routes.items()
        ]

def link_state(G, node):
    """Perform link state algorithm for graph G and return the routing table"""
    resR = RoutingTable(node)
    toVisit = G.get_neighbors_distance(node)
    visited = [node]

    while len(toVisit) > 0:
        newV = toVisit.pop(0)
        oldD = resR.get_distance(newV[0])
        if (oldD <= 0 or oldD > newV[1]) and not newV[0] in visited:
            resR.add_route( newV[0], newV[1], newV[2])
            visited.append(newV[0])
            neighb = G.get_neighbors_distance(newV[0])
            neighb = [a for a in neighb if not a[0] in visited]
            neighb = [[a[0], a[1] + newV[1], a[2]] for a in neighb]
            
            toVisit = toVisit + neighb
            toVisit.sort(key=lambda edge: edge[1])

    return resR
            





