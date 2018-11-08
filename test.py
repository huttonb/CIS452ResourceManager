import networkx as nx
import matplotlib.pyplot as plt
G = nx.DiGraph()
G.add_edge(1,2,color='r')
G.add_edge(2,3,color='b')
G.add_edge(3,4,color='g')

pos = nx.bipartite_layout(G, [1,2])

edges = G.edges()
colors = [G[u][v]['color'] for u,v in edges]


nx.draw(G, pos, edges=edges, edge_color=colors, with_labels=True)
plt.show()
