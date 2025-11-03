import io
import matplotlib.pyplot as plt
from PIL import Image
from textual.app import App, ComposeResult
from textual.widgets import Placeholder, Header, Footer, Static, Tabs, Tab, DataTable
from textual.containers import Horizontal, Vertical, HorizontalScroll
from rich_pixels import Pixels
import networkx as nx

G = nx.Graph()
G.add_nodes_from(
    [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
    ]
)
G.add_edges_from(
    [
        ("A", "B"),
        ("A", "C"),
        ("A", "D"),
        ("A", "E"),
        ("A", "F"),
        ("A", "G"),
        ("F", "G"),
        ("E", "G"),
        ("E", "F"),
    ]
)


def generate_graph_image(graph: nx.Graph, width_px: int, height_px: int) -> Image.Image:
    pos = nx.spring_layout(graph, seed=42)
    dpi = 30
    fig_w, fig_h = width_px / dpi, height_px / dpi
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
    # remove figure background and margins so there are no borders
    fig.patch.set_facecolor("none")
    ax.set_axis_off()
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    nx.draw(
        graph,
        pos=pos,
        ax=ax,
        node_color="skyblue",
        node_size=600,
        edge_color="gray",
        with_labels=True,
        font_size=20,
    )
    buf = io.BytesIO()
    fig.savefig(buf, format="png", transparent=True, bbox_inches="tight", pad_inches=0)
    # plt.show() # TODO include this
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf).convert("RGBA")


ROUTING_TABLES = {
    "A": [
        ["Destination", "Via/Next-Hop", "Cost"],
        ("A", "B", "1"),
        ("A", "C", "2"),
        ("A", "D", "3"),
        ("A", "E", "4"),
        ("A", "F", "5"),
        ("A", "G", "6"),
    ],
    "B": [
        ["Destination", "Via/Next-Hop", "Cost"],
        ("B", "A", "1"),
        ("C", "A", "2"),
        ("D", "A", "3"),
        ("E", "A", "4"),
        ("F", "A", "5"),
        ("G", "A", "6"),
    ],
}


class LayoutApp(App):
    CSS = """
    Screen {
        layout: horizontal;
        background: #1e1e1e;
        color: white;
    }

    #Header, #Footer {
        background: #333333;
        color: white;
        height: 1;
        content-align: center middle;
    }

    #left_pane {
        width: 1fr;
    }

    #right_pane {
        width: 3fr;
    }
    
    #routing_tables_title {
        height: 1fr;
        content-align: center middle;
        background: #252526;
        color: #f5f5f5;
        border: none;
    }

    .node_tabs {
        background: #1f1f1f;
        color: #f5f5f5;
        height: 1fr;
        width: auto;
        padding: 0 0;
        border: none;
    }

    #node_tabs Tab {
        background: #2a2a2a;
        color: #f5f5f5;
        text-style: none;
    }

    /* Active tab */
    #node_tabs Tab.-active {
        background: #007acc;
        color: white;
        text-style: bold;
    }

    .routing_table_pane {
        height: 20fr;
        background: #2d2d2d;
        padding: 0;
    }

    .graph_view_pane {
        height: 12fr;
        background: #202020;
        padding: 0;
        content-align: center middle;
    }

    .button {
        height: 1fr;
        width: 1fr;
        background: #2a2a2a;
        content-align: center middle;
        padding: 0;
    }
    """

    TITLE = "Network Routing"
    SUB_TITLE = (
        "Interactive Network Topology — Routing Visualization"  # TODO make better
    )

    def compose(self) -> ComposeResult:
        yield Header(id="Header")

        with Horizontal():
            with Vertical(id="left_pane"):
                yield Static("Routing Tables", id="routing_tables_title")

                tabs = [Tab(name, id=name) for name in G.nodes]
                # Make tabs horizontally scrollable when they don't fit

                with HorizontalScroll():
                    yield Tabs(*tabs, name="Nodes", id="node_tabs", classes="node_tabs")

                yield DataTable(id="routing_table", classes="routing_table_pane")

            with Vertical(id="right_pane"):
                term_width, term_height = self.app.size
                graph_image = generate_graph_image(
                    G, int(term_width / 1.5), int(term_height * 1.6)
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
        routing_table = ROUTING_TABLES.get(node, [])
        table = self.query_one(DataTable)
        if not table.columns:
            table.add_columns(*routing_table[0])
        table.clear()
        table.add_rows(routing_table[1:])
        table.zebra_stripes = True


def main():
    # TwoPaneApp().run()

    app = LayoutApp()
    app.run()


if __name__ == "__main__":
    main()
