def safeIntInput(message, errorMessage, begin, end):
    result = -1
    while result == -1 or result < begin or result > end:
        try:
            result = int(input(message + "\n\n\n"))
        except ValueError:
            print("\n\n\n" + errorMessage)
        else:
            if result < begin or result > end:
                print("\n\n\n" + errorMessage)
    return result


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d hours %02d minutes" % (hour, minutes)

import tkinter as tk
from tkinter import ttk

class MetroGraphApp:
    def __init__(self, master):
        self.master = master
        master.title("Projet Graphe 2024 - Enzo / Jade / Ahmad / Cedric")
        master.geometry("1000x800")  # Dimensions modifiées

        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 24), padding=20)

        self.menu_label = tk.Label(master, text="Menu :", font=("Arial", 36))
        self.menu_label.pack(pady=30)  # Espacement modifié

        self.connexity_button = ttk.Button(master, text="Vérifier Connexité", command=self.check_connexity, style='TButton')
        self.connexity_button.pack(pady=20)  # Espacement modifié

        self.shortest_path_button = ttk.Button(master, text="Calculer Plus Court Chemin", command=self.calculate_shortest_path, style='TButton')
        self.shortest_path_button.pack(pady=20)  # Espacement modifié

        self.minimum_spanning_tree_button = ttk.Button(master, text="Calculer Arbre Couvrant", command=self.calculate_minimum_spanning_tree, style='TButton')
        self.minimum_spanning_tree_button.pack(pady=20)  # Espacement modifié

        self.quit_button = ttk.Button(master, text="Quitter", command=master.quit, style='TButton')
        self.quit_button.pack(pady=20)  # Espacement modifié

    def check_connexity(self):
        # Mettez ici le code pour vérifier la connexité du graphe
        print("Fonction à implémenter : Vérification de la connexité")

    def calculate_shortest_path(self):
        # Mettez ici le code pour calculer le plus court chemin
        print("Fonction à implémenter : Calcul du plus court chemin")

    def calculate_minimum_spanning_tree(self):
        # Mettez ici le code pour calculer l'arbre couvrant de poids minimum
        print("Fonction à implémenter : Calcul de l'arbre couvrant de poids minimum")

if __name__ == "__main__":
    root = tk.Tk()
    app = MetroGraphApp(root)
    root.mainloop()