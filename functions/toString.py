from functions.utils import get_name_station_from_num, get_ligne_station, find_direction, time_format
from values import sommets_df


def get_instructions(shortest_path: list[int], total_time: int) -> str:
    first_station = shortest_path[0]
    if len(shortest_path) == 1:
        second_station = shortest_path[0]
        last_station = shortest_path[0]
    else:
        second_station = shortest_path[1]
        last_station = shortest_path[-1]

    instructions = ''

    current_location = get_name_station_from_num(first_station)

    line = get_ligne_station(first_station)

    instructions += f"- Vous êtes à {current_location}, ligne {line}.\n"

    direction = find_direction(path=shortest_path, current_station=first_station, next_station=second_station,
                               line=line)

    if direction:
        instructions += f"- Prenez la ligne {line} direction {direction}\n"

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
                instructions += f"- A {name_changement}, changez et prenez la ligne {line} direction {direction}.\n"

    final_location = get_name_station_from_num(last_station)
    instructions += f"- Vous devriez arriver à {final_location} (ligne {get_ligne_station(last_station)}) { 'dans environ '+time_format(total_time) if total_time else 'INSTANTANÉMENT!!!'}."

    return instructions
