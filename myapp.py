# from mymainpage import MyMainPage
import tkinter as tk
from tkinter import ttk, Tk, Listbox, StringVar
from tkinter.ttk import Label, Scrollbar, Frame, Entry, Button
from typing import cast  # Any, List, Optional, Tuple, cast

from utility.servicedepot import ServiceDepot
# from typing_extensions import override
from datapanel import DataPanel
from datasource.sqlite import DataSource


class MyApp(tk.Frame):
    """App subclass, with customizations for this application"""

    # project_list_source: list[tuple[Any, ...]] | None
    # # services
    #
    # # widgets
    # root: Tk
    # panel_search: Frame
    # panel_detail: DataPanel
    # panel_buttons: Frame
    # label_list: Label
    # label_details: Label
    # label_search: Label
    # entry_search: Entry
    # project_list: Listbox
    # scrollbar: Scrollbar
    # button_new: Button
    # button_delete: Button
    # button_edit: Button
    #
    # # binding variables
    # search_text: tk.StringVar

    def __init__(self) -> None:
        super().__init__(padx=10, pady=10, background="Navy Blue")
        # self.app_name: str = "TKApp1"
        # self._default_position = [0, 0]
        # self._default_size = [1024, 768]
        # self.main_page: AppPageBase | None = MyMainPage(self)

        # services
        self.db: DataSource = ServiceDepot.db_service()

        # bind variables
        self.search_text: StringVar = StringVar(value="")

        # UI Widgets
        self.root: Tk = cast(Tk, self.master)
        self.grid(column=0, row=0, sticky='nwes')
        self.columnconfigure(10, weight=0, minsize="20")
        self.columnconfigure(20, weight=40, pad="20")
        self.columnconfigure(30, weight=0)
        self.columnconfigure(40, weight=0, minsize="20")
        self.columnconfigure(50, weight=60, pad="30")
        self.columnconfigure(60, weight=0, minsize="20")
        self.rowconfigure(10, weight=0)
        self.rowconfigure(15, weight=0)
        self.rowconfigure(20, weight=100)
        self.rowconfigure(30, weight=0, pad="10")
        self.root.title("Projects")
        self.root.geometry("1024x768")

        clear_panel_style: ttk.Style = ttk.Style()
        clear_panel_style.configure("clear.TFrame", foreground="clear",
                                    background="clear")
        self.panel_search:Frame = Frame(master=self, style='clear.TFrame')
        self.panel_search.grid(column=20, columnspan=11, row=10, sticky='nsew',
                               pady=10)
        # self.label_search = Label(self.panel_search, text="Search:")
        # self.label_search.pack(side='left', expand=True)
        self.entry_search: Entry = Entry(self.panel_search, width=40,
                                         textvariable=self.search_text)
        self.entry_search.pack(side='left', expand=True)
        self.button_search: Button = Button(self.panel_search, text="Search",
                                            command=self.on_search_pressed)
        self.button_search.pack(side='left', expand=True, pady=10)

        # self.label_list = Label(self, text="Projects")
        # self.label_list.grid(column=20, row=10, columnspan=2, sticky='ew')
        self.project_list: Listbox = Listbox(self, bg='aliceblue', fg='black', bd='2',
                                             # height=10, width=15,
                                             font='Courier 10',
                                             highlightcolor='cyan',
                                             exportselection=0)
        self.project_list.grid(column=20, row=20, sticky='nsew', pady=10)
        self.project_list.bind('<<ListboxSelect>>', self.on_item_selected)
        self.scrollbar: Scrollbar = Scrollbar(self, orient=tk.VERTICAL)
        self.project_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(column=30, row=20, sticky='nsew', pady=10)
        self.scrollbar.config(command=self.project_list.yview)

        self.label_details: Label = Label(self, text="Details")
        self.label_details.grid(column=50, row=10, sticky='ew', pady=10)
        self.panel_detail: DataPanel = DataPanel(self)
        self.panel_detail.grid(column=50, row=20, rowspan=6, sticky='nsew',
                               ipadx=5, ipady=5, padx=0, pady=10)

        self.panel_buttons: Frame = Frame(self)
        self.panel_buttons.grid(column=20, columnspan=31, row=30,
                                sticky='nsew')
        self.button_new: Button = Button(self.panel_buttons, text="New",
                                         command=self.on_new_pressed)
        self.button_new.pack(side='left', expand=True, pady=10)
        self.button_delete = Button(self.panel_buttons, text="Delete",
                                    command=self.on_delete_pressed)
        self.button_delete.pack(side='left', expand=True, pady=10)
        # fill='none', ipadx=0, ipady=0)
        self.button_edit = Button(self.panel_buttons, text="Edit",
                                  command=self.on_edit_pressed)
        self.button_edit.pack(side='left', expand=True, pady=10)
        # fill='none', ipadx=0, ipady=0)

        self.pack(expand=True)

        # further activities
        self._init_db()
        self.load_project_list(reg_exp_pattern="")
        # self.project_list = None
        # self.scrollbar = None

    def run(self) -> bool:
        self.mainloop()
        self.unload_page()
        return True

    def unload_page(self) -> None:
        self.children.clear()

    def load_project_list(self, reg_exp_pattern: str = "") -> None:
        self.project_list.delete(0, tk.END)
        self.project_list_source = self.db.get_project_list(reg_exp_pattern)
        # for i in range(1, 50):
        if self.project_list_source:
            for row in self.project_list_source:
                self.project_list.insert(tk.END, row[1])

    def on_search_pressed(self) -> None:
        pass

    def on_new_pressed(self) -> None:
        pass

    def on_edit_pressed(self) -> None:
        pass

    def on_delete_pressed(self) -> None:
        pass

    def on_item_selected(self, evt: tk.Event) -> None:
        """ copy the selected list item's details into the detail panel """
        sel = self.project_list.curselection()
        if sel and self.project_list_source:
            ix = sel[0]
            row = self.project_list_source[ix]
            self.panel_detail.push_data_row(row)
        else:
            self.panel_detail.clear_data()

    def _init_db(self) -> None:
        # self.db = DataSource()  # in __init__
        self.db.create_database()  # does nothing if it already exists
        # db.create_schema()
        # create_database will create schema and load sample data
        # db.open_database()
        # db.load_sample_data()
        # $db.close_database()

    # syntax check:
    #   flake8 --enable-extensions True --statistics myapp.py
    # static rules check
    #   mypy --string myapp.py
    