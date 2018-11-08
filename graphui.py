import networkx as nx
import matplotlib.pyplot as plt
import warnings

class resource_graph:
    def __init__(self):
        self.G = nx.DiGraph()
        self.processes = []
        self.ncolors = []

    def add_res_node(self, res):
        self.G.add_node(res)
        self.ncolors.append('green')
    def add_proc_node(self, proc):
        self.G.add_node(proc)
        self.processes.append(proc)
        self.ncolors.append('red')
    def add_requests_edge(self, proc, res):
        self.G.add_edge(res, proc,color='r')


    def add_connects_edge(self, proc, res):
        self.G.add_edge(proc, res, color='b')

    def add_releases_edge(self, proc, res):
        if self.G.has_edge(proc, res):
            self.G.remove_edge(proc, res)
        elif self.G.has_edge(res, proc):
            self.G.remove_edge(proc, res)


    def draw_graph(self):
        pos=nx.bipartite_layout(self.G, self.processes)
        nx.draw(self.G, pos, node_color = self.ncolors, with_labels=True)
        plt.show()

