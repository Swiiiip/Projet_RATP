import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import tkinter as tk

from ui.metro_graph_app import MetroGraphApp
from data.values import light_color, data_base64

if __name__ == "__main__":
    root = tk.Tk()

    logo_ratp = tk.PhotoImage(data=data_base64["logo_ratp"])
    root.iconphoto(True, logo_ratp)
    root.configure(bg=light_color)
    app = MetroGraphApp(root)
    root.mainloop()
