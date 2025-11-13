import io

from PIL import Image
import matplotlib.pyplot as plt
import networkx as nx

from network_routing_tui import error
from network_routing_tui.routing_table import RoutingTable


class Graph(nx.Graph):
    def apply_input(self, inp):
        # TODO will deprecate in favor of __main__ implementation
        inp = inp.split(" ")  # Should be 3 values

        if inp[2] == "-":
            self.remove_edge(inp[0], inp[1])
        else:
            self.add_edge(inp[0], inp[1], weight=int(inp[2]))

    def remove_edge(self, u, v):
        # remove edge if exists, else warn
        if self.has_edge(u, v):
            super().remove_edge(u, v)
        else:
            error.warning("No edges to remove between " + u + " and " + v)
        # remove nodes if they have no remaining edges
        if self.degree(u) == 0:
            print("Removing node " + u + " as it has no remaining edges.")
            self.remove_node(u)
        if self.degree(v) == 0:
            print("Removing node " + v + " as it has no remaining edges.")
            self.remove_node(v)

    def add_edge(self, u, v, weight):
        # create nodes if they don't exist
        if not self.has_node(u):
            self.add_node(u, routable=RoutingTable(u))
        if not self.has_node(v):
            self.add_node(v, routable=RoutingTable(v))
        # add edge
        return super().add_edge(u, v, weight=weight)

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

    def get_neighbors_distance(self, u):
        res = []
        for v in self.neighbors(u):
            w = self.get_edge_data(u, v, "weight")["weight"]
            res.append([v, w, u])
        res.sort(key=lambda edge: edge[1])
        return res

    def distance_vector(self):
        routes = {}
        for n in self.nodes:
            routes[n] = self.nodes[n]["routable"].copy()

        for n in self.nodes:
            self.nodes[n]["routable"].remove_neighbors()
            for v in self.neighbors(n):
                w = self.get_edge_data(n, v, "weight")["weight"]
                self.nodes[n]["routable"].update_dv(routes[v], w, v)

    def draw(self, tui=False, seed=7):
        pos = nx.spring_layout(self, seed=seed)

        nx.draw_networkx_nodes(
            self,
            pos,
            node_size=600 if tui else 700,
            node_color="skyblue" if tui else "#1f78b4",
        )
        nx.draw_networkx_edges(
            self,
            pos,
            width=4,
            edge_color="gray" if tui else "k",
        )
        nx.draw_networkx_labels(
            self,
            pos,
            font_size=20,
            font_family="sans-serif",
        )

        if not tui:
            edge_labels = nx.get_edge_attributes(self, "weight")
            nx.draw_networkx_edge_labels(self, pos, edge_labels, rotate=False)

    def show(self):
        self.draw()
        plt.show()

    def print_table(self, n):
        print(self.get_routing_table(n).show())

    def get_routing_table(self, n):
        if not self.has_node(n):
            return None
        return self.nodes[n]["routable"]

    def generate_image(self, width_px: int, height_px: int, dpi=30) -> Image.Image:
        # TODO make this use self.draw()
        pos = nx.spring_layout(self, seed=42)
        fig_w, fig_h = width_px / dpi, height_px / dpi
        fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
        fig.patch.set_facecolor("none")
        ax.set_axis_off()
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

        self.draw(tui=True)

        buf = io.BytesIO()
        fig.savefig(
            buf, format="png", transparent=True, bbox_inches="tight", pad_inches=0
        )
        plt.close(fig)
        buf.seek(0)
        img = Image.open(buf).convert("RGBA")
        return img
