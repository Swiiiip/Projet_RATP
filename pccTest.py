from functions import *

nodes_info, edges = getData()


def getNumFromNameStation(name):
    station_info = nodes_info.loc[nodes_info['name_station'] == name]
    return station_info['num_station'].values[0]


def getNameStationFromNum(num):
    station_info = nodes_info.loc[nodes_info['num_station'] == num]
    return station_info['name_station'].values[0]


graph = getGraph(edges)

# Parcours en largeur à partir d'un nœud de départ
start_node = edges['num_start'].iloc[0]
visited_nodes = breadthFirstSearch(graph=graph, start_node=start_node)

# Vérifier si le graphe est connexe
is_connected = len(visited_nodes) == len(graph)

# Si le graphe n'est pas connexe, ajoutez des arêtes supplémentaires
if not is_connected:
    print("Le graphe n'est pas connexe. Ajout d'arêtes pour le rendre connexe...")
    makeConnexe(graph=graph, visited_nodes=visited_nodes)

start = input('Saisissez votre station de départ : ')
destination = input('Saisissez votre station d\'arrivee : ')

num_start = getNumFromNameStation(start)
num_destination = getNumFromNameStation(destination)

path, time_total = bellmanFord(graph=edges, start=start, destination=destination)

print(path, time_total)
