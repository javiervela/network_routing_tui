import re

from rich_pixels import Pixels
from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import (
    Button,
    DataTable,
    Footer,
    Header,
    Input,
    Label,
    Static,
    Tab,
    Tabs,
)

from network_routing_tui.graph import Graph


class FilenamePopup(ModalScreen[str | None]):
    def __init__(self):
        super().__init__()
        self.filename: str | None = None
        print("FilenamePopup initialized")

    def compose(self):
        yield Vertical(
            Label("Enter filename:"),
            Input(id="input"),
            Horizontal(
                Button("OK", id="ok", variant="success"),
                Button("Cancel", id="cancel", variant="error"),
            ),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed):
        input_box = self.query_one("#input", Input)

        if event.button.id == "ok":
            self.dismiss(input_box.value.strip() or None)
        else:
            self.dismiss(None)


class LayoutApp(App):
    CSS_PATH = "layout.css"

    TITLE = "Network Routing"
    # TODO better subtitle
    SUB_TITLE = "Interactive Network Topology — Routing Visualization"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.graph: Graph | None = None
        self.previous_tab_ids = []

    def on_mount(self) -> None:
        self.graph = Graph()
        self._refresh_graph()

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

    def _update_tabs(self):
        current_tab_ids = [id for id in self.graph.nodes]
        to_add_tab_ids = [
            id for id in current_tab_ids if id not in self.previous_tab_ids
        ]
        to_remove_tab_ids = [
            id for id in self.previous_tab_ids if id not in current_tab_ids
        ]

        tabs = self.query_one(Tabs)
        for tab_id in to_remove_tab_ids:
            tabs.remove_tab(tab_id)

        for tab_id in to_add_tab_ids:
            tabs.add_tab(Tab(tab_id, id=tab_id))

        self.previous_tab_ids = current_tab_ids

    def _update_table_for_node(self, node):
        table = self.query_one(DataTable)
        if not table.columns:
            # COLUMNS = ["Destination", "Via/Next-Hop", "Cost"]
            COLUMNS = ["Dest.", "Via", "Cost"]
            table.add_columns(*COLUMNS)

        table.clear()
        table.zebra_stripes = True
        if not node:
            return
        routing_table = self._get_routing_table(node)
        if routing_table:
            table.add_rows(routing_table)

    def _refresh_graph(self):
        # Update graph image
        graph_widget = self.query_one("#graph_view_pane", Static)
        graph_widget.update(self._get_graph_image(self.app.size))

        # Update node tabs
        tabs = self.query_one(Tabs)
        self._update_tabs()

        # Update routing table
        node = tabs.active_tab.id if tabs.active_tab else None
        self._update_table_for_node(node)

        # TODO maybe other components

    def _command_show(self) -> None:
        print("Command 'show' called")
        if self.graph is None:
            return
        self.graph.show()

    @work
    async def _command_export(self, filename=None) -> None:
        print("Command 'export' called")
        if not filename:
            filename = await self.push_screen_wait(FilenamePopup())
        if not filename:
            self.notify("Export cancelled", severity="warning")
            return
        if self.graph is None:
            return
        self.graph.save_file(filename)
        self.notify(f"Graph exported successfully to {filename}")

    def _command_clear(self) -> None:
        print("Command 'clear' called")
        if self.graph is None:
            return
        self.graph.clear()
        self.notify("Graph cleared successfully")
        self._refresh_graph()

    @work
    async def _command_load(self, filename=None) -> None:
        print("Command 'load' called")
        if not filename:
            filename = await self.push_screen_wait(FilenamePopup())
        if not filename:
            self.notify("Load cancelled", severity="warning")
            return
        if self.graph is None:
            return
        self.graph.load_file(filename)
        self.notify(f"Graph loaded successfully from {filename}")
        self._refresh_graph()

    def _execute_command(self, cmd: str) -> None:
        # Edge add/update: "X Y cost"  (cost is integer)
        m = re.fullmatch(r"([A-Z])\s+([A-Z])\s+(\d+)", cmd)
        if m:
            x, y, cost = m.group(1), m.group(2), int(m.group(3))
            print(f"Adding/updating edge {x} {y} with cost {cost}")
            self.graph.add_edge(x, y, cost)
            self._refresh_graph()
            return

        # Edge remove: "X Y -"
        m = re.fullmatch(r"([A-Z])\s+([A-Z])\s+-", cmd)
        if m:
            x, y = m.group(1), m.group(2)
            print(f"Removing edge {x} {y}")
            self.graph.remove_edge(x, y)
            self._refresh_graph()
            return

        # Link-state: "ls X"
        m = re.fullmatch(r"ls\s+([A-Z])", cmd)
        if m:
            node = m.group(1)
            print(f"Link-state algorithm initiated for node {node}")
            self.graph.link_state(node)
            self._refresh_graph()
            return

        # Distance-vector iteration then show X: "dv X"
        m = re.fullmatch(r"dv\s+([A-Z])", cmd)
        if m:
            node = m.group(1)
            print(f"Distance-vector iteration initiated for node {node}")
            self.graph.distance_vector()
            # TODO for 1 specific node: switch tab to it
            # TODO check rest of implementation specs
            self._refresh_graph()
            return

        # Convenience commands
        if cmd == "clear":
            self._command_clear()
            return

        if cmd == "show":
            self._command_show()
            return

        if cmd.startswith("export "):
            filename = cmd.split(" ", 1)[1]
            self._command_export(filename)
            return

        if cmd.startswith("load "):
            # TODO implement and test
            filename = cmd.split(" ", 1)[1]
            self._command_load(filename)
            return

        # Warn in input
        self.notify(f"Unrecognized command: {cmd}", severity="error")

    def compose(self) -> ComposeResult:
        yield Header(id="Header")
        with Vertical(id="app_pane"):
            with Horizontal(id="visualization_pane"):
                with Vertical(id="left_visualization_pane", classes="left_pane"):
                    yield Static("Routing Tables", id="routing_tables_title")
                    yield Tabs(name="Nodes", id="node_tabs")
                    yield DataTable(id="routing_table", classes="routing_table_pane")
                with Vertical(id="right_visualization_pane", classes="right_pane"):
                    yield Static(
                        self._get_graph_image(self.app.size),
                        id="graph_view_pane",
                        classes="graph_view_pane",
                    )
            with Horizontal(id="command_pane"):
                with Vertical(id="left_command_pane", classes="left_pane"):
                    yield Input(
                        placeholder="Command Input",
                        id="command_input",
                        classes="command_input",
                    )
                with Vertical(id="right_command_pane", classes="right_pane"):
                    with Horizontal():
                        yield Button("Load", id="button_load", classes="button")
                        yield Button("Export", id="button_export", classes="button")
                        yield Button("Clear", id="button_clear", classes="button")
                        yield Button("Show", id="button_show", classes="button")
        yield Footer(id="Footer")

    def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:
        node = event.tab.id
        self._update_table_for_node(node)

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "button_show":
            self._command_show()
        elif button_id == "button_export":
            self._command_export()
        elif button_id == "button_clear":
            self._command_clear()
        elif button_id == "button_load":
            self._command_load()

    @on(Input.Submitted, "#command_input")
    def handle_command_submit(self, event: Input.Submitted) -> None:
        cmd = event.value.strip()
        if not cmd:
            return
        self._execute_command(cmd)
        event.input.value = ""


def main():
    app = LayoutApp()
    app.run()


if __name__ == "__main__":
    main()


# TODO implement --cli flag to run without TUI
# TODO add warnings and errors
