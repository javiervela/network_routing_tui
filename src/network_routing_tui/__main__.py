from rich_pixels import Pixels
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, HorizontalScroll
from textual.widgets import (
    Button,
    DataTable,
    Footer,
    Header,
    Static,
    Tab,
    Tabs,
)
from textual.reactive import reactive

from network_routing_tui.graph import Graph


class LayoutApp(App):
    CSS_PATH = "layout.css"

    TITLE = "Network Routing"
    # TODO better subtitle
    SUB_TITLE = "Interactive Network Topology — Routing Visualization"

    def on_mount(self) -> None:
        self.graph = Graph()
        self._load_test_graph()
        self.refresh_graph()

    def _load_test_graph(self):
        # TODO just for test
        self.graph.load_file("./tests/graph.txt")
        for _ in range(5):
            self.graph.distance_vector()

    def _get_tabs(self):
        if self.graph is None:
            return []
        return [Tab(name, id=name) for name in self.graph.nodes]

    def _get_routing_table(self, node):
        if self.graph is None:
            return []
        routing_table = self.graph.get_routing_table(node)
        if routing_table is None:
            return []
        return routing_table.get_table_as_list()

    def _get_graph_image(self, size):
        if self.graph is None:
            return None
        term_width, term_height = size
        img = self.graph.generate_image(int(term_width / 1.5), int(term_height * 1.6))
        return Pixels.from_image(img)

    def compose(self) -> ComposeResult:
        yield Header(id="Header")

        with Horizontal():
            with Vertical(id="left_pane"):
                yield Static("Routing Tables", id="routing_tables_title")

                with HorizontalScroll():
                    tabs = self._get_tabs()
                    yield Tabs(*tabs, name="Nodes", id="node_tabs", classes="node_tabs")

                yield DataTable(id="routing_table", classes="routing_table_pane")

            with Vertical(id="right_pane"):
                yield Static(
                    self._get_graph_image(self.app.size),
                    id="graph_view_pane",
                    classes="graph_view_pane",
                )

                with Horizontal():
                    yield Button("Show", id="button_show", classes="button")
                    yield Button("Export", id="button_export", classes="button")
                    yield Button("Clear", id="button_clear", classes="button")
                    yield Button(
                        "Load Test Graph", id="button_load_test", classes="button"
                    )

        yield Footer(id="Footer")

    def _update_table_for_node(self, node):
        print("HERHE HERE")
        table = self.query_one(DataTable)
        if not table.columns:
            # TODO make constants
            table.add_columns("Destination", "Via/Next-Hop", "Cost")

        table.clear()
        table.zebra_stripes = True
        if not node:
            return
        routing_table = self._get_routing_table(node)
        if routing_table:
            table.add_rows(routing_table)

    def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:
        """Handle TabActivated message sent by Tabs."""

        node = event.tab.id
        self._update_table_for_node(node)

    def refresh_graph(self):
        # Update graph image
        graph_widget = self.query_one("#graph_view_pane", Static)
        graph_widget.update(self._get_graph_image(self.app.size))

        # Update node tabs
        tabs = self.query_one("#node_tabs", Tabs)
        tabs.clear()
        for tab in self._get_tabs():
            tabs.add_tab(tab)

        # Update routing table
        node = tabs.active_tab.id if tabs.active_tab else None
        self._update_table_for_node(node)

        # TODO maybe other components

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "button_show":
            print("Show button pressed")
            self.graph.show()
        elif button_id == "button_export":
            print("Export button pressed")
            # TODO prompt where to save
            self.graph.save_file("./exported_graph.txt")
        elif button_id == "button_clear":
            print("Clear button pressed")
            self.graph.clear()
            self.refresh_graph()
        elif button_id == "button_load_test":
            print("Load Test Graph button pressed")
            self._load_test_graph()
            self.refresh_graph()


def main():
    app = LayoutApp()
    app.run()


if __name__ == "__main__":
    main()
