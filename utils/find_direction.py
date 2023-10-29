from __future__ import annotations

import pandas as pd

from data.values import sommets_df, aretes_df
from utils.compare_data import is_same_line, is_same_direction


def find_direction(path: list[int], current_station: int, next_station: int, line: str) -> str | None:
    """
    Trouve la direction entre deux stations sur la même ligne.

    Args:
        path (list[int]): Une liste de numéros de stations représentant un chemin.
        current_station (int): Le numéro de la station actuelle.
        next_station (int): Le numéro de la station de destination.
        line (str): Le numéro de ligne de métro.

    Returns:
        str | None: La direction entre les deux stations sur la même ligne, ou None si aucune direction n'est trouvée.
    """
    visited = set()
    return find_direction_recursive(path, current_station, next_station, line, visited)


def find_direction_recursive(path: list[int], current_station: int, next_station: int,
                              line: str, visited: set) -> str | None:
    """
    Fonction récursive pour trouver la direction entre deux stations sur la même ligne.

    Args:
        path (list[int]): Une liste de numéros de stations représentant un chemin.
        current_station (int): Le numéro de la station actuelle.
        next_station (int): Le numéro de la station suivante.
        line (str): Le numéro de ligne de métro.
        visited (set) : la liste des stations déja visitées.

    Returns:
        str | None: La direction entre les deux stations sur la même ligne, ou None si aucune direction n'est trouvée.
    """
    current_station_info = sommets_df.loc[current_station]
    next_station_info = sommets_df.loc[next_station]

    # terminus
    if next_station_info['terminus'] == 'True':
        return next_station_info['name_station']

    if current_station in visited:
        return None

    visited.add(current_station)

    branchement = current_station_info['branchement']

    edges = aretes_df.loc[(aretes_df['num_start'] == next_station) | (aretes_df['num_destination'] == next_station)]

    # dernier cas
    if edges['num_start'].count() == 1:
        return next_station_info['name_station']

    possible_station = pd.concat([edges['num_start'], edges['num_destination']]).unique()

    for station in possible_station:
        if (station != current_station and station != next_station
                and is_same_line(station, line) and is_same_direction(path, station, branchement)):
            direction = find_direction_recursive(path=path, current_station=next_station, next_station=station,
                                                 line=line, visited=visited)
            if direction:
                return direction

    visited.remove(current_station)

    # Aucun chemin jusqu'à un terminus trouvé
    return None
