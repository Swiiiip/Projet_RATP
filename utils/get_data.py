from data.values import sommets_df


def get_num_from_name_station_and_line(name: str, line: str = None) -> int:
    """
    Récupère le numéro de station à partir du nom de la station et éventuellement du numéro de ligne.

    Args :
        name (str) : Le nom de la station.
        line (str, optional) : Le numéro de la ligne de métro. Par défaut, il est None.

    Returns :
        int : Le numéro de la station correspondant au nom et, éventuellement, au numéro de ligne.
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

    Args :
        num (int) : Le numéro de la station.

    Returns :
        str : Le nom de la station correspondant au numéro.
    """
    station_info = sommets_df.loc[sommets_df['num_station'] == num]
    return station_info['name_station'].values[0]


def get_ligne_station(station: int) -> str:
    """
    Récupère le numéro de ligne de la station à partir de son numéro.

    Args :
        station (int) : Le numéro de la station.

    Returns :
        str : Le numéro de ligne correspondant à la station.
    """
    station_info = sommets_df.loc[sommets_df['num_station'] == station]
    return station_info['num_line'].values[0]
