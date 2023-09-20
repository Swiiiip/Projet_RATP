import networkx as nx
import matplotlib.pyplot as plt

liste_aretes = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]
graphe = nx.Graph(liste_aretes)
print("Nœuds du graphe:", graphe.nodes())
print("Arêtes du graphe:", graphe.edges())
nx.draw(graphe, with_labels=True, node_color='lightblue', node_size=800, font_size=12)
plt.show()