# from mymainpage import MyMainPage
import tkinter as tk
from tkinter import ttk, Tk, Listbox, StringVar
from tkinter.ttk import Label, Scrollbar, Frame, Entry, Button
from typing import cast  # Any, List, Optional, Tuple, cast
# from typing_extensions import override
import globals
from datapanel import DataPanel
from dataaccess.sqlite.projectrow import ProjectRow


class MyApp(tk.Frame):
    """App subclass, with customizations for this application"""

    def __init__(self) -> None:
        super().__init__(padx=10, pady=10, background="Navy Blue")
        # self.app_name: str = "TKApp1"
        # self._default_position = [0, 0]
        # self._default_size = [1024, 768]
        # self.main_page: AppPageBase | None = MyMainPage(self)
        self.is_editing: bool = False

        # services
        from dataaccess.sqlite.idatasource import IDataSource
        self.db: IDataSource = globals.service_depot.db_service()
        from dataaccess.sqlite.iprojectadapter import IProjectAdapter
        self.projects: IProjectAdapter = globals.service_depot.project_service()

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

        self.project_list_source: list[ProjectRow] | None = None

        clear_panel_style: ttk.Style = ttk.Style()
        clear_panel_style.configure("clear.TFrame", foreground="clear",
                                    background="clear")
        self.panel_search: Frame = Frame(master=self, style='clear.TFrame')
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
        self.project_list: Listbox = Listbox(self, bg='aliceblue', fg='black',
                                             bd='2',
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
        self.button_save = Button(self.panel_buttons, text="Save",
                                  command=self.on_save_pressed)
        self.button_cancel = Button(self.panel_buttons, text="Cancel",
                                    command=self.on_cancel_pressed)

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
        self.project_list_source: list[ProjectRow] | None = \
            self.projects.get_project_list(reg_exp_pattern)
        # for i in range(1, 50):
        if self.project_list_source:
            for row in self.project_list_source:
                self.project_list.insert(tk.END, row.name)

    def on_search_pressed(self) -> None:
        self.configure_mode(editing=False)

    def on_new_pressed(self) -> None:
        row = self.projects.new_row()
        self.panel_detail.push_data_row(row)
        self.configure_mode(editing=True)

    def on_edit_pressed(self) -> None:
        self.configure_mode(not self.is_editing)  # (True)

    def on_delete_pressed(self) -> None:
        pass

    def on_save_pressed(self) -> None:
        is_new = False
        row = self.panel_detail.pull_data_row()
        new_id = self.projects.save_row(row)  # int if new row created
        if new_id is not None:
            is_new = True
            assert(row.id is None, "Incorrectly inserted an existing project row")
            row.id = new_id

        if is_new:
            self.project_list_source.append(row)
            new_ix = len(self.project_list.children) - 1
            self.project_list.selection_set(new_ix, new_ix)
        else:
            sel: list[int] | None = self.project_list.curselection()
            if sel and self.project_list_source:
                ix = sel[0]
                old_row = self.project_list_source[ix]
                assert(old_row.id == row.id, "Incorrectly inserted an existing project row")
                self.panel_detail.push_data_row(row)
            else:
                old_ix = -1
                for ky, item in self.project_list.children:
                    if item.id == row.id:
                        old_ix = ky
                        break
                if old_ix >= 0:
                    self.project_list.children[old_ix] = row
                self.panel_detail.clear_data()

        self.configure_mode(False)
        self.on_item_selected()

    def on_cancel_pressed(self) -> None:
        self.configure_mode(False)
        self.on_item_selected()

    def on_item_selected(self, _: tk.Event | None = None) -> None:
        """ copy the selected list item's details into the detail panel """
        sel: list[int] | None = self.project_list.curselection()
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
    def configure_mode(self, editing: bool | None = None) -> bool:
        if editing is not None:
            if self.is_editing != editing:
                if editing:
                    # set up editing mode: change button bar to Save, Cancel
                    # and disable and dim selection list and search
                    self.button_delete.pack_forget()
                    self.button_new.pack_forget()
                    self.button_edit.pack_forget()
                    #self.button_save.pack_forget()
                    #self.button_cancel.pack_forget()
                    #self.button_delete.pack(side='left', expand=True, pady=10)
                    #self.button_new.pack(side='left', expand=True, pady=10)
                    #self.button_edit.pack(side='left', expand=True, pady=10)
                    self.button_save.pack(side='left', expand=True, pady=10)
                    self.button_cancel.pack(side='left', expand=True, pady=10)
                else:
                    # set up non-editing (selection) mode:
                    # change button bar to New, Edit, Delete
                    # and disable and dim edit panel
                    #self.button_delete.pack_forget()
                    #self.button_new.pack_forget()
                    #self.button_edit.pack_forget()
                    self.button_save.pack_forget()
                    self.button_cancel.pack_forget()
                    self.button_delete.pack(side='left', expand=True, pady=10)
                    self.button_new.pack(side='left', expand=True, pady=10)
                    self.button_edit.pack(side='left', expand=True, pady=10)
                    #self.button_save.pack(side='left', expand=True, pady=10)
                    #self.button_cancel.pack(side='left', expand=True, pady=10)
                self.is_editing = editing
        return self.is_editing
