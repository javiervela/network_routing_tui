import matplotlib.pyplot as plt

from network_routing_tui.graph import Graph


if __name__ == "__main__":
    G = Graph()

    G.load_file("./tests/graph.txt")
    G.save_file("./tests/test.txt")

    for i in range(5):
        print("-------")
        G.distance_vector()
        G.print_table("A")

    print(G.get_routing_table("A").get_table_as_list())

    G.draw(1)
    plt.show()
