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
