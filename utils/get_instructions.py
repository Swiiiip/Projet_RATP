from data.values import sommets_df
from utils.get_data import get_name_station_from_num, get_ligne_station
from utils.time_format import time_format
from utils.find_direction import find_direction


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
