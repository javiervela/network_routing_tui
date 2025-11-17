import matplotlib.pyplot as plt

from network_routing_tui.graph import Graph
from network_routing_tui.link_state import link_state


if __name__ == "__main__":
    G = Graph()

    G.load_file("./tests/graph.txt")
    G.save_file("./tests/test.txt")

    rT = link_state(G,"A")
    print(rT.show())
    G.show()

    """
    for i in range(5):
        print("-------")
        G.distance_vector()
        G.print_table("A")
    
    G.show()
    print("  \nBREAK\n")
    G.apply_input("A B 50")
    G.print_table("J")
    G.show()

    for i in range(5):
        print("######")
        print("-------A")
        G.distance_vector()
        G.print_table("A")
        print("-------J")
        G.print_table("J")

    print(G.get_routing_table("A").get_table_as_list())

    G.show()
    """
