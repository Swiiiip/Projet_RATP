from __future__ import annotations

from values import *


def get_num_from_name_station_and_line(name: str, line: str = None) -> int:
    """
    Récupère le numéro de station à partir du nom de la station et éventuellement du numéro de ligne.

    Args:
        name (str): Le nom de la station.
        line (str, optional): Le numéro de la ligne de métro. Par défaut, il est None.

    Returns:
        int: Le numéro de la station correspondant au nom et, éventuellement, au numéro de ligne.
    """
    stations_info = sommets_df.loc[(sommets_df['name_station'] == name)]

    if line is None:
        return stations_info['num_station'].values[0]

    else:
        station = stations_info.loc[stations_info['num_line'] == line]
        return station['num_station'].values[0]


def get_name_station_from_num(num: int) -> str:
    """
    Récupère le nom de la station à partir de son numéro.

    Args:
        num (int): Le numéro de la station.

    Returns:
        str: Le nom de la station correspondant au numéro.
    """
    station_info = sommets_df.loc[sommets_df['num_station'] == num]
    return station_info['name_station'].values[0]


def get_ligne_station(station: int) -> str:
    """
    Récupère le numéro de ligne de la station à partir de son numéro.

    Args:
        station (int): Le numéro de la station.

    Returns:
        str: Le numéro de ligne correspondant à la station.
    """
    station_info = sommets_df.loc[sommets_df['num_station'] == station]
    return station_info['num_line'].values[0]


def is_same_line(station: str, line: str) -> bool:
    """
    Vérifie si une station est sur la même ligne que le numéro de ligne donné.

    Args:
        station (str): Le numéro de la station.
        line (str): Le numéro de ligne de métro.

    Returns:
        bool: True si la station est sur la même ligne que le numéro de ligne donné, False sinon.
    """
    return sommets_df.at[station, 'num_line'] == line


def is_same_direction(path: list[int], station: str, branchement: int) -> bool:
    """
    Vérifie si une station est dans la même direction que la station donnée.

    Args:
        path (list[int]): Une liste de numéros de stations représentant le plus court chemin.
        station (str): Le numéro de la station.
        branchement (int): Le numéro de branchement de la station.

    Returns:
        bool: True si la station est dans la même direction que la station donnée et qu'elle est dans le chemin,
        False sinon.
    """
    branchement_station = sommets_df.at[station, 'branchement']

    if branchement_station != branchement:
        return station in path

    else:
        return True


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


def find_direction_recursive(path: list[int], current_station: int, next_station: int, line: str, visited: set) -> str | None:
    """
    Fonction récursive pour trouver la direction entre deux stations sur la même ligne.

    Args:
        path (list[int]): Une liste de numéros de stations représentant un chemin.
        current_station (int): Le numéro de la station actuelle.
        next_station (int): Le numéro de la station suivante.
        line (str): Le numéro de ligne de métro.

    Returns:
        str | None: La direction entre les deux stations sur la même ligne, ou None si aucune direction n'est trouvée.
    """
    if current_station in visited:
        return None

    visited.add(current_station)
    current_station_info = sommets_df.loc[current_station]
    next_station_info = sommets_df.loc[next_station]

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


def time_format(seconds: int) -> str:
    """
    Convertit un nombre de secondes en une chaîne de format heures, minutes, et secondes.

    Args:
        seconds (int): Le nombre de secondes.

    Returns:
        str: Une chaîne de format "X heures Y minutes et Z secondes".
    """
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    time = ""
    if hour > 0:
        time += f"{hour} heure{'s' if hour > 1 else ''}"

    if minutes > 0:
        if time:
            time += " "
        time += f"{minutes} minute{'s' if minutes > 1 else ''}"

    if seconds > 0:
        if time:
            time += " et "
        time += f"{seconds} seconde{'s' if seconds > 1 else ''}"

    return time


def get_instructions(shortest_path: list[int], total_time: int) -> str:
    """
    Génère des instructions pour un itinéraire le plus court calculé à l'aide de l'algorithme de Bellman-Ford.

    Args:
        shortest_path (list[int]): Une liste d'entiers représentant les numéros des stations
            sur l'itinéraire le plus court calculé avec l'algorithme de Bellman-Ford.
        total_time (int): Le temps total estimé pour parcourir l'itinéraire en secondes.

    Returns:
        str: Une chaîne de caractères contenant les instructions pour suivre l'itinéraire,
            y compris les stations, les changements de ligne et le temps de trajet estimée.

    """
    first_station = shortest_path[0]
    current_location = get_name_station_from_num(first_station)

    if len(shortest_path) == 1:
        return f'Vous êtes déjà à {current_location}. Vous n\'avez pas besoin de prendre le métro.'

    second_station = shortest_path[1]
    last_station = shortest_path[-1]

    line = get_ligne_station(first_station)

    instructions = f'- Vous êtes à {current_location}, ligne {line}.\n'

    direction = find_direction(path=shortest_path, current_station=first_station, next_station=second_station,
                               line=line)

    if direction:
        instructions += f'- Prenez la ligne {line} direction {direction}\n'

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
                instructions += f'- À {name_changement}, changez et prenez la ligne {line} direction {direction}.\n'

    final_location = get_name_station_from_num(last_station)
    line_final_station = get_ligne_station(last_station)
    instructions += (f'- Vous devriez arriver à {final_location}, ligne {line_final_station}'
                     f' dans environ {time_format(total_time)}.')

    return instructions
