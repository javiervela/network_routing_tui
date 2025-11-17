import re
from enum import Enum

from network_routing_tui.graph import Graph
from network_routing_tui.routing_table import RoutingTable


class NetworkRoutingCommand(Enum):
    ADD_EDGE = "add_edge"
    REMOVE_EDGE = "remove-edge"
    LINK_STATE = "link_state"
    DISTANCE_VECTOR = "distance_vector"
    SHOW = "show"
    EXPORT = "export"
    CLEAR = "clear"
    LOAD = "load"
    HELP = "help"


class NetworkRouting:
    RE_ADD_EDGE = re.compile(r"([A-Z])\s+([A-Z])\s+(\d+)")
    RE_REMOVE_EDGE = re.compile(r"([A-Z])\s+([A-Z])\s+-")
    RE_LINK_STATE = re.compile(r"ls\s+([A-Z])")
    RE_DISTANCE_VECTOR = re.compile(r"dv\s+([A-Z])")

    HELP_TEXT = (
        "Available commands:\n"
        "1. ADD EDGE: 'X Y COST' - Add or update an edge between nodes X and Y with the given COST.\n"
        "2. REMOVE EDGE: 'X Y -' - Remove the edge between nodes X and Y.\n"
        "3. LINK-STATE: 'ls X' - Execute the link-state algorithm for node X.\n"
        "4. DISTANCE-VECTOR: 'dv X' - Execute one iteration of the distance-vector algorithm for node X.\n"
        "5. SHOW: 'show' - Display the current graph in the console.\n"
        "6. EXPORT: 'export FILENAME' - Export the current graph to a file named FILENAME.\n"
        "7. CLEAR: 'clear' - Clear the current graph.\n"
        "8. LOAD: 'load FILENAME' - Load a graph from a file named FILENAME.\n"
    )

    def __init__(self):
        self.graph = Graph()

    def get_routing_table(self, node):
        routing_table: RoutingTable = self.graph.get_routing_table(node)
        if routing_table is None:
            return []
        return routing_table.get_table_as_list()

    def add_edge(self, x, y, cost):
        self.graph.add_edge(x, y, cost)

    def remove_edge(self, x, y):
        self.graph.remove_edge(x, y)

    def link_state(self, node):
        self.graph.link_state(node)

    def distance_vector(self, node):
        self.graph.distance_vector()

    def show(self):
        self.graph.show()

    def export(self, filename):
        self.graph.save_file(filename)

    def clear(self):
        self.graph.clear()

    def load(self, filename):
        # TODO do something about this method
        with open(filename) as f:
            l = f.readline()
            while l != "":
                self.apply_input(l)
                l = f.readline()

    def apply_input(self, inp):
        # TODO do something about this method
        inp = inp.split(" ")  # TODO Should be 3 values

        if inp[2] == "-":
            self.remove_edge(inp[0], inp[1])
        else:
            self.add_edge(inp[0], inp[1], weight=int(inp[2]))

    def save_file(self, dest):
        # TODO do something about this method
        with open(dest, "w", encoding="utf-8") as f:
            for u, v, weight in self.edges.data("weight"):
                f.write(str(u) + " " + str(v) + " " + str(weight) + "\n")

    def parse_command(self, cmd):
        if m := self.RE_ADD_EDGE.fullmatch(cmd):
            x, y, cost = m.group(1), m.group(2), int(m.group(3))
            return (NetworkRoutingCommand.ADD_EDGE, (x, y, cost))
        elif m := self.RE_REMOVE_EDGE.fullmatch(cmd):
            x, y = m.group(1), m.group(2)
            return (NetworkRoutingCommand.REMOVE_EDGE, (x, y))
        elif m := self.RE_LINK_STATE.fullmatch(cmd):
            node = m.group(1)
            return (NetworkRoutingCommand.LINK_STATE, (node))
        elif m := self.RE_DISTANCE_VECTOR.fullmatch(cmd):
            node = m.group(1)
            return (NetworkRoutingCommand.DISTANCE_VECTOR, (node))
        elif cmd == "show":
            return (NetworkRoutingCommand.SHOW, ())
        elif cmd.startswith("export "):
            filename = cmd.split(" ", 1)[1]
            return (NetworkRoutingCommand.EXPORT, (filename,))
        elif cmd == "clear":
            return (NetworkRoutingCommand.CLEAR, ())
        elif cmd.startswith("load "):
            filename = cmd.split(" ", 1)[1]
            return (NetworkRoutingCommand.LOAD, (filename,))
        elif cmd == "help":
            return (NetworkRoutingCommand.HELP, ())
        else:
            return (None, None)
