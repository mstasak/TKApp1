import tkinter as tk
from tkinter import ttk

from typing_extensions import override

from lib.guiframework import AppPageBase
from lib.datasource.sqlite import DataSource
class MyMainPage(AppPageBase):
    """ Main page of app """

    def __init__(self, root:tk.Tk) -> None :
        super().__init__(root)
        self.feet = ""
        self.meters = ""

    @override
    def build_page(self) -> tk.Frame :
        root = self.root
        #mainframe: tk.Frame = tk.Frame(master=self.root, padding=10)
        mainframe = ttk.Frame(master=root, padding="3 3 12 12")

        root.title("Feet to Meters")

        mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.feet = tk.StringVar()
        self.feet.set("???")
        feet_entry = ttk.Entry(mainframe, width=7, textvariable=self.feet)
        feet_entry.grid(column=2, row=1, sticky=(tk.W, tk.E))

        self.meters = tk.StringVar()
        self.meters.set("???")
        ttk.Label(mainframe, textvariable=self.meters).grid(column=2, row=2, sticky=(tk.W, tk.E))

        ttk.Button(mainframe, text="Calculate", command=self.calculate).grid(column=3, row=3, sticky=tk.W)

        ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=tk.W)
        ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=tk.E)
        ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=tk.W)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        feet_entry.focus()
        root.bind("<Return>", self.calculate)

        return mainframe

    def calculate(self,*args):
        try:
            db = DataSource()
            db.open_database()
            db.load_sample_data()
            db.close_database()
            value = float(self.feet.get())
            self.meters.set(str(int(0.3048 * value * 10000.0 + 0.5)/10000.0))
        except ValueError:
            pass



"""
from tkinter import *
from tkinter import ttk

def calculate(*args):
    try:
        value = float(feet.get())
        meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
    except ValueError:
        pass


root = Tk()
root.title("Feet to Meters")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

feet = StringVar()
feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
feet_entry.grid(column=2, row=1, sticky=(W, E))

meters = StringVar()
ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))

ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)

ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

feet_entry.focus()
root.bind("<Return>", calculate)

root.mainloop()
"""