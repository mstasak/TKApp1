import tkinter as tk
#from tkinter import ttk

from .apppagebase import AppPageBase

class AppBase:
    """Base class for an application"""

    app_name: str = "(undefined)"
    _default_position = [0, 0]
    _default_size = [800, 600]

    def __init__(self) -> None :
        self.root = tk.Tk()
        self.main_page: AppPageBase | None = None

    def run(self) -> bool : 
        self.load_page()
        self.root.mainloop()
        self.unload_page()
        return True
        
    def load_page(self) -> None:
        self.root.frame = self.main_page.build_page()

    def unload_page(self) -> None:
        self.root.frame = None
        
    