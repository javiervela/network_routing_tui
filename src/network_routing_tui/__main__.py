from rich_pixels import Pixels
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, HorizontalScroll
from textual.widgets import Placeholder, Header, Footer, Static, Tabs, Tab, DataTable

from network_routing_tui.graph import Graph


class LayoutApp(App):
    CSS_PATH = "layout.css"

    TITLE = "Network Routing"
    SUB_TITLE = (
        "Interactive Network Topology — Routing Visualization"  # TODO make better
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.graph = Graph()

        # TODO just for test
        self.graph.load_file("./tests/graph.txt")
        for _ in range(5):
            self.graph.distance_vector()

    def compose(self) -> ComposeResult:
        yield Header(id="Header")

        with Horizontal():
            with Vertical(id="left_pane"):
                yield Static("Routing Tables", id="routing_tables_title")

                with HorizontalScroll():
                    tabs = [Tab(name, id=name) for name in self.graph.nodes]
                    yield Tabs(*tabs, name="Nodes", id="node_tabs", classes="node_tabs")

                yield DataTable(id="routing_table", classes="routing_table_pane")

            with Vertical(id="right_pane"):
                term_width, term_height = self.app.size
                graph_image = self.graph.generate_image(
                    int(term_width / 1.5), int(term_height * 1.6)
                )
                yield Static(
                    Pixels.from_image(graph_image),
                    id="graph_view_pane",
                    classes="graph_view_pane",
                )

                with Horizontal():
                    yield Placeholder(id="button_SHOW", classes="button")
                    yield Placeholder(id="button_EXPORT", classes="button")
                    yield Placeholder(id="button_CLEAR", classes="button")

        yield Footer(id="Footer")

    def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:
        """Handle TabActivated message sent by Tabs."""
        node = event.tab.id
        print(f"Activated tab: {node}")
        routing_table = self.graph.get_routing_table(node).get_table_as_list()

        table = self.query_one(DataTable)
        if not table.columns:
            table.add_columns(
                "Destination", "Via/Next-Hop", "Cost"
            )  # TODO make constants

        table.clear()
        table.add_rows(routing_table[1:])
        table.zebra_stripes = True


def main():
    app = LayoutApp()
    app.run()


if __name__ == "__main__":
    main()
