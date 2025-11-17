import argparse

from network_routing_tui.tui import NetworkRoutingTUI
from network_routing_tui.cli import NetworkRoutingCLI


def main():
    parser = argparse.ArgumentParser(description="Run Network Routing TUI or CLI")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--tui", action="store_true", help="Run TUI (default)")
    group.add_argument("--cli", action="store_true", help="Run CLI")
    parser.add_argument(
        "--script",
        "-s",
        metavar="FILE",
        help="Script file to pass to CLI (only with --cli)",
    )
    args = parser.parse_args()

    if args.script and not args.cli:
        parser.error("--script can only be used with --cli")

    if args.cli:
        NetworkRoutingCLI(script=args.script).run()
    else:
        NetworkRoutingTUI().run()


if __name__ == "__main__":
    main()
