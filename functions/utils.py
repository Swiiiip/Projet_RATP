from values import *


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

    # Aucun chemin jusqu'à un terminus trouvé
    return None
