import pandas as pd


def getData():
    with open(file='metro.txt', mode='r', encoding='utf-8') as f:
        lines = f.readlines()[13:]

        sommets_data = []
        aretes_data = []

        for line in lines:
            elements = line.strip().split(';')
            premiere_colonne = elements[0].split(' ')

            if premiere_colonne[0] == 'V':
                nom_sommet = ' '.join(premiere_colonne[2:]) if len(premiere_colonne) > 2 else ''
                num_sommet = int(premiere_colonne[1])
                num_line = elements[1]
                derniere_colonne = elements[-1].split()
                terminus = derniere_colonne[0]
                branchement = int(derniere_colonne[1])
                sommets_data.append([num_sommet, nom_sommet.strip(), num_line, terminus, branchement])
            else:
                num_start = int(premiere_colonne[1])
                num_end = int(premiere_colonne[2])
                time = int(premiere_colonne[3])
                aretes_data.append([num_start, num_end, time])

        sommets_df = pd.DataFrame(sommets_data,
                                  columns=['num_station', 'name_station', 'num_line', 'terminus', 'branchement'])
        aretes_df = pd.DataFrame(aretes_data,
                                 columns=['num_start', 'num_destination', 'time_secondes'])

        sommets_df['num_line'] = [value.replace(' ', '') for value in sommets_df['num_line']]

    return sommets_df, aretes_df