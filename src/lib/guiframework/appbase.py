import tkinter as tk
from tkinter import ttk

from .apppagebase import AppPageBase

class AppBase:
    """Base class for an application"""

    app_name: str = "(undefined)"
    _default_position = [0, 0]
    _default_size = [800, 600]

    def __init__(self) -> None :
        self.root = tk.Tk()

    def run(self) -> bool : 
        self._load_page(self._main_page)
        self.root.mainloop()
        self._unload_page()
        return True
        
    def _load_page(self, page: AppPageBase) -> None:
        self.root.frame = page.buildpage()

    def _unload_page(self) -> None:
        self.root.frame = None
        
    