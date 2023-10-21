import math
from tkinter import messagebox, simpledialog

from values import *


# Vérifier la connexité du graphe
def is_connected():
    # Créez une liste d'arêtes à partir du DataFrame
    edges = [(row['num_start'], row['num_destination']) for _, row in aretes_df.iterrows()]

    # Fonction de recherche en profondeur (DFS)
    def dfs(graph, node, visited):
        visited[node] = True
        for neighbor in graph[node]:
            if not visited[neighbor]:
                dfs(graph, neighbor, visited)

    # Créez un ensemble de tous les nœuds
    nodes = set()
    for edge in edges:
        nodes.add(edge[0])
        nodes.add(edge[1])

    # Créez un dictionnaire de listes d'adjacence pour représenter le graphe
    graph = {node: [] for node in nodes}
    for edge in edges:
        graph[edge[0]].append(edge[1])
        graph[edge[1]].append(edge[0])  # Si le graphe est non dirigé, ajoutez également cette ligne

    # Commencez la recherche en profondeur à partir d'un nœud au hasard
    start_node = list(nodes)[0]
    visited = {node: False for node in nodes}
    dfs(graph, start_node, visited)

    # Vérifiez si tous les nœuds ont été visités
    if all(visited[node] for node in nodes):
        return True
    else:
        return False


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d hours %02d minutes" % (hour, minutes)


def need_line_precision(name):
    return sommets_df.loc[(sommets_df['name_station'] == name)]['name_station'].count() != 1


def getNumFromNameStationAndLine(name, line):
    stations_info = sommets_df.loc[(sommets_df['name_station'] == name)]

    if line is None:
        return stations_info['num_station'].values[0]

    else:
        station = stations_info.loc[stations_info['num_line'] == line]
        return station['num_station'].values[0]


def getRealName(station):
    station = station.lower()

    station_info = sommets_df.loc[sommets_df['name_station'].str.lower() == station]

    return station_info['name_station'].values[0]


def getNameStationFromNum(num):
    station_info = sommets_df.loc[sommets_df['num_station'] == num]
    return station_info['name_station'].values[0]


def getLigneStation(station):
    station_info = sommets_df.loc[sommets_df['num_station'] == station]
    return station_info['num_line'].values[0]


def est_station_valide(nom_station):
    nom_station = nom_station.lower()
    sommets_df_lower = sommets_df['name_station'].str.lower()

    return nom_station in sommets_df_lower.tolist()


def getNeighbors(num_sommet):
    neighbors = aretes_df.loc[aretes_df['num_start'] == num_sommet]

    return neighbors['num_destination']


def same_line(station, line):
    num_line_station = sommets_df.at[station, 'num_line']

    return num_line_station == line


def same_direction(path, station, branchement):
    branchement_station = sommets_df.at[station, 'branchement']

    if branchement_station != branchement:
        return station in path

    else:
        return True


def find_direction(path, current_station, next_station, line):
    return find_direction_recursive(path, current_station, next_station, line)


def find_direction_recursive(path, current_station, next_station, line):
    current_station_info = sommets_df.loc[current_station]
    next_station_info = sommets_df.loc[next_station]

    branchement = current_station_info['branchement']

    edges = aretes_df.loc[(aretes_df['num_start'] == next_station) | (aretes_df['num_destination'] == next_station)]

    possible_station = pd.concat([edges['num_start'], edges['num_destination']]).unique()

    for station in possible_station:
        if (station != current_station and station != next_station
                and same_line(station, line) and same_direction(path, station, branchement)):
            direction = find_direction_recursive(path=path, current_station=next_station, next_station=station,
                                                 line=line)
            if direction:
                return direction

    # dernier cas
    if edges['num_start'].count() == 1:
        return next_station_info['name_station']

    return None  # Aucun chemin jusqu'à un terminus trouvé


def bellman_ford(num_start, num_destination):
    all_nodes = set(aretes_df['num_start']) | set(aretes_df['num_destination'])
    distances = {num_start: 0}
    predecessors = {None: 0 for _ in all_nodes}

    # Créer un dictionnaire pour représenter le graphe à partir du dataframe
    graph = {}
    for index, row in aretes_df.iterrows():
        start, destination, time = row['num_start'], row['num_destination'], row['time_secondes']
        if start not in graph:
            graph[start] = []
        if destination not in graph:
            graph[destination] = []
        graph[start].append((destination, time))
        graph[destination].append((start, time))

    # Appliquer l'algorithme de Bellman-Ford
    num_vertices = len(graph)

    for _ in range(num_vertices - 1):
        for vertex in graph:
            if vertex in distances:  # Vérifier si le nœud est déjà atteint
                for neighbor, weight in graph[vertex]:
                    if neighbor not in distances or distances[vertex] + weight < distances[neighbor]:
                        distances[neighbor] = distances[vertex] + weight
                        predecessors[neighbor] = vertex

    # Vérifier s'il y a des cycles de poids négatifs
    for vertex in graph:
        if vertex in distances:  # Vérifier si le nœud est déjà atteint
            for neighbor, weight in graph[vertex]:
                if distances[vertex] + weight < distances[neighbor]:
                    raise ValueError("Le graphe contient un cycle de poids négatif")

    path = []
    current_node = num_destination

    while current_node != num_start:
        path.insert(0, current_node)  # Insérer le nœud au début du chemin
        if current_node not in predecessors:
            raise ValueError(f"Il n'y a pas de chemin de {num_start} à {num_destination}")

        current_node = predecessors[current_node]
    path.insert(0, num_start)

    return path, convert(distances[num_destination])


def toString(num_start, num_destination):
    shortest_path, total_time = bellman_ford(num_start, num_destination)

    current_location = getNameStationFromNum(num_start)
    first_station = shortest_path[0]
    second_station = shortest_path[1]
    line = getLigneStation(first_station)

    print(f'\t- Vous êtes à {current_location}, ligne {line}.')

    direction = find_direction(path=shortest_path, current_station=first_station, next_station=second_station,
                               line=line)

    if direction:
        print(f'\t- Prenez la ligne {line} direction {direction}')

    for i in range(0, len(shortest_path) - 1):
        station = shortest_path[i]
        station_info = sommets_df.loc[sommets_df['num_station'] == station]
        next_station = shortest_path[i + 1]

        line_station = station_info['num_line'].values[0]

        if line_station != line:
            name_changement = station_info['name_station'].values[0]
            line = line_station
            direction = find_direction(path=shortest_path, current_station=station, next_station=next_station,
                                       line=line)
            if direction:
                print(f'\t- A {name_changement}, changez et prenez la ligne {line} direction {direction}.')

    final_location = getNameStationFromNum(num_destination)
    print(f'\t- Vous devriez arriver à {final_location} dans environ {total_time}.')
