from tkinter import messagebox, simpledialog

from values import *


# Vérifier la connexité du graphe
def is_connected(aretes_df):
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


def getNumFromNameStation(name):
    station_info = sommets_df.loc[sommets_df['name_station'] == name]
    return station_info['num_station'].values[0]


def getRealName(station):
    station = station.lower()

    station_info = sommets_df.loc[sommets_df['name_station'].str.lower() == station]

    return station_info['name_station'].values[0]


def getNameStationFromNum(num):
    station_info = sommets_df.loc[sommets_df['num_station'] == num]
    return station_info['name_station'].values[0]


def est_station_valide(nom_station):
    nom_station = nom_station.lower()
    sommets_df_lower = sommets_df['name_station'].str.lower()

    return nom_station in sommets_df_lower.tolist()


def custom_input_dialog(parent, title, prompt):
    parent.withdraw()
    while True:
        user_input = simpledialog.askstring(title, prompt)
        if user_input is None:
            parent.deiconify()
            return None
        if est_station_valide(user_input):
            return user_input
        else:
            messagebox.showerror("Erreur", "Station inconnue, veuillez saisir une station valide.")


def getNeighbors(num_sommet):
    neighbors = aretes_df.loc[aretes_df['num_start'] == num_sommet]

    return neighbors['num_destination']


def bellman_ford(aretes_df, num_start, num_destination):
    # Créez une liste d'arêtes à partir du DataFrame
    edges = [(row['num_start'], row['num_destination'], row['time_secondes']) for _, row in aretes_df.iterrows()]

    # Créez un ensemble de tous les nœuds
    nodes = set()
    for edge in edges:
        weight = edge[2]
        nodes.add(edge[0], weight)
        nodes.add(edge[1], weight)

    # Calculez le nombre total de nœuds
    num_nodes = max(nodes) + 1

    # Créez une liste pour stocker les distances initiales à l'infini
    distances = [float('inf')] * num_nodes
    distances[num_start] = 0

    # Créez une liste pour stocker les précédents nœuds
    previous_nodes = [None] * num_nodes

    for _ in range(num_nodes - 1):
        for u, v, weight in edges:
            if distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight
                previous_nodes[v] = u

    # Reconstituez le chemin depuis le nœud de destination jusqu'au nœud de départ
    path = []
    current_node = num_destination
    while current_node is not None:
        path.insert(0, current_node)
        current_node = previous_nodes[current_node]

    return path
