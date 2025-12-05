import io
import warnings

from PIL import Image
import matplotlib.pyplot as plt
import networkx as nx

from network_routing_tui.routing_table import RoutingTable
from network_routing_tui.link_state import link_state
from network_routing_tui.exceptions import (
    EdgeDoesNotExistError,
    EdgeOverwriteWarning,
    NodeDoesNotExistError,
    NodeDoesNotExistWarning,
    RemovingEdgeWarning,
)


class Graph(nx.Graph):
    # REMOVE duplicate code with NetworkRouting? keep it for testing purposes
    def apply_input(self, inp):
        inp = inp.split(" ")  # Should be 3 values
        if inp[2] == "-":
            self.remove_edge(inp[0], inp[1])
        else:
            self.add_edge(inp[0], inp[1], weight=int(inp[2]))

    # REMOVE duplicate code with NetworkRouting? keep it for testing purposes
    def load_file(self, src):
        with open(src) as f:
            l = f.readline()
            while l != "":
                self.apply_input(l)
                l = f.readline()

    # REMOVE duplicate code with NetworkRouting? keep it for testing purposes
    def save_file(self, dest):
        with open(dest, "w", encoding="utf-8") as f:
            for u, v, weight in self.edges.data("weight"):
                f.write(str(u) + " " + str(v) + " " + str(weight) + "\n")

    def remove_edge(self, u, v):
        # remove edge if exists, else warn
        if self.has_edge(u, v):
            super().remove_edge(u, v)
        else:
            warnings.warn(
                f"No edges to remove between {u} and {v}.",
                EdgeDoesNotExistError,
            )
            return

        # remove nodes if they have no remaining edges
        if self.degree(u) == 0:
            # print("Removing node " + u + " as it has no remaining edges.")
            self.remove_node(u)
            warnings.warn(
                f"Node {u} has no remaining edges and was removed.",
                RemovingEdgeWarning,
            )
        if self.degree(v) == 0:
            # print("Removing node " + v + " as it has no remaining edges.")
            self.remove_node(v)
            warnings.warn(
                f"Node {v} has no remaining edges and was removed.",
                RemovingEdgeWarning,
            )

    def add_edge(self, u, v, weight):
        # create nodes if they don't exist
        if not self.has_node(u):
            self.add_node(u, routable=RoutingTable(u))
            warnings.warn(
                f"Node {u} did not exist and was created.",
                NodeDoesNotExistWarning,
            )
        if not self.has_node(v):
            self.add_node(v, routable=RoutingTable(v))
            warnings.warn(
                f"Node {v} did not exist and was created.",
                NodeDoesNotExistWarning,
            )
        # warn if edge exists
        if self.has_edge(u, v):
            warnings.warn(
                f"Edge between {u} and {v} is being overwritten. (previous weight: {self.get_edge_data(u, v)['weight']}, new weight: {weight})",
                EdgeOverwriteWarning,
            )
        # add edge
        return super().add_edge(u, v, weight=weight)

    def get_neighbors_distance(self, u):
        res = []
        for v in self.neighbors(u):
            w = self.get_edge_data(u, v, "weight")["weight"]
            res.append([v, w, v])
        res.sort(key=lambda edge: edge[1])
        return res

    def get_routing_table(self, n):
        if not self.has_node(n):
            return None
        return self.nodes[n]["routable"]

    def distance_vector(self, legacy = False):
        routes = {}
        for n in self.nodes:
            routes[n] = self.nodes[n]["routable"].copy()

        for n in self.nodes:
            self.nodes[n]["routable"] = RoutingTable(n)
            # self.nodes[n]["routable"].remove_neighbors(self.neighbors(n))
            for v in self.neighbors(n):
                w = self.get_edge_data(n, v, "weight")["weight"]
                self.nodes[n]["routable"].update_dv(routes[v], w, v, n, legacy)

    def send_msg(self, src, dest, rec_max=200):
        """
        Recursive function to obtain the distance from src to dest using the routing tables.

        Returns -1 if the message cannot reach the destination within rec_max hops.
        """
        if src == dest:
            return 0
        if rec_max == 0:
            return -1
        rT = self.nodes[src]["routable"]
        via = rT.get_seq(dest)
        if via == "ERROR" or not self.has_edge(src, via):
            return -1

        res = self.send_msg(via, dest, rec_max - 1)
        if res == -1:
            return -1
        return res + self.get_edge_data(src, via, "weight")["weight"]

    def distance_vector_legacy(self):
        routes = {}
        for n in self.nodes:
            routes[n] = self.nodes[n]["routable"].copy()

        for n in self.nodes:
            self.nodes[n]["routable"] = RoutingTable(n)
            # self.nodes[n]["routable"].remove_neighbors(self.neighbors(n))
            for v in self.neighbors(n):
                w = self.get_edge_data(n, v, "weight")["weight"]
                self.nodes[n]["routable"].update_dv(routes[v], w, v, n, True)

    def link_state(self, node):
        if not self.has_node(node):
            raise NodeDoesNotExistError(f"Node {node} does not exist in the graph.")
        resR = link_state(self, node)
        self.nodes[node]["routable"] = resR

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

    def generate_image(self, width_px: int, height_px: int, dpi=30) -> Image.Image:
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

    def show(self):
        self.draw()
        plt.show()
