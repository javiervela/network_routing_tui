import warnings

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

from network_routing_tui.network_routing import NetworkRouting, NetworkRoutingCommand
from network_routing_tui.exceptions import CommandDoesNotExistError


class HelpPopup(ModalScreen):
    def compose(self):
        yield Vertical(
            Static(NetworkRouting.HELP_TEXT, id="help_text"),
            Button("Close", id="close", variant="primary"),
            id="help_dialog",
        )

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "close":
            self.dismiss()


class FilenamePopup(ModalScreen[str | None]):
    def __init__(self, default_value=None):
        super().__init__()
        self.filename: str | None = None
        self.default_value = default_value
        print("FilenamePopup initialized")

    def compose(self):
        yield Vertical(
            Label("Enter filename:"),
            Input(id="input", value=self.default_value),
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


class NetworkRoutingTUI(App):
    CSS_PATH = "layout.css"

    TITLE = "Network Routing"
    SUB_TITLE = "Interactive Network Topology — Routing Visualization"

    LOAD_DEFAULT_FILENAME = "./tests/graph.txt"
    SAVE_GRAPH_DEFAULT_FILENAME = "./tests/test.txt"

    def __init__(self, log_level="WARNING", **kwargs):
        super().__init__(**kwargs)
        self.network_routing: NetworkRouting | None = None
        self.log_level = log_level
        self.previous_tab_ids = []

    ###########################################################################
    # TUI Layout
    ###########################################################################

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
                        yield Button(
                            "Save Graph", id="button_save_graph", classes="button"
                        )
                        yield Button("Clear", id="button_clear", classes="button")
                        yield Button("Show", id="button_show", classes="button")
        yield Footer(id="Footer")

    ###########################################################################
    # Event Handlers
    ###########################################################################

    def on_mount(self) -> None:
        self.network_routing = NetworkRouting()
        self._refresh_graph()

    def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:
        node = event.tab.id
        self._update_table_for_node(node)

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "button_show":
            self._command_show()
        elif button_id == "button_save_graph":
            self._command_save_graph()
        # TODO implement save routing table button
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

    ###########################################################################
    # Command Handlers
    ###########################################################################

    def _command_add_edge(self, x, y, cost) -> None:
        self.network_routing.add_edge(x, y, cost)
        self._refresh_graph()
        self.notify(f"Edge {x} {y} with cost {cost} added/updated")

    def _command_remove_edge(self, x, y) -> None:
        self.network_routing.remove_edge(x, y)
        self._refresh_graph()
        self.notify(f"Edge {x} {y} removed")

    def _command_link_state(self, node) -> None:
        self.network_routing.link_state(node)
        tabs = self.query_one(Tabs)
        tabs.active = node
        self._refresh_graph()
        self.notify(f"Link-state algorithm executed for node {node}")

    def _command_distance_vector(self, node) -> None:
        self.network_routing.distance_vector(node)
        tabs = self.query_one(Tabs)
        tabs.active = node
        self._refresh_graph()
        self.notify(f"Distance-vector iteration executed for node {node}")

    def _command_show(self) -> None:
        if self.network_routing is not None:
            self.network_routing.show()

    @work
    async def _command_save_graph(self, filename=None) -> None:
        if not filename:
            filename = await self.push_screen_wait(
                FilenamePopup(default_value=self.SAVE_GRAPH_DEFAULT_FILENAME)
            )
        if not filename:
            self.notify("Save Graph cancelled", severity="warning")
            return
        if self.network_routing is None:
            return
        try:
            self.network_routing.save_graph(filename)
            self.notify(f"Graph saved successfully to {filename}")
        except Exception as e:
            self.notify(f"Error saving graph: {e}", severity="error")

    @work
    async def _command_save_routing_table(self, node=None, filename=None) -> None:
        # This method is only used through command, there is not a button for it yet
        # Therefore, we assume node and filename are always provided and we do not need a popup to ask for them

        # if not filename:
        #     filename = await self.push_screen_wait(
        #         FilenamePopup(default_value=f"{node}_routing_table.txt")
        #     )
        # if not filename:
        #     self.notify("Save Routing Table cancelled", severity="warning")
        #     return

        if self.network_routing is None:
            return
        try:
            self.network_routing.save_routing_table(node, filename)
            self.notify(
                f"Routing table for node {node} saved successfully to {filename}"
            )
        except Exception as e:
            self.notify(f"Error saving routing table: {e}", severity="error")

    def _command_clear(self) -> None:
        if self.network_routing is None:
            return
        self.network_routing.clear()
        self.notify("Graph cleared successfully")
        self._refresh_graph()

    @work
    async def _command_load(self, filename=None) -> None:
        if not filename:
            filename = await self.push_screen_wait(
                FilenamePopup(default_value=self.LOAD_DEFAULT_FILENAME)
            )
        if not filename:
            self.notify("Load cancelled", severity="warning")
            return
        if self.network_routing is None:
            return
        try:
            self.network_routing.load(filename)
            self.notify(f"Graph loaded successfully from {filename}")
        except Exception as e:
            self.notify(f"Error loading graph: {e}", severity="error")
        self._refresh_graph()

    def _command_help(self) -> None:
        self.push_screen(HelpPopup())

    ###########################################################################
    # Command Execution
    ###########################################################################

    def _execute_command(self, cmd: str) -> None:
        try:
            with warnings.catch_warnings(record=True) as caught:
                command, params = self.network_routing.parse_command(cmd)
                if command == NetworkRoutingCommand.ADD_EDGE:
                    x, y, cost = params
                    self._command_add_edge(x, y, cost)
                elif command == NetworkRoutingCommand.REMOVE_EDGE:
                    x, y = params
                    self._command_remove_edge(x, y)
                elif command == NetworkRoutingCommand.LINK_STATE:
                    node = params
                    self._command_link_state(node)
                elif command == NetworkRoutingCommand.DISTANCE_VECTOR:
                    node = params
                    self._command_distance_vector(node)
                elif command == NetworkRoutingCommand.SHOW:
                    self._command_show()
                elif command == NetworkRoutingCommand.SAVE_GRAPH:
                    (filename,) = params
                    self._command_save_graph(filename)
                elif command == NetworkRoutingCommand.SAVE_ROUTING_TABLE:
                    (node, filename) = params
                    self._command_save_routing_table(node, filename)
                # TODO implement print routing table command?
                elif command == NetworkRoutingCommand.CLEAR:
                    self._command_clear()
                elif command == NetworkRoutingCommand.LOAD:
                    (filename,) = params
                    self._command_load(filename)
                elif command == NetworkRoutingCommand.HELP:
                    self._command_help()
                elif command == NetworkRoutingCommand.QUIT:
                    self.exit()

                if self.log_level in ("WARNING",):
                    for warning in caught:
                        self.notify(
                            f"Warning: {str(warning.message)}", severity="warning"
                        )

        except Exception as e:
            if self.log_level in ("WARNING", "ERROR"):
                self.notify(f"Error: {e}", severity="error")

    ###########################################################################
    # Helper Methods
    ###########################################################################

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

    def _get_routing_table(self, node):
        if self.network_routing is None:
            return []

        return self.network_routing.get_routing_table(node)

    def _get_graph_image(self, size):
        if self.network_routing is None:
            return None

        term_width, term_height = size
        img = self.network_routing.graph.generate_image(
            int(term_width / 1.5), int(term_height * 1.6)
        )
        return Pixels.from_image(img)

    def _update_tabs(self):
        current_tab_ids = [id for id in self.network_routing.graph.nodes]
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
