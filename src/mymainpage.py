import tkinter as tk
from tkinter import ttk

from typing_extensions import override

from lib.guiframework import AppPageBase
from lib.datasource.sqlite import DataSource
class MyMainPage(AppPageBase):
    """ Main page of app """

    def __init__(self, root:tk.Tk) -> None :
        super().__init__(root)
        #self.feet = ""
        #self.meters = ""

    @override
    def build_page(self) -> tk.Frame :
        root: tk.Tk = self.root
        #mainframe: tk.Frame = tk.Frame(master=self.root, padding=10)
        mainframe = ttk.Frame(master=root, padding="3 3 12 12")
        mainframe.grid(sticky="nsew")
        root.geometry("800x600")
        root.title("Projects")

        mainframe.grid(column=0, row=0, sticky='nwes')
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        # self.project_list = tk.Listbox(mainframe, bg='yellow', fg='black', bd='1',
        #                                height='400', width='600', font='Courier New 10',
        #                                highlightcolor='cyan')
        self.project_list = tk.Listbox(mainframe, bg= 'yellow', fg='black', bd='1',
                                       height=10, width=15, font='Courier 10',
                                       highlightcolor='cyan')
        self.scrollbar = tk.Scrollbar(mainframe, orient=tk.VERTICAL)
        self.project_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.project_list.yview)
        self.project_list.grid(column=0, row=1, sticky='nsew')
        self.scrollbar.grid(column=1, row=1, sticky='ns')
        for i in range(1,20):
            self.project_list.insert(tk.END,"apples")
            self.project_list.insert(tk.END,"oranges")
            self.project_list.insert(tk.END,"plums")
            self.project_list.insert(tk.END,"grapes")
            self.project_list.insert(tk.END,"bananas")
        # self.feet = tk.StringVar()
        # self.feet.set("???")
        # feet_entry = ttk.Entry(mainframe, width=7, textvariable=self.feet)
        # feet_entry.grid(column=2, row=1, sticky=(tk.W, tk.E))
        #
        # self.meters = tk.StringVar()
        # self.meters.set("???")
        # ttk.Label(mainframe, textvariable=self.meters).grid(column=2, row=2, sticky=(tk.W, tk.E))
        #
        # ttk.Button(mainframe, text="Calculate", command=self.calculate).grid(column=3, row=3, sticky=tk.W)
        #
        # ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=tk.W)
        # ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=tk.E)
        # ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=tk.W)
        #
        # for child in mainframe.winfo_children():
        #     child.grid_configure(padx=5, pady=5)
        #
        # feet_entry.focus()
        # root.bind("<Return>", self.calculate)

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