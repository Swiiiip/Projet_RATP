from functions.algo import bellman_ford
from functions.utils import getNameStationFromNum, getLigneStation, find_direction, convert
from values import sommets_df


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
    print(f'\t- Vous devriez arriver à {final_location} dans environ {convert(total_time)}.')
