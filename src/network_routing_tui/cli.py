import warnings

from network_routing_tui.network_routing import NetworkRouting, NetworkRoutingCommand


class NetworkRoutingCLI:
    def __init__(self, script=None):
        self.network_routing = NetworkRouting()
        self.script = script

    def print_help(self):
        print(self.network_routing.HELP_TEXT)

    def run(self):
        print("Network Routing CLI")
        print("Type 'help' for commands, 'quit' to exit.\n")

        if self.script:
            with open(self.script, "r", encoding="utf-8") as f:
                for line in f:
                    print(f"> {line.strip()}")
                    self.execute_command(line)
        else:
            while True:
                try:
                    line = input("> ")
                except (EOFError, KeyboardInterrupt):
                    print()
                    break
                self.execute_command(line)

    def execute_command(self, line):
        try:
            with warnings.catch_warnings(record=True) as caught:
                cmd = line.strip()
                command, params = self.network_routing.parse_command(cmd)
                if command == NetworkRoutingCommand.ADD_EDGE:
                    x, y, cost = params
                    self.network_routing.add_edge(x, y, cost)
                elif command == NetworkRoutingCommand.REMOVE_EDGE:
                    x, y = params
                    self.network_routing.remove_edge(x, y)
                elif command == NetworkRoutingCommand.LINK_STATE:
                    node = params
                    self.network_routing.link_state(node)
                    self.network_routing.print_routing_table(node)
                elif command == NetworkRoutingCommand.DISTANCE_VECTOR:
                    node = params
                    self.network_routing.distance_vector(node)
                    self.network_routing.print_routing_table(node)
                elif command == NetworkRoutingCommand.SHOW:
                    self.network_routing.show()
                elif command == NetworkRoutingCommand.SAVE_GRAPH:
                    (filename,) = params
                    self.network_routing.save_graph(filename)
                elif command == NetworkRoutingCommand.SAVE_ROUTING_TABLE:
                    (node, filename) = params
                    self.network_routing.save_routing_table(node, filename)
                elif command == NetworkRoutingCommand.PRINT_ROUTING_TABLE:
                    (node,) = params
                    self.network_routing.print_routing_table(node)
                elif command == NetworkRoutingCommand.CLEAR:
                    self.network_routing.clear()
                elif command == NetworkRoutingCommand.LOAD:
                    (filename,) = params
                    self.network_routing.load(filename)
                elif command == NetworkRoutingCommand.HELP:
                    self.print_help()
                elif command == NetworkRoutingCommand.QUIT:
                    exit(0)
                elif command is None:
                    print(f"Error: Command '{cmd}' does not exist")
                for warning in caught:
                    print(f"Warning: {warning.message}")
        except Exception as e:
            print(f"Error: {e}")
