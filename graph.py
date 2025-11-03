import networkx as nx
import matplotlib.pyplot as plt
import error

class RoutingTable():
    
    def __init__(self, n):
        self.id = n
        self.routes = {}
        self.routes[n] = [n, 0]

    def show(self):
        res = ""
        for r in self.routes:
            m = self.routes[r][0]
            if r == m:
                m = "-"
            res += r + " " + m + " " + str(self.routes[r][1]) + "\n"
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
            self.routes[n] = [seq,w]

    def update_dv(self, routable, w):
        for dest in routable.get_routes():
            d = routable.get_distance(dest)
            if d == 0:
                seq = self.id
            else:
                seq = routable.get_seq(dest)
            self.add_route(dest, w + d, seq)
    

    

class Graph(nx.Graph):

    def apply_input(self,inp):
        inp = inp.split(" ") # Should be 3 values

        if inp[2] == "-":
            if self.has_edge(inp[0], inp[1]):
                self.remove_edge(inp[0], inp[1])
            else:
                error.warning("No edges to remove between " + inp[0] + " and " + inp[1])            
        else:
            self.create_if_needed(inp[0])
            self.create_if_needed(inp[1])
            self.add_edge(inp[0], inp[1], weight=int(inp[2]))

    def create_if_needed(self, u):
        if not self.has_node(u):
            self.add_node(u, routable = RoutingTable(u))

    def load_file(self, src):
        with open(src) as f:
            l = f.readline()
            while l != "":
                self.apply_input(l)
                l = f.readline()

    def save_file(self, dest):
        with open(dest, "w", encoding="utf-8") as f:
            for u, v, weight in G.edges.data("weight"):
                f.write(str(u) + " " + str(v) + " " + str(weight) + "\n")

    def distance_vector(self):
        routes = {}
        for n in self.nodes:
            routes[n] = self.nodes[n]["routable"].copy()

        for n in self.nodes:
            for v in self.neighbors(n):
                w = self.get_edge_data(n,v,"weight")["weight"]
                self.nodes[n]["routable"].update_dv(routes[v], w)

    def draw(self, seed = 7):
        pos = nx.spring_layout(self, seed=seed)
        
        nx.draw_networkx_nodes(self, pos, node_size=700)
        nx.draw_networkx_edges(self, pos, width=4)
        nx.draw_networkx_labels(self, pos, font_size=20, font_family="sans-serif")

        edge_labels = nx.get_edge_attributes(self, "weight")
        nx.draw_networkx_edge_labels(self, pos, edge_labels, rotate=False)

    def print_table(self,n):
        print(self.nodes[n]["routable"].show())

if __name__ == "__main__":

    G = Graph()

    #G.apply_input("H E 200")
    G.load_file("graph.txt")
    #G.apply_input("C H -")
    #G.apply_input("C H -")

    G.save_file("test.txt")
    for i in range(5):
        print("-------")
        G.distance_vector()
        G.print_table("A")
    
    G.draw(1)
    plt.show()
