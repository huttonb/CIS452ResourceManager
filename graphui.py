import networkx as nx
import matplotlib.pyplot as plt

# Resource Graph is the UI for the resource manager. It creates a graph using networkX and presents it.
# It's a directional graph, edges going from the resource to the process are requested, but not taken.
# Edges going from process to resource means that resource is held by that process.
class resource_graph:
    def __init__(self):
        self.G = nx.DiGraph()
        self.processes = []
        self.ncolors = []

    # add_res_node adds a resource node, which are green.
    def add_res_node(self, res):
        self.G.add_node(res)
        self.ncolors.append('green')
    # add_proc_node adds a process node, which is red
    def add_proc_node(self, proc):
        self.G.add_node(proc)
        self.processes.append(proc)
        self.ncolors.append('red')

    # add_requests_edge adds an edge between the resource and process. It needs to be its own function as
    # the edge is going from resource to process, not the other way around.
    def add_requests_edge(self, proc, res):
        self.G.add_edge(res, proc,color='r')

    # add_connects_edge adds an edge between a process and a resource
    def add_connects_edge(self, proc, res):
        self.G.add_edge(proc, res, color='b')

    # add_releases_edge removes an edge between two nodes. Before it removes the edge, it first checks to make
    # sure that the edge exists.
    def add_releases_edge(self, proc, res):
        if self.G.has_edge(proc, res):
            self.G.remove_edge(proc, res)
        elif self.G.has_edge(res, proc):
            self.G.remove_edge(res, proc)

    # Draw Graph draws and shows the graph, using a bipartite layout.
    def draw_graph(self):
        pos=nx.bipartite_layout(self.G, self.processes)
        nx.draw(self.G, pos, node_color = self.ncolors, with_labels=True)
        plt.show()

