import argparse

from network_routing_tui.tui import NetworkRoutingTUI
from network_routing_tui.cli import NetworkRoutingCLI


def main():
    parser = argparse.ArgumentParser(description="Run Network Routing TUI or CLI")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--tui", action="store_true", help="Run TUI (default)")
    group.add_argument("--cli", action="store_true", help="Run CLI")
    args = parser.parse_args()

    if args.cli:
        NetworkRoutingCLI().run()
    else:
        NetworkRoutingTUI().run()


if __name__ == "__main__":
    main()
