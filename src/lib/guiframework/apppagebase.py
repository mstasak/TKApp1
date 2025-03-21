import tkinter as tk
from tkinter import ttk

class AppPageBase:
    """ A page (window content definition) of an app """
    
    def __init__(self, root: tk.Tk) -> None :
        self.root = root #copy of ui parent's MyApp.root
        self.mainframe: tk.Frame | None = None

    def build_page(self) -> tk.Frame :
        pass

#    pass
