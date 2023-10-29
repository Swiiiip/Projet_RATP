import tkinter as tk
from os import getcwd, path

from ui.metro_graph_app import MetroGraphApp
from data.values import light_color

if __name__ == "__main__":
    root = tk.Tk()
    logo_ratp = tk.PhotoImage(file=path.join(getcwd(), "..", "data", "assets", "logo_ratp.png"))
    root.iconphoto(True, logo_ratp)
    root.configure(bg=light_color)
    app = MetroGraphApp(root)
    root.mainloop()