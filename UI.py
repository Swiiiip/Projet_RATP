from functions.algo import prim, bellman_ford, is_connexe
from functions.data import get_graph
from functions.toString import display_instructions
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

from functions.utils import is_station_valide, get_real_name, need_line_precision, get_num_from_name_station_and_line, \
    time_format


def custom_input_dialog(parent, title, prompt):
    parent.withdraw()
    while True:
        user_input = simpledialog.askstring(title, prompt)
        if user_input is None:
            parent.deiconify()
            return None
        if is_station_valide(user_input):
            return user_input
        else:
            messagebox.showerror("Erreur", "Station inconnue, veuillez saisir une station valide.")


def check_connexity():
    # Mettez ici le code pour vérifier la connexité du graphe
    graph = get_graph()
    print("Ce graphe " + ("est" if is_connexe(graph) else "n'est pas") + " connexe.")
    print("Fonction à implémenter : Vérification de la connexité")


def calculate_shortest_path():
    # Demande de la station de départ
    start_station = custom_input_dialog(
        root,
        "Station de départ",
        "Entrez la station de départ:",
    )
    if start_station is None:
        return  # L'utilisateur a annulé

    # Demande de la station d'arrivée
    end_station = custom_input_dialog(
        root,
        "Station d'arrivée",
        "Entrez la station d'arrivée:",
    )
    if end_station is None:
        return  # L'utilisateur a annulé

    start_station = get_real_name(start_station)
    end_station = get_real_name(end_station)

    print(f"Station de départ : {start_station}")
    print(f"Station d'arrivée : {end_station}")
    root.deiconify()

    while True:
        try:
            user_input = input(f"Précisez la ligne pour {start_station}: ") \
                if need_line_precision(start_station) else None
            num_start = get_num_from_name_station_and_line(name=start_station, line=user_input)
            break
        except IndexError:
            print("Ligne incorrect. Veuillez réessayer.\n")

    while True:
        try:
            user_input = input(f"Précisez la ligne pour {end_station} : ") \
                if need_line_precision(end_station) else None
            num_destination = get_num_from_name_station_and_line(name=end_station, line=user_input)
            break
        except IndexError:
            print("Ligne Incorrect. Veuillez réessayer.")

    graph = get_graph()
    shortest_path, total_time = bellman_ford(graph, num_start, num_destination)
    display_instructions(shortest_path, total_time)


def calculate_minimum_spanning_tree():
    # Mettez ici le code pour calculer l'arbre couvrant de poids minimum
    graph = get_graph()
    prim_res, total_time = prim(graph)
    print(f"=============="
          f"\nAlgo de Prim :"
          f"\n=============="
          f"\nTemps total = {time_format(total_time)}"
          f"\nnb d'aretes = {len(prim_res)}"
          f"\nACPM :\n{prim_res}\n")

    print("Fonction à implémenter : Calcul de l'arbre couvrant de poids minimum")


class MetroGraphApp:
    def __init__(self, master):
        self.master = master
        master.title("Projet Graphe 2024 - Enzo / Jade / Ahmad / Cedric")
        master.geometry(f"{1000}x{800}")

        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 24), padding=20)

        self.menu_label = tk.Label(master, text="Menu :", font=("Arial", 36))
        self.menu_label.pack(pady=30)  # Espacement modifié

        self.connexity_button = ttk.Button(master, text="Vérifier Connexité", command=check_connexity,
                                           style='TButton')
        self.connexity_button.pack(pady=20)  # Espacement modifié

        self.shortest_path_button = ttk.Button(master, text="Calculer Plus Court Chemin",
                                               command=calculate_shortest_path, style='TButton')
        self.shortest_path_button.pack(pady=20)  # Espacement modifié

        self.minimum_spanning_tree_button = ttk.Button(master, text="Calculer Arbre Couvrant",
                                                       command=calculate_minimum_spanning_tree, style='TButton')
        self.minimum_spanning_tree_button.pack(pady=20)  # Espacement modifié

        self.quit_button = ttk.Button(master, text="Quitter", command=master.quit, style='TButton')
        self.quit_button.pack(pady=20)  # Espacement modifié


if __name__ == "__main__":
    root = tk.Tk()
    app = MetroGraphApp(root)
    root.mainloop()
