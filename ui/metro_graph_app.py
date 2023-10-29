import tkinter as tk
from os import path, getcwd
from tkinter import simpledialog, messagebox

from utils.time_format import time_format
from algo.algo import prim, bellman_ford, is_connexe
from data.values import station_coordinates, sommets_df, decalage_y, circle_radius, graph, bg_color, fg_color, \
    light_color
from utils.get_data import get_name_station_from_num, get_num_from_name_station_and_line
from utils.get_instructions import get_instructions


class MetroGraphApp:
    def __init__(self, master: tk.Tk) -> None:
        """
        Initialise l'application de visualisation du métro parisien.

        Args :
            master (tk.Tk) : La fenêtre principale de l'application.
        """
        self.selected_journey = None
        self.canvas = None
        self.side_panel = None
        self.master = master
        master.title("RATP++")
        master.geometry(f"{800}x{500}")

        self.logo_ratp = tk.PhotoImage(file=path.join(getcwd(), "data", "assets", "logo_ratp.png"))
        self.logo_ratp = self.logo_ratp.subsample(7)

        self.menu_label = tk.Label(master, image=self.logo_ratp, font=("Arial", 36), bg=light_color)
        self.menu_label.image = self.logo_ratp
        self.menu_label.pack(pady=30)

        self.VerifConnex = tk.Button(master, text="Vérifier la connexité", command=self.check_connex, fg=fg_color,
                                     bg=bg_color, font=("Arial", 24), width=25)
        self.VerifConnex.pack(pady=10)

        self.Trajet = tk.Button(master, text="Prendre la route", command=self.afficher_trajet, fg=fg_color, bg=bg_color,
                                font=("Arial", 24), width=25)
        self.Trajet.pack(pady=10)

        self.quit_button = tk.Button(master, text="Quitter", command=master.quit, fg=bg_color, bg=fg_color,
                                     font=("Arial", 24), width=25)
        self.quit_button.pack(pady=10)
        print("Application démarrée")
        print('--------------------------')

    def metro_line_input_dialog(self, station: str, lines: list[str]) -> str:
        """
        Ouvre une boîte de dialogue pour permettre à l'utilisateur de choisir la ligne de métro pour un arrêt de métro.

        Args :
            station (str) : L'arrêt de métro concerné.
            lines (list[str]) : La liste des lignes possibles.

        Returns :
            str : La ligne de métro sélectionnée par l'utilisateur.
        """
        while True:
            user_input = simpledialog.askstring("Préciser ligne de métro",
                                                f"Plusieurs lignes ont été détectées pour la station "
                                                f"{station}\n"
                                                f"Voici les lignes possibles : {lines}\n")

            if user_input not in lines or user_input is None:
                messagebox.showerror("Erreur", "Ligne inconnue, veuillez saisir une des lignes proposées!")
                self.master.withdraw()
            else:
                return user_input

    def close_all_popups(self):
        """
        Ferme toutes les fenêtres popup.
        """
        for window in self.master.winfo_children():
            if isinstance(window, tk.Toplevel):
                window.destroy()

    def check_connex(self) -> None:
        """
        Vérifie si le graphe du métro parisien est connexe et affiche un message.
        """
        messagebox.showinfo(title="Connexité du métro parisien",
                            message="Le réseau parisien " + ("est bel et bien" if is_connexe() else "n'est pas")
                                    + " connexe.")

    def afficher_trajet(self) -> None:
        """
        Affiche la fenêtre de sélection du trajet.
        """
        self.selected_journey = {'start': None, 'end': None}
        self.close_all_popups()
        self.display_map_with_stations()

    def display_map_with_stations(self) -> None:
        """
        Affiche la carte avec les stations et ouvre la fenêtre de sélection du trajet.
        """
        popup = tk.Toplevel(self.master, bg=bg_color)
        popup.title("Allons-y!")

        original_image = tk.PhotoImage(file=path.join(getcwd(), "data", "assets", "metrof_r.png"))
        self.create_canvas(popup, original_image)

        side_panel_width = 300
        side_panel_size = (side_panel_width, original_image.height())
        self.setup_sidebar(popup, side_panel_size)

        panel_components = self.side_panel.winfo_children()
        self.setup_map(panel_components)

    def create_canvas(self, trajet_window: tk.Toplevel, original_image: tk.PhotoImage) -> None:
        """
        Crée un canevas avec l'image de fond.

        Args :
            trajet_window (tk.Toplevel) : La fenêtre de sélection du trajet.
            original_image (tk.PhotoImage) : L'image de fond pour le canevas.
        """
        self.canvas = tk.Canvas(trajet_window, width=original_image.width(), height=original_image.height())
        self.canvas.create_image(0, 0, image=original_image, anchor=tk.NW)
        self.canvas.image = original_image
        self.canvas.grid(row=0, column=0)

    def setup_map(self, panel_components: list) -> None:
        """
        Configure la carte avec les stations.

        Args :
            panel_components (list) : Les composants de la fenêtre de sélection du trajet.
        """
        start_station_label = panel_components[0]
        end_station_label = panel_components[2]
        instructions_label = panel_components[-1]

        self.reset_input()

        def on_station_click(event: tk.Event) -> None:
            """
            Réagit au clic sur une station sur la carte.

            Args :
                event (tk.Event) : L'événement de clic de la souris.

            Cette fonction met à jour les informations sur la station sélectionnée.
            """
            station_number = event.widget.find_withtag(tk.CURRENT)[0]
            station_name = ' '.join(event.widget.gettags(station_number)[:-1])

            if self.selected_journey['start'] is None or self.selected_journey['end'] is None:
                self.change_station_radius(station_number, 1.75)
                self.change_station_color(station_number, 'red')
                instructions_label.config(text="Veuillez sélectionner la station d'arrivée.")

            if station_name == "Even Nicer :P":
                print("Très beau choix ;)")
                return

            if self.selected_journey['start'] is None:
                self.selected_journey['start'] = station_name
                start_station_label.config(text=station_name)
                print(f"Départ :\n {station_name}")

            elif self.selected_journey['end'] is None:
                self.selected_journey['end'] = station_name
                end_station_label.config(text=station_name)
                print(f"Arrivée :\n {station_name}")

            else:
                self.side_panel.winfo_children()[-1].config(
                    text="Vous avez déjà choisi une station de départ et une station d'arrivée.")
                print("\033[91mVous avez déjà choisi une station de départ et une station d'arrivée.\033[0m")

        for station_info, (x, y) in station_coordinates.items():
            y -= decalage_y

            circle = self.canvas.create_oval(x - circle_radius, y - circle_radius, x + circle_radius, y + circle_radius,
                                             fill="black")

            self.canvas.tag_bind(circle, "<Button-1>", on_station_click)
            self.canvas.itemconfig(circle, tag=station_info)

    def setup_sidebar(self, trajet_window: tk.Toplevel, size: tuple[int, int]) -> None:
        """
        Configure la barre latérale avec les composants du trajet.

        Args :
            trajet_window (tk.Toplevel) : La fenêtre de sélection du trajet.
            size (tuple[int, int]) : La taille de la barre latérale (largeur, hauteur).
        """
        width, height = size
        self.side_panel = tk.Frame(trajet_window, width=width, height=height, bg=bg_color, padx=50)

        start_station_label = tk.Label(self.side_panel, text='', font=("Arial", 16), bg=bg_color, wraplength=width)
        start_station_label.pack(pady=10)

        arrow_image = tk.PhotoImage(file=path.join(getcwd(), "data", "assets", "arrow.png"))
        arrow_label = tk.Label(self.side_panel, image=arrow_image, bg=bg_color)
        arrow_label.image = arrow_image
        arrow_label.pack(pady=5)

        end_station_label = tk.Label(self.side_panel, text='', font=("Arial", 16), bg=bg_color, wraplength=width)
        end_station_label.pack(pady=10)

        def on_calculate_path_click() -> None:
            """
            Réagit au clic sur le bouton "Calculer B-F".

            Cette fonction calcule le chemin Bellman-Ford entre les stations de départ et d'arrivée,
            affiche les instructions, et affiche le chemin sur la carte.
            """

            if self.selected_journey['start'] is None:
                text = "Veuillez sélectionner la station de départ."
                print('\033[91m' + text + '\033[0m')

            elif self.selected_journey['end'] is None:
                text = "Veuillez sélectionner la station d'arrivée."
                print('\033[91m' + text + '\033[0m')

            else:
                try:
                    need_reset = False
                    self.verif_ligne()
                except Exception:
                    print('\033[91mVous devez reset avant de pouvoir utiliser Bellman-ford à nouveau\033[0m')
                    need_reset = True
                    text = "Vous devez reset avant de pouvoir utiliser Bellman-ford à nouveau"

                if not need_reset:
                    bellman_ford_path, total_time = bellman_ford(num_start=self.selected_journey['start'],
                                                                 num_destination=self.selected_journey['end'])
                    text = get_instructions(bellman_ford_path, total_time)
                    self.display_path_on_map(bellman_ford_path)

            instructions_label.config(text=text)

        calculate_path_button = tk.Button(self.side_panel, text="Calculer B-F", font=("Arial", 16), fg=fg_color,
                                          bg=light_color, command=on_calculate_path_click, width=20)

        calculate_path_button.pack(pady=5)

        reset_button = tk.Button(self.side_panel, text="Reset", font=("Arial", 16), bg="#F15928", fg=light_color,
                                 command=lambda: self.reset_input(), width=20)
        reset_button.pack(pady=5)

        acpm_button = tk.Button(self.side_panel, text="Calculer ACPM", font=("Arial", 16), bg=fg_color, fg=light_color,
                                command=self.display_acpm_on_map, width=20)
        acpm_button.pack(pady=5)

        if self.selected_journey['start'] is None:
            start_station_label['text'] = "?"
        if self.selected_journey['end'] is None:
            end_station_label['text'] = "?"

        instructions_label = tk.Label(self.side_panel, text='', font=("Arial", 12, 'italic'), bg=bg_color,
                                      fg=light_color, wraplength=width,
                                      justify=tk.LEFT)
        instructions_label.pack(pady=5)

        self.side_panel.grid(row=0, column=1)
        self.side_panel.pack_propagate(True)

    def display_acpm_on_map(self) -> None:
        """
        Affiche l'arbre couvrant de poids minimum (ACPM) sur la carte.
        """
        acpm, weight = prim()
        print(f"\nApplication de Prim : l'arbre couvrant minimal a un poids de "
              f"{time_format(weight)}\n")

        self.reset_input()

        for vertex, edges in acpm.items():
            for edge, weight in edges:
                x1, y1 = station_coordinates[get_name_station_from_num(vertex)]
                x2, y2 = station_coordinates[get_name_station_from_num(edge)]

                y1 -= decalage_y
                y2 -= decalage_y

                self.canvas.create_line(x1, y1, x2, y2, fill="blue", width=5, tag="acpm")

    def change_station_color(self, circle_num: int, color: str) -> None:
        """
        Change la couleur d'une station sur la carte.

        Args :
            circle_num (int) : Le numéro de la station sur la carte.
            color (str) : La couleur à appliquer.
        """
        self.canvas.itemconfig(circle_num, fill=color)

    def change_station_radius(self, circle_num: int, size_multiplier: float) -> None:
        """
        Change le rayon d'une station sur la carte.

        Args :
            circle_num (int) : Le numéro de la station sur la carte.
            size_multiplier (float) : Le multiplicateur de taille.
        """
        x1, y1, x2, y2 = self.canvas.coords(circle_num)

        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        new_radius = circle_radius * size_multiplier

        new_x1 = center_x - new_radius
        new_y1 = center_y - new_radius
        new_x2 = center_x + new_radius
        new_y2 = center_y + new_radius

        self.canvas.coords(circle_num, new_x1, new_y1, new_x2, new_y2)

    def reset_input(self) -> None:
        """
        Réinitialise la sélection du trajet.
        """
        print("\nRéinitialisation...\n")

        self.selected_journey['start'], self.selected_journey['end'] = None, None
        self.side_panel.winfo_children()[0].config(text="?")
        self.side_panel.winfo_children()[2].config(text="?")
        self.side_panel.winfo_children()[-1].config(text="Veuillez sélectionner la station de départ.")
        self.canvas.delete("bellman-ford")
        self.canvas.delete("acpm")
        for circle_num in self.canvas.find_all()[1:]:
            self.change_station_radius(circle_num, 1)
            self.change_station_color(circle_num, "black")

    def verif_ligne(self) -> None:
        """
        Vérifie si la station sélectionnée a besoin d'une précision de ligne.
        """
        result = []
        instructions_label = (self.side_panel.winfo_children())[-1]

        for station in self.selected_journey.values():
            intersecting_lines = list(sommets_df.loc[(sommets_df["name_station"] == station)]["num_line"])

            if len(intersecting_lines) > 1:
                while True:
                    try:
                        user_input = (
                            self.metro_line_input_dialog(station, intersecting_lines))
                        result.append(get_num_from_name_station_and_line(name=station, line=user_input))
                        instructions_label.config(text=f"Veuillez préciser la ligne pour {station} dans le popup!")
                        break

                    except IndexError:
                        print("\033[91mLigne incorrect. Veuillez réessayer.\033[0m\n")
            else:
                result.append(get_num_from_name_station_and_line(name=station))
                instructions_label.config(text='')

        self.selected_journey['start'], self.selected_journey['end'] = result

    def display_path_on_map(self, path: list[int]) -> None:
        """
        Affiche le chemin sélectionné sur la carte.

        Args :
            path (list[int]) : La liste des stations du chemin.
        """
        line_color = "red"
        line_width = 5

        for i in range(len(path) - 1):
            start_station = path[i]
            end_station = path[i + 1]

            start_x, start_y = station_coordinates[get_name_station_from_num(start_station)]
            end_x, end_y = station_coordinates[get_name_station_from_num(end_station)]

            start_y -= decalage_y
            end_y -= decalage_y

            self.canvas.create_line(start_x, start_y, end_x, end_y, fill=line_color, width=line_width,
                                    tag="bellman-ford")
