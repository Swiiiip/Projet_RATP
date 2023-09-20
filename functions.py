from collections import deque

import pandas as pd


def safeIntInput(message, errorMessage, begin, end):
    result = -1
    while result == -1 or result < begin or result > end:
        try:
            result = int(input(message + "\n\n\n"))
        except ValueError:
            print("\n\n\n" + errorMessage)
        else:
            if result < begin or result > end:
                print("\n\n\n" + errorMessage)
    return result


def displayGraph(graph):
    # TODO display shit
    return


def getData():
    with open(file='metro.txt', mode='r', encoding='utf-8') as f:
        lines = f.readlines()[13:]

        sommets_data = []
        aretes_data = []

        for line in lines:
            elements = line.strip().split(';')
            premiere_colonne = elements[0].split(' ')

            if premiere_colonne[0] == 'V':
                nom_sommet = ' '.join(premiere_colonne[2:]) if len(premiere_colonne) > 2 else ''
                num_sommet = int(premiere_colonne[1])
                num_line = elements[1]
                derniere_colonne = elements[-1].split()
                terminus = bool(derniere_colonne[0])
                branchement = int(derniere_colonne[1])
                sommets_data.append([num_sommet, nom_sommet.strip(), num_line, terminus, branchement])
            else:
                num_start = int(premiere_colonne[1])
                num_end = int(premiere_colonne[2])
                time = int(premiere_colonne[3])
                aretes_data.append([num_start, num_end, time])

        sommets_df = pd.DataFrame(sommets_data,
                                  columns=['num_station', 'name_station', 'num_line', 'terminus', 'branchement'])
        aretes_df = pd.DataFrame(aretes_data,
                                 columns=['num_start', 'num_destination', 'time_secondes'])

    return sommets_df, aretes_df


def bellmanFord(graph, start, destination):
    # Initialisation
    weights = {}
    for index, row in graph.iterrows():
        u = row['num_start']

        if u not in weights:
            weights[u] = float('inf')

    weights[start] = 0

    predecessors = {}

    for _ in range(len(graph) - 1):
        for index, row in graph.iterrows():
            u = row['num_start']
            v = row['num_destination']
            w = row['time_secondes']

            if weights[u] + w < weights[v]:
                weights[v] = weights[u] + w
                predecessors[v] = u

    path = [destination]
    current_node = destination
    total_time = 0

    while current_node != start:
        if current_node in predecessors:
            current_node = predecessors[current_node]
            total_time += graph[(predecessors[current_node], current_node)]
            path.insert(0, current_node)

    return path, total_time


def getGraph(df_edges):
    graph = {}
    for _, row in df_edges.iterrows():
        start_node = row['num_start']
        end_node = row['num_destination']
        weight = row['time_secondes']

        if start_node not in graph:
            graph[start_node] = []
        if end_node not in graph:
            graph[end_node] = []

        graph[start_node].append((end_node, weight))
        graph[end_node].append((start_node, weight))

    return graph


def breadthFirstSearch(graph, start_node):
    visited = {}  # Dictionnaire pour suivre les nœuds visités
    queue = deque()  # File pour le parcours BFS

    # Ajouter le nœud de départ à la file
    queue.append(start_node)

    while queue:
        node = queue.popleft()  # Récupérer le premier nœud de la file
        visited[node] = True   # Marquer le nœud comme visité

        # Parcourir tous les voisins du nœud actuel
        for neighbor in graph[node]:
            if neighbor not in visited and neighbor not in queue:
                queue.append(neighbor)

    return visited

def makeConnexe(graph, visited_nodes):
    unvisited_nodes = list(set(graph.keys()) - set(visited_nodes))

    # Assurez-vous que les listes ne sont pas vides
    if unvisited_nodes and visited_nodes:
        # Choisissez un nœud non visité et connectez-le à un nœud visité
        unvisited_node = unvisited_nodes[0]
        visited_node = visited_nodes[0]

        # Ajoutez une arête entre les deux nœuds
        graph[unvisited_node].append(visited_node)
        graph[visited_node].append(unvisited_node)

    return graph


def prim(graph):
    acpm = set()
    start_vertex = list(graph.keys())[0]
    acpm.add(start_vertex)
    acpm_edges = []

    while len(acpm) < len(graph):
        min_edge = None

        for vertex in acpm:
            for neighbor, weight in graph[vertex]:
                if neighbor not in acpm and (min_edge is None or weight < min_edge[2]):
                    min_edge = (vertex, neighbor, weight)

        if min_edge is not None:
            u, v, w = min_edge
            acpm.add(v)
            acpm_edges.append((u, v, w))

    return acpm_edges

