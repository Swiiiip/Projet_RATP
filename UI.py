from functions.algo import prim, bellman_ford, is_connexe
from functions.data import get_graph
from functions.toString import get_instructions
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

from functions.utils import need_line_precision, get_num_from_name_station_and_line, \
    time_format, get_name_station_from_num
from values import station_coordinates, sommets_df

decalage_y = 34


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


def display_path_on_map(path):    # Initialize line attributes
    line_color = "red"
    line_width = 5

    # Display the path as lines connecting stations
    for i in range(len(path) - 1):
        start_station = path[i]
        end_station = path[i + 1]

        # Get coordinates of the start and end stations
        start_x, start_y = station_coordinates[get_name_station_from_num(start_station)]
        end_x, end_y = station_coordinates[get_name_station_from_num(end_station)]

        start_y -= decalage_y
        end_y -= decalage_y

        # Draw a line connecting the stations
        canvas.create_line(start_x, start_y, end_x, end_y, fill=line_color, width=line_width, tag="bellman-ford")


def metro_line_input_dialog(parent, prompt, lines):
    while True:
        user_input = simpledialog.askstring("Préciser ligne de métro", prompt)
        if user_input is None:
            return None
        if user_input in lines:
            return user_input
        else:
            messagebox.showerror("Erreur", "Ligne inconnue, veuillez saisir une des lignes proposées!")


def display_acpm_on_map():
    acpm = prim(get_graph())[0]

    for vertex, edges in acpm.items():
        for edge, weight in edges:

            x1, y1 = station_coordinates[get_name_station_from_num(vertex)]
            x2, y2 = station_coordinates[get_name_station_from_num(edge)]

            y1 -= decalage_y
            y2 -= decalage_y

            canvas.create_line(x1, y1, x2, y2, fill="blue", width=5, tag="acpm")


def reset_input():
    selected_journey['start'], selected_journey['end'] = None, None
    side_panel.winfo_children()[0].config(text="Cliquez sur votre station de départ.")
    side_panel.winfo_children()[1].config(text="")
    side_panel.winfo_children()[5].config(text="")
    canvas.delete("bellman-ford")
    canvas.delete("acpm")


def Check_connex():
    # Mettez ici le code pour vérifier la connexité du graphe
    graph = get_graph()
    print("Ce graphe " + ("est" if is_connexe(graph) else "n'est pas") + " connexe.")
    print("Fonction à implémenter : Vérification de la connexité")


def Calcul_Court_Chemin():
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
    print(get_instructions(shortest_path, total_time))


def Calcul_Arbre_Couvrant():
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


def create_canvas(trajet_window, original_image):
    # Create a Canvas for drawing the image
    global canvas
    canvas = tk.Canvas(trajet_window, width=original_image.width(), height=original_image.height())
    canvas.create_image(0, 0, image=original_image, anchor=tk.NW)
    canvas.image = original_image
    canvas.grid(row=0, column=0)

def setup_map(trajet_window, original_image, panel_components):
    start_station_label = panel_components[0]
    end_station_label = panel_components[1]

    def on_station_click(event):
        station_number = event.widget.find_withtag(tk.CURRENT)[0]
        station_name = ' '.join(event.widget.gettags(station_number)[:-1])

        if station_name == "Even Nicer :P":
            print("Nice numbers ;)")
            return

        if selected_journey['start'] is None:
            selected_journey['start'] = station_name
            start_station_label.config(text=f"Départ :\n {station_name}")

        elif selected_journey['end'] is None:
            selected_journey['end'] = station_name
            end_station_label.config(text=f"Arrivée :\n {station_name}")

        else:
            side_panel.winfo_children()[-1].config(text="Vous avez déjà choisi une station de départ et une station d'arrivée.")

    # Initialize
    circle_radius = 5

    # Display clickable and sizeable circles for station coordinates
    for station_name, (x, y) in station_coordinates.items():
        y -= decalage_y

        circle = canvas.create_oval(x - circle_radius, y - circle_radius, x + circle_radius, y + circle_radius,
                                    fill="red")

        # Bind a click event to each circle
        canvas.tag_bind(circle, "<Button-1>", on_station_click)
        canvas.itemconfig(circle, tag=station_name)


def setup_sidebar(trajet_window, size):
    width, height = size

    # Display side panel with instructions
    global side_panel
    side_panel = tk.Frame(trajet_window, width=width, height=height, bg="white")

    # Display selected journey
    start_station_label = tk.Label(side_panel, text='', font=("Arial", 16), bg="white", wraplength=width)
    start_station_label.pack(pady=5)

    end_station_label = tk.Label(side_panel, text='', font=("Arial", 16), bg="white", wraplength=width)
    end_station_label.pack(pady=5)

    def on_calculate_path_click():

        if selected_journey['start'] is None:
            text = "Veuillez sélectionner la station de départ."
        elif selected_journey['end'] is None:
            text = "Veuillez sélectionner la station d'arrivée."
        else:
            verif_ligne()

            bellman_ford_path, total_time = bellman_ford(get_graph(), selected_journey['start'],
                                                         selected_journey['end'])
            text = get_instructions(bellman_ford_path, total_time)
            display_path_on_map(bellman_ford_path)

            # selected_journey['start'], selected_journey['end'] = None, None

        instructions_label.config(text=text)

    # Calculate path button (Bellman-Ford)
    calculate_path_button = tk.Button(side_panel, text="Calculer B-F", font=("Arial", 16), bg="white",
                                      command=on_calculate_path_click)

    calculate_path_button.pack(pady=5)

    # Reset button
    reset_button = tk.Button(side_panel, text="Reset", font=("Arial", 16), bg="red", fg="white", command=lambda: reset_input())
    reset_button.pack(pady=5)

    # ACPM button
    acpm_button = tk.Button(side_panel, text="Calculer ACPM", font=("Arial", 16), bg="blue", fg="white", command=display_acpm_on_map)
    acpm_button.pack(pady=5)

    if selected_journey['start'] is None:
        start_station_label['text'] = "Cliquez sur votre station de départ."
    elif selected_journey['end'] is None:
        end_station_label['text'] = "Cliquez sur une station d'arrivée."

    instructions_label = tk.Label(side_panel, text='', font=("Arial", 12), bg="white", wraplength=width, justify=tk.LEFT)
    instructions_label.pack(pady=5)

    side_panel.grid(row=0, column=1)
    side_panel.pack_propagate(True)

    return side_panel


def verif_ligne():
    result = []

    for station in selected_journey.values():
        intersecting_lines = list(sommets_df.loc[(sommets_df["name_station"] == station)]["num_line"])

        if len(intersecting_lines) > 1:
            while True:
                try:
                    user_input = metro_line_input_dialog(canvas, f"Plusieurs lignes ont été détectées pour la station {station}\n"
                                                               f"Voici les lignes possibles : {intersecting_lines}\n",
                                                         intersecting_lines)
                    result.append(get_num_from_name_station_and_line(name=station, line=user_input))
                    break
                except IndexError:
                    print("Ligne incorrect. Veuillez réessayer.\n")
        else:
            result.append(get_num_from_name_station_and_line(name=station))

    selected_journey['start'], selected_journey['end'] = result


def display_map_with_stations():
    # Create a new window for displaying the image and circles
    popup = tk.Toplevel(root)
    popup.title("Allons-y!")

    original_image = tk.PhotoImage(file="metrof_r.png")
    create_canvas(popup, original_image)

    side_panel_width = 300
    side_panel_size = (side_panel_width, original_image.height())
    side_panel = setup_sidebar(popup, side_panel_size)

    panel_components = side_panel.winfo_children()
    setup_map(popup, original_image, panel_components)


def Afficher_Trajet():
    # Call the function to display the image with station labels and clickable red circles
    global selected_journey
    selected_journey = {'start': None, 'end': None}  # Reset selected journey

    display_map_with_stations()


class MetroGraphApp:
    def __init__(self, master):
        self.master = master
        master.title("Projet Graphe 2024 - Enzo / Jade / Ahmad / Cedric")
        master.geometry(f"{1200}x{800}")

        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 24), padding=20)

        button_options = {
            'style': 'TButton',
            'width': 30,
        }

        self.menu_label = tk.Label(master, text="MENU", font=("Arial", 36))
        self.menu_label.pack(pady=30)

        self.VerifConnex = ttk.Button(master, text="Vérifier Connexité", command=Check_connex, **button_options)
        self.VerifConnex.pack(pady=10)

        self.CourtChemin = ttk.Button(master, text="Calculer le plus court chemin", command=Calcul_Court_Chemin,
                                      **button_options)
        self.CourtChemin.pack(pady=10)

        self.ArbreCouvrant = ttk.Button(master, text="Calculer Arbre Couvrant", command=Calcul_Arbre_Couvrant,
                                        **button_options)
        self.ArbreCouvrant.pack(pady=10)

        self.Trajet = ttk.Button(master, text="Prendre la route", command=Afficher_Trajet, **button_options)
        self.Trajet.pack(pady=10)

        self.quit_button = ttk.Button(master, text="Quitter", command=master.quit, **button_options)
        self.quit_button.pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = MetroGraphApp(root)
    root.mainloop()
