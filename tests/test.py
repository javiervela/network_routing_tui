import matplotlib.pyplot as plt

from network_routing_tui.graph import Graph
from network_routing_tui.link_state import link_state
from network_routing_tui.graph_generator import gen_random, gen_damage
from network_routing_tui.measurement import evaluate_routing


if __name__ == "__main__":
    G = Graph()

    #G.load_file("./tests/graph.txt")
    #G.save_file("./tests/randotron.txt")
    G.apply_input("A B 10")

    for i in range(10):
        G.distance_vector()

        d = evaluate_routing(G)
        print("Total errors:", d)
        if i == 5:
            print("Damaging graph")
            G = gen_damage(G, 2)

    G.show()

    print("------\nLegacy")
    G = Graph()

    G.load_file("./tests/graph.txt")
    #G.save_file("./tests/randotron.txt")

    for i in range(20):
        G.distance_vector_legacy()

        d = evaluate_routing(G)
        print("Total errors:", d)
        if i == 5:
            print("Damaging graph")
            G = gen_damage(G, 2)

    G.show()

    
    """
    G.apply_input("A B 1")
    G.apply_input("C B 1")
    G.apply_input("C D 1")

    rT = link_state(G,"A")
    print(rT.show(),"\n----")
    for i in range(10):
        G.distance_vector_legacy()
    print(G.get_routing_table("A").show(),"\n----")
    G.show()

    G.apply_input("C B -")

    for i in range(10):
        G.distance_vector_legacy()
    
    print(G.get_routing_table("A").show())
    G.show()
    """
    """
    for i in range(100):
        G = gen_random(20)
        for i in range(5):
            G.distance_vector()

        G = gen_damage(G, 5)

        for i in range(20):
            G.distance_vector()

        for u in ["A", "B", "C", "D", "E"]:
            if u in G:
                rT = link_state(G,u)
                if not rT.compare(G.get_routing_table(u)):
                    print("Yo problem")
                    print(rT.show())
                    print("--------------")
                    print(G.get_routing_table(u).show())
                    G.show()
    """
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
