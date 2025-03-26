import tkinter as tk
from tkinter import ttk

from typing_extensions import override

from lib.guiframework import AppPageBase
from lib.datasource.sqlite import DataSource


class MyMainPage(AppPageBase):
    """ Main page of app """

    def __init__(self, root:tk.Tk) -> None :
        super().__init__(root)
        self.panel_list_buttons = None
        self.project_list: tk.Listbox | None = None
        self.scrollbar: tk.Scrollbar | None = None
        self.search_text = tk.StringVar(value="")
        self._init_db()

    @staticmethod
    def _init_db():
        db = DataSource()
        db.create_database()  # does nothing if it already exists
        #db.create_schema()  # create_database will create schema and load sample data
        #db.open_database()
        #db.load_sample_data()
        #$db.close_database()

    @override
    def build_page(self) -> tk.Frame :
        root: tk.Tk = self.root
        #mainframe: tk.Frame = tk.Frame(master=self.root, padding=10)
        self.mainframe = ttk.Frame(master=root, padding="3 3 12 12")
        root.title("Projects")
        root.geometry("800x600")

        self.mainframe.grid(column=0, row=0, sticky='nwes')
        self.mainframe.columnconfigure(10, weight = 0, minsize = "20")
        self.mainframe.columnconfigure(20, weight = 40, pad = "20")
        self.mainframe.columnconfigure(30, weight = 0)
        self.mainframe.columnconfigure(40, weight = 0,minsize = "20")
        self.mainframe.columnconfigure(50, weight = 60,pad = "30")
        self.mainframe.columnconfigure(60, weight = 0, minsize = "20")
        self.mainframe.rowconfigure(10, weight = 0)
        self.mainframe.rowconfigure(15, weight = 0)
        self.mainframe.rowconfigure(20, weight = 100)
        self.mainframe.rowconfigure(30, weight = 0)

        self.label_list = ttk.Label(self.mainframe, text="Projects")
        self.label_list.grid(column=20, row=10, columnspan=2, sticky='ew')
        self.label_details = ttk.Label(self.mainframe, text="Details")
        self.label_details.grid(column=50, row=10, sticky='ew')

        self.panel_search = ttk.Frame(self.mainframe)
        self.panel_search.grid(column=20, columnspan=2, row=15, sticky='nsew')
        self.label_search = ttk.Label(self.panel_search, text="Search:")
        self.label_search.pack(side='left', expand=True)
        self.entry_search = ttk.Entry(self.panel_search, width=40, textvariable=self.search_text)
        self.entry_search.pack(side='left', expand=True)

        self.project_list = tk.Listbox(self.mainframe, bg= 'yellow', fg='black', bd='2',
                                       # height=10, width=15,
                                       font='Courier 10',
                                       highlightcolor='cyan')
        self.scrollbar = tk.Scrollbar(self.mainframe, orient=tk.VERTICAL)
        self.project_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.project_list.yview)
        self.project_list.grid(column=20, row=20, sticky='nsew')
        self.scrollbar.grid(column=30, row=20, sticky='ns')

        self.panel_list_buttons = ttk.Frame(self.mainframe)
        self.panel_list_buttons.grid(column=20, columnspan=2, row=30, sticky='nsew')
        self.button_new = ttk.Button(self.panel_list_buttons, text="New")
        self.button_new.pack()

        self.panel_details = ttk.Frame(self.mainframe, padding='0 0 0 0')
        self.panel_details.grid(column=50, row=15, rowspan=2, sticky='nsew', ipadx=0, ipady=0, padx=0, pady=0)
        self.label_details_placeholder = ttk.Label(self.panel_details, text="Details Placeholder blah blah blah blah blah blah blah blah blah blah blah blah blah")
        self.label_details_placeholder.pack(side='top', fill='x')

        self.panel_detail_buttons = ttk.Frame(self.mainframe) #, sticky='ew'
        self.panel_detail_buttons.grid(column=50, row=30, sticky='nsew')
        self.button_delete = ttk.Button(self.panel_detail_buttons, text="Delete")
        self.button_delete.pack(side='left', expand=True) # fill='none', ipadx=0, ipady=0)
        self.button_edit = ttk.Button(self.panel_detail_buttons, text="Edit")
        self.button_edit.pack(side='left', expand=True) # fill='none', ipadx=0, ipady=0)

        self.load_project_list(reg_exp_pattern="")

        return self.mainframe

    def load_project_list(self, reg_exp_pattern: str = ""):
        # for i in range(1,20):
        #     self.project_list.insert(tk.END,"apples")
        #     self.project_list.insert(tk.END,"oranges")
        #     self.project_list.insert(tk.END,"plums")
        #     self.project_list.insert(tk.END,"grapes")
        #     self.project_list.insert(tk.END,"bananas")
        for i in range(1, 50):
            for row in DataSource().get_project_list(reg_exp_pattern):
                self.project_list.insert(tk.END, row[1])

