import tkinter as tk

from ui.metro_graph_app import MetroGraphApp
from data.values import light_color, images_base64


if __name__ == "__main__":
    root = tk.Tk()

    logo_ratp = tk.PhotoImage(data = images_base64["logo_ratp"])
    root.iconphoto(True, logo_ratp)
    root.configure(bg=light_color)
    app = MetroGraphApp(root)
    root.mainloop()