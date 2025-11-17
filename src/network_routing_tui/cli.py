from network_routing_tui.network_routing import NetworkRouting, NetworkRoutingCommand


class NetworkRoutingCLI:
    def __init__(self):
        self.network_routing = NetworkRouting()

    def print_help(self):
        print(self.network_routing.HELP_TEXT)

    def run(self):
        print("Network Routing CLI")
        print("Type 'help' for commands, 'quit' to exit.\n")

        while True:
            try:
                line = input("> ")
            except (EOFError, KeyboardInterrupt):
                print()
                break

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
            elif command == NetworkRoutingCommand.DISTANCE_VECTOR:
                node = params
                self.network_routing.distance_vector(node)
            elif command == NetworkRoutingCommand.SHOW:
                self.network_routing.show()
            elif command == NetworkRoutingCommand.SAVE_GRAPH:
                (filename,) = params
                self.network_routing.save(filename)
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
                break
            elif command is None:
                print(f"Unrecognized command: {cmd}\n")
