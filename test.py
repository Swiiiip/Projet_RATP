from functions.algo import *

start_station_name = "Saint-Lazare"
destination_station_name = "Villejuif, P. Vaillant Couturier"

while True:
    try:
        user_input = input(f"Précisez la ligne pour {start_station_name}: ") if need_line_precision(start_station_name) else None
        num_start = getNumFromNameStationAndLine(name=start_station_name, line=user_input)
        break
    except Exception as e:
        print("Ligne incorrect. Veuillez réessayer.\n")

while True:
    try:
        user_input = input(f"Précisez la ligne pour {destination_station_name} : ") if need_line_precision(destination_station_name) else None
        num_destination = getNumFromNameStationAndLine(name=destination_station_name, line=user_input)
        break
    except Exception as e:
        print("Ligne Incorrect. Veuillez réessayer.")

toString(num_start=num_start, num_destination=num_destination)
