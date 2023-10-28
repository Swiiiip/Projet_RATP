from values import *


def need_line_precision(name: str) -> bool:
    return sommets_df.loc[(sommets_df['name_station'] == name)]['name_station'].count() != 1


def get_num_from_name_station_and_line(name: str, line: str | None) -> int:
    stations_info = sommets_df.loc[(sommets_df['name_station'] == name)]

    if line is None:
        return stations_info['num_station'].values[0]

    else:
        station = stations_info.loc[stations_info['num_line'] == line]
        return station['num_station'].values[0]


def get_real_name(station: str) -> str:
    station = station.lower()

    station_info = sommets_df.loc[sommets_df['name_station'].str.lower() == station]

    return station_info['name_station'].values[0]



def get_name_station_from_num(num: int) -> str:
    station_info = sommets_df.loc[sommets_df['num_station'] == num]
    return station_info['name_station'].values[0]


def get_ligne_station(station: int) -> str:
    station_info = sommets_df.loc[sommets_df['num_station'] == station]
    return station_info['num_line'].values[0]


def is_station_valide(nom_station: str) -> bool:
    nom_station = nom_station.lower()
    sommets_df_lower = sommets_df['name_station'].str.lower()

    return nom_station in sommets_df_lower.tolist()


'''def get_neighbors(num: int) -> pd.Series[int] | pd.DataFrame[int, int]:
    neighbors = aretes_df.loc[aretes_df['num_start'] == num]

    return neighbors['num_destination']'''


def is_same_line(station: str, line: str) -> bool:
    num_line_station = sommets_df.at[station, 'num_line']

    return num_line_station == line


def is_same_direction(path: list[int], station: str, branchement: int) -> bool:
    branchement_station = sommets_df.at[station, 'branchement']

    if branchement_station != branchement:
        return station in path

    else:
        return True


def find_direction(path: list[int], current_station: int, next_station: int, line: str) -> str | None:
    return find_direction_recursive(path, current_station, next_station, line)


def find_direction_recursive(path: list[int], current_station: int, next_station: int, line: str) -> str | None:
    current_station_info = sommets_df.loc[current_station]
    next_station_info = sommets_df.loc[next_station]

    branchement = current_station_info['branchement']

    edges = aretes_df.loc[(aretes_df['num_start'] == next_station) | (aretes_df['num_destination'] == next_station)]

    possible_station = pd.concat([edges['num_start'], edges['num_destination']]).unique()

    for station in possible_station:
        if (station != current_station and station != next_station
                and is_same_line(station, line) and is_same_direction(path, station, branchement)):
            direction = find_direction_recursive(path=path, current_station=next_station, next_station=station,
                                                 line=line)
            if direction:
                return direction

    # dernier cas
    if edges['num_start'].count() == 1:
        return next_station_info['name_station']

    # Aucun chemin jusqu'à un terminus trouvé
    return None


def time_format(seconds: int) -> str:
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
