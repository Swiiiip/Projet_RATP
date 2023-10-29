from random import choice
from values import *


def is_connexe(graph: dict[int, list[tuple[int, int]]]) -> bool:
    """
    Vérifie si le graphe est connexe en utilisant un parcours en profondeur.

    Args:
        graph (dict[int, list[tuple[int, int]]]): Le graphe représenté sous forme de dictionnaire.

    Returns:
        bool: True si le graphe est connexe, False sinon.
    """
    def PP(graph, node, visited):
        """
        Fonction de parcours en profondeur

        Cette fonction est utilisée pour parcourir le graphe en profondeur à partir d'un nœud donné
        et marquer les nœuds visités.

        Args:
            graph (dict[int, list[tuple[int, int]]]): Le graphe représenté sous forme de dictionnaire.
            node (int): Le numéro du nœud à partir duquel commence le parcours en profondeur.
            visited (dict[int, bool]): Un dictionnaire qui marque les nœuds visités.

        Returns:
            None: La fonction ne renvoie rien, mais elle met à jour le dictionnaire `visited` pour marquer les nœuds visités.
        """
        visited[node] = True
        for edge in graph[node]:
            neighbor = edge[0]
            if not visited[neighbor]:
                PP(graph, neighbor, visited)

    edges = [(row['num_start'], row['num_destination']) for _, row in aretes_df.iterrows()]

    # Crée un ensemble de tous les nœuds.
    nodes = set()
    for edge in edges:
        nodes.add(edge[0])
        nodes.add(edge[1])

    # Commence la recherche en profondeur à partir d'un nœud au hasard
    start_node = list(nodes)[0]
    visited = {node: False for node in nodes}
    PP(graph, start_node, visited)

    # Vérifie si tous les nœuds ont été visités
    return all(visited[node] for node in nodes)


def bellman_ford(graph: dict[int, list[tuple[int, int]]], num_start: int, num_destination: int) -> tuple[list[int], int]:
    """
    Applique l'algorithme de Bellman-Ford pour trouver le plus court chemin entre deux stations.

    Args:
        graph (dict[int, list[tuple[int, int]]]): Le graphe représenté sous forme de dictionnaire.
        num_start (int): Le numéro de la station de départ.
        num_destination (int): Le numéro de la station d'arrivée.

    Returns:
        tuple[list[int], int]: Un tuple contenant le chemin le plus court sous forme de liste de numéros de station,
        et la distance totale du chemin en secondes.
    Raises:
        ValueError: Si le graphe contient un cycle de poids négatif ou s'il n'y a pas de chemin entre les stations.
    """
    all_nodes = set(aretes_df['num_start']) | set(aretes_df['num_destination'])
    distances = {num_start: 0}
    predecessors = {None: 0 for _ in all_nodes}

    # Application de l'algorithme de Bellman-Ford
    num_vertices = len(graph)

    for _ in range(num_vertices - 1):
        for vertex in graph:
            if vertex in distances:  # Vérifie si le nœud est déjà atteint
                for neighbor, weight in graph[vertex]:
                    if neighbor not in distances or distances[vertex] + weight < distances[neighbor]:
                        distances[neighbor] = distances[vertex] + weight
                        predecessors[neighbor] = vertex

    # Vérifie s'il y a des cycles de poids négatifs
    for vertex in graph:
        if vertex in distances:  # Vérifier si le nœud est déjà atteint
            for neighbor, weight in graph[vertex]:
                if distances[vertex] + weight < distances[neighbor]:
                    raise ValueError("Le graphe contient un cycle de poids négatif")

    # Récupère le pcc entre la station de départ et la station d'arrivée
    path = []
    current_node = num_destination

    while current_node != num_start:
        path.insert(0, current_node)  # Insère le nœud au début du chemin
        if current_node not in predecessors:
            raise ValueError(f"Il n'y a pas de chemin de {num_start} à {num_destination}")

        current_node = predecessors[current_node]
    path.insert(0, num_start)

    return path, distances[num_destination]


def prim(graph: dict[int, list[tuple[int, int]]]) -> (dict[int, list[tuple[int, int]]], int):
    """
    Applique l'algorithme de Prim pour trouver un arbre couvrant minimal dans le graphe.

    Args:
        graph (dict[int, list[tuple[int, int]]]): Le graphe représenté sous forme de dictionnaire.

    Returns:
        dict[int, list[tuple[int, int]]]: Un dictionnaire représentant un arbre couvrant minimal du graphe.
    """
    # Initialisation
    all_nodes = graph.keys()
    edges = dict()

    total_weight = 0

    # Choisit n'importe quel sommet initial
    start_node = choice(list(all_nodes))
    edges[start_node] = []

    # Répète jusqu'à ce que tous les sommets soient inclus
    while len(edges.keys()) < len(all_nodes):
        min_edge = None

        # Parcoure tous les sommets inclus
        for node in edges.keys():
            # Parcoure toutes les arêtes du sommet actuel
            for neighbor, weight in graph[node]:
                # Si le voisin n'est pas inclus
                if neighbor not in edges.keys():
                    # Si aucune arête n'a encore été sélectionnée
                    # OU si l'arête actuelle est plus petite que l'arête sélectionnée précédente
                    if min_edge is None or weight < min_edge[2]:
                        min_edge = (node, neighbor, weight)

        # Si une arête a été sélectionnée
        if min_edge is not None:
            # Ajoutez l'arête minimale à la liste des arêtes de l'arbre couvrant minimal
            tmp = edges[min_edge[0]] + [(min_edge[1], min_edge[2])]
            edges[min_edge[0]] = tmp

            # Ajoute le sommet exclu à l'ensemble des sommets inclus
            edges[min_edge[1]] = []

            # Ajoutez le poids de l'arête à la somme des poids
            total_weight += min_edge[2]

    return edges, total_weight
