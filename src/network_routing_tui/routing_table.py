class RoutingTable:
    def __init__(self, n):
        self.id = n
        self.routes = {}  # routes[dest] = [via, distance]
        self.routes[n] = [n, 0]

    def compare(self, rT):
        for k in self.routes:
            if k in rT.routes:
                if self.get_distance(k) != rT.get_distance(k):
                    return False
            else:
                return False
        return True

    def show(self):
        # TODO change show naming
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

    def add_route(self, n, w, via):
        if n not in self.routes or w < self.get_distance(n):
            self.routes[n] = [via, w]

    def remove_route(self, n):
        self.routes.pop(n, None)

    def remove_neighbors(self, neigh):
        for k in list(self.routes.keys()):
            if (
                self.routes[k][0] == k or self.routes[k][0] not in neigh
            ) and k != self.id:
                self.remove_route(k)

    def update_dv(self, routable, w, via, me):
        # If any of my routes go through via, we can remove them
        for dest in list(self.routes.keys()):
            if self.get_seq(dest) == via:
                self.remove_route(dest)

        for dest in routable.get_routes():
            d = routable.get_distance(dest)
            # This route goes through myself, I don't need to learn from it
            if routable.get_seq(dest) == me:
                continue
            self.add_route(dest, w + d, via)

    def get_table_as_list(self):
        return [
            (node, next_hop[0], str(next_hop[1]))
            for node, next_hop in self.routes.items()
        ]
