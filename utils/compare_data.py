from data.values import sommets_df


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
