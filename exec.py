import values
from functions.algo import *

# Vérifier la connexité du graphe
if is_connected(aretes_df=values.aretes_df):
    print("Le graphe est déjà connexe.")
else:
    print("Le graphe n'est pas connexe. Ajout d'arêtes pour le rendre connexe...")

# Exemple d'utilisation :
start_station = getNumFromNameStation("Carrefour Pleyel")
print(start_station)
end_station = getNumFromNameStation("Villejuif, P. Vaillant Couturier")
print(end_station)
shortest_path = bellman_ford(values.aretes_df, start_station, end_station)
print(f"Plus court chemin de la station {start_station} à la station {end_station} :")
print(shortest_path)

#print(prim(aretes_df))

''' sommets.head()
   num_station     name_station num_line  terminus  branchement
0            0         Abbesses      12       True            0
1            1  Alexandre Dumas       2       True            0
2            2     Alma Marceau       9       True            0
3            3           Alésia       4       True            0
4            4   Anatole France       3       True            0
'''

''' aretes.head()
   num_start  num_destination  time_secondes
0          0              238             41
1          0              159             46
2          1               12             36
3          1              235             44
4          2              110             69
'''
