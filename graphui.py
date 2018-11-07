import networkx as nx
import matplotlib.pyplot as plt

class resource_graph:
    def __init__(self):
        g = nx.Graph()
        g.add_node(1)
        g.add_node(2)

        nx.draw(g)
        plt.show()

rg = resource_graph()