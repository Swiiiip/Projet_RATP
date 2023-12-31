import pandas as pd
from os import getcwd, path
from urllib.request import urlopen

from typing import Tuple, Dict, List


def fetch_data_from_url(url: str) -> str:
    """
    Récupère une image à partir d'une URL et la convertit en base64.

    Parameters:
        url (str): L'URL de l'image à récupérer.

    Returns:
        str: La data cherchée.
    """
    u = urlopen(url)
    if '.txt' in url:
        raw_data = u.read().decode("utf-8")
    else:
        raw_data = u.read()
    u.close()

    return raw_data


data_urls = {
    "logo_ratp" : r"https://github.com/Swiiiip/Projet_RATP/blob/a76dce810b7a3a8074abd5e3ff4780d1b02780f5/data/assets/logo_ratp.png?raw=true",
    "arrow" : r"https://github.com/Swiiiip/Projet_RATP/blob/a76dce810b7a3a8074abd5e3ff4780d1b02780f5/data/assets/arrow.png?raw=true",
    "metrof_r" : r"https://github.com/Swiiiip/Projet_RATP/blob/a76dce810b7a3a8074abd5e3ff4780d1b02780f5/data/assets/metrof_r.png?raw=true",
    "metro.txt" : r"https://github.com/Swiiiip/Projet_RATP/blob/a76dce810b7a3a8074abd5e3ff4780d1b02780f5/data/assets/metro.txt?raw=true",
    "pospoints.txt" : r"https://github.com/Swiiiip/Projet_RATP/blob/a76dce810b7a3a8074abd5e3ff4780d1b02780f5/data/assets/pospoints.txt?raw=true"
    }

data_base64 = dict()
for name, url in data_urls.items():
    data_base64[name] = fetch_data_from_url(url)


def get_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Charge les données du fichier "metro.txt" et les structure en deux DataFrames pandas.

    Cette fonction lit les données du fichier "metro.txt" et les organise en deux DataFrames pandas :
    - Le premier DataFrame contient des informations sur les stations de métro.
    - Le deuxième DataFrame contient des informations sur les connexions entre les stations.

    Returns :
        tuple[pd.DataFrame, pd.DataFrame] : Un tuple contenant deux DataFrames.
            - Le premier DataFrame contient les colonnes suivantes :
                - 'num_station' : Le numéro de la station.
                - 'name_station' : Le nom de la station.
                - 'num_line' : Le numéro de la ligne de métro.
                - 'terminus' : Le terminus de la ligne.
                - 'branchement' : Le numéro de branchement.

            - Le deuxième DataFrame contient les colonnes suivantes :
                - 'num_start' : Le numéro de la station de départ.
                - 'num_destination' : Le numéro de la station de destination.
                - 'time_secondes' : Le temps en secondes pour atteindre la destination depuis la station de départ.
    """
    f = data_base64["metro.txt"].splitlines()
    lines = f[13:]

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
            terminus = derniere_colonne[0]
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

    sommets_df['num_line'] = [value.replace(' ', '') for value in sommets_df['num_line']]

    return sommets_df, aretes_df


def get_graph() -> Dict[int, List[Tuple[int, int]]]:
    """
    Construit un graphe représentant les connexions entre les stations de métro.

    Cette fonction utilise les données renvoyées par la fonction `get_data()` pour construire
    un graphe représentant les connexions entre les stations de métro.

    Returns :
        dict[int, list[tuple[int, int]]] : Un dictionnaire où les clés sont les numéros de station,
        et les valeurs sont des listes de tuples. Chaque tuple contient le numéro de la station de destination
        et le temps en secondes pour atteindre cette destination à partir de la station d'origine.
    """
    graph = {}
    aretes_df = get_data()[1]

    for _, row in aretes_df.iterrows():
        num_start = row['num_start']
        num_destination = row['num_destination']
        time_secondes = row['time_secondes']

        if num_start not in graph:
            graph[num_start] = []
        if num_destination not in graph:
            graph[num_destination] = []

        graph[num_start].append((num_destination, time_secondes))
        graph[num_destination].append((num_start, time_secondes))

    return graph


def get_station_coordinates() -> Dict[str, Tuple[int, int]]:
    """
    Lit les coordonnées des stations à partir d'un fichier et les stocke dans un dictionnaire.

    Returns :
        dict[str, tuple[int, int]] : Un dictionnaire avec les noms de station en tant que clés
         et les coordonnées (x, y) en tant que valeurs.

    Le fichier doit avoir un format spécifique où chaque ligne contient les coordonnées x et y,
     suivies du nom de la station séparé par des points-virgules (;).
      Les noms de station peuvent contenir des caractères spéciaux, et le caractère '@' est remplacé par un espace.
    """

    station_coordinates = {}

    file = data_base64["pospoints.txt"].splitlines()
    for line in file:
        x, y, station_name = line.strip().split(';')

        x, y = int(x), int(y)
        station_name = station_name.replace('@', ' ')

        station_coordinates[station_name] = (x, y)

    return station_coordinates
