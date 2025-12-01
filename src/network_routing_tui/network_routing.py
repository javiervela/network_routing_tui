import re
from enum import Enum

from network_routing_tui.graph import Graph
from network_routing_tui.routing_table import RoutingTable
from network_routing_tui.exceptions import NodeDoesNotExistError


class NetworkRoutingCommand(Enum):
    ADD_EDGE = "add_edge"
    REMOVE_EDGE = "remove_edge"
    LINK_STATE = "link_state"
    DISTANCE_VECTOR = "distance_vector"
    SHOW = "show"
    SAVE_GRAPH = "save_graph"
    SAVE_ROUTING_TABLE = "save_routing_table"
    PRINT_ROUTING_TABLE = "print_routing_table"
    CLEAR = "clear"
    LOAD = "load"
    HELP = "help"
    QUIT = "quit"


class NetworkRouting:
    RE_ADD_EDGE = re.compile(r"([A-Z])\s+([A-Z])\s+(\d+)")
    RE_REMOVE_EDGE = re.compile(r"([A-Z])\s+([A-Z])\s+-")
    RE_LINK_STATE = re.compile(r"ls\s+([A-Z])")
    RE_DISTANCE_VECTOR = re.compile(r"dv\s+([A-Z])")
    RE_SAVE_GRAPH = re.compile(r"saveg\s+(\S+)")
    RE_SAVE_ROUTING_TABLE = re.compile(r"savert\s+([A-Z])\s+(\S+)")
    RE_PRINT_ROUTING_TABLE = re.compile(r"print\s+([A-Z])")
    RE_CLEAR = re.compile(r"clear")
    RE_LOAD = re.compile(r"load\s+(\S+)")
    RE_HELP = re.compile(r"help")
    RE_QUIT = re.compile(r"(quit|exit)")
    RE_SHOW = re.compile(r"show")

    HELP_TEXT = (
        "Available commands:\n\n"
        "ADD EDGE:            'X Y COST'        - Add an edge (nodes X and Y) with COST.\n"
        "REMOVE EDGE:         'X Y -'           - Remove the edge between nodes X and Y.\n"
        "LINK-STATE:          'ls X'            - Execute the link-state algorithm for node X.\n"
        "DISTANCE-VECTOR:     'dv X'            - Execute one iteration of the distance-vector algorithm.\n"
        "SHOW:                'show'            - Display the graph.\n"
        "SAVE GRAPH:          'saveg FILENAME'  - Save the graph to a file named FILENAME.\n"
        "SAVE ROUTING TABLE:  'savert FILENAME' - Save the routing table to a file named FILENAME.\n"
        "PRINT ROUTING TABLE: 'print NODE'      - Print the routing table for node NODE.\n"
        "CLEAR:               'clear'           - Clear the graph.\n"
        "LOAD:                'load FILENAME'   - Load a graph from a file named FILENAME.\n"
        "HELP:                'help'            - Show this help message.\n"
        "QUIT:                'quit' or 'exit'  - Exit the CLI.\n"
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
        if not self.graph.has_node(node):
            raise NodeDoesNotExistError(f"Node {node} does not exist in the graph.")
        self.graph.distance_vector()

    def show(self):
        self.graph.show()

    def clear(self):
        self.graph.clear()

    def print_routing_table(self, node):
        if not self.graph.has_node(node):
            raise NodeDoesNotExistError(f"Node {node} does not exist in the graph.")
        rt = self.graph.get_routing_table(node)
        print(rt.show())

    def apply_input(self, inp):
        # TODO do something about this method
        inp = inp.split(" ")  # TODO Should be 3 values

        if inp[2] == "-":
            self.graph.remove_edge(inp[0], inp[1])
        else:
            self.graph.add_edge(inp[0], inp[1], weight=int(inp[2]))

    def load(self, filename):
        # TODO do something about this method
        with open(filename) as f:
            l = f.readline()
            while l != "":
                self.apply_input(l)
                l = f.readline()

    def save_graph(self, filename):
        # TODO implement
        with open(filename, "w", encoding="utf-8") as f:
            for u, v, weight in self.graph.edges.data("weight"):
                f.write(str(u) + " " + str(v) + " " + str(weight) + "\n")

    def save_routing_table(self, node, filename):
        with open(filename, "w", encoding="utf-8") as f:
            rt = self.graph.get_routing_table(node)
            if rt is None:
                print(f"No routing table found for node {node}.\n")
            else:
                f.write(rt.show())

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
        elif m := self.RE_SHOW.fullmatch(cmd):
            return (NetworkRoutingCommand.SHOW, ())
        elif m := self.RE_SAVE_GRAPH.fullmatch(cmd):
            filename = m.group(1)
            return (NetworkRoutingCommand.SAVE_GRAPH, (filename,))
        elif m := self.RE_SAVE_ROUTING_TABLE.fullmatch(cmd):
            node, filename = m.group(1), m.group(2)
            return (NetworkRoutingCommand.SAVE_ROUTING_TABLE, (node, filename))
        elif m := self.RE_PRINT_ROUTING_TABLE.fullmatch(cmd):
            node = m.group(1)
            return (NetworkRoutingCommand.PRINT_ROUTING_TABLE, (node,))
        elif m := self.RE_CLEAR.fullmatch(cmd):
            return (NetworkRoutingCommand.CLEAR, ())
        elif m := self.RE_LOAD.fullmatch(cmd):
            filename = m.group(1)
            return (NetworkRoutingCommand.LOAD, (filename,))
        elif m := self.RE_HELP.fullmatch(cmd):
            return (NetworkRoutingCommand.HELP, ())
        elif m := self.RE_QUIT.fullmatch(cmd):
            return (NetworkRoutingCommand.QUIT, ())
        else:
            return (None, None)


# TODO save and load methods for graph and routing tables
# TODO add file autocompletion
