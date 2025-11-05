import networkx as nx
from network_routing_tui import error
from network_routing_tui.routing_table import RoutingTable


class Graph(nx.Graph):
    def apply_input(self, inp):
        inp = inp.split(" ")  # Should be 3 values

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
            self.add_node(u, routable=RoutingTable(u))

    def load_file(self, src):
        with open(src) as f:
            l = f.readline()
            while l != "":
                self.apply_input(l)
                l = f.readline()

    def save_file(self, dest):
        with open(dest, "w", encoding="utf-8") as f:
            for u, v, weight in self.edges.data("weight"):
                f.write(str(u) + " " + str(v) + " " + str(weight) + "\n")

    def distance_vector(self):
        routes = {}
        for n in self.nodes:
            routes[n] = self.nodes[n]["routable"].copy()

        for n in self.nodes:
            for v in self.neighbors(n):
                w = self.get_edge_data(n, v, "weight")["weight"]
                self.nodes[n]["routable"].update_dv(routes[v], w)

    def draw(self, seed=7):
        pos = nx.spring_layout(self, seed=seed)

        nx.draw_networkx_nodes(self, pos, node_size=700)
        nx.draw_networkx_edges(self, pos, width=4)
        nx.draw_networkx_labels(self, pos, font_size=20, font_family="sans-serif")

        edge_labels = nx.get_edge_attributes(self, "weight")
        nx.draw_networkx_edge_labels(self, pos, edge_labels, rotate=False)

    def print_table(self, n):
        print(self.nodes[n]["routable"].show())
