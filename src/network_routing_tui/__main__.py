import io
import matplotlib.pyplot as plt
from PIL import Image
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Placeholder, Header, Footer, Static
from textual.containers import Horizontal
from rich_pixels import Pixels
import networkx as nx


G = nx.Graph()
G.add_nodes_from(["A", "B", "C", "D", "E", "F", "G"])
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
    plt.show()
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf).convert("RGBA")


class LayoutApp(App):
    CSS = """
        Screen {
        layout: horizontal;
    }

    .box {
        height: 100%;
        width: 1fr;
        border: solid green;
    }
    """
    TITLE = "A Question App"
    SUB_TITLE = "The most important question"

    def compose(self) -> ComposeResult:
        yield Header(id="Header")
        with Horizontal():
            yield Static(id="left_pane", classes="box")

            term_width, term_height = self.app.size
            graph_image = generate_graph_image(
                G, int(term_width / 2.2), int(term_height * 1.75)
            )
            yield Static(Pixels.from_image(graph_image), id="right_pane", classes="box")

        yield Footer(id="Footer")


def main():
    # TwoPaneApp().run()

    app = LayoutApp()
    app.run()


if __name__ == "__main__":
    main()
