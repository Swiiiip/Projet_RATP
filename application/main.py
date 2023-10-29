import tkinter as tk
from ui.metro_graph_app import MetroGraphApp

if __name__ == "__main__":
    print('Initialisation...')
    root = tk.Tk()
    app = MetroGraphApp(root)
    root.mainloop()
