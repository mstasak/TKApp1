import tkinter
from typing import Any, List, cast  # , Optional, Tuple
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter.constants import END

# from tkinter import Label  # , IntVar, StringVar
# import sqlite3
# import re
# from tkinter import ttk


class DataPanel(tk.Frame):
    """Build a frame with labels and data entry controls in a grid"""

    def __init__(self, parent: tk.Misc | None) -> None:
        super().__init__(parent)
        self.data_variables: dict[str, tkinter.Variable] = {
            "Id": tkinter.IntVar(),
            "Name": tkinter.StringVar(),
            "Description": tkinter.StringVar(),
            "Created": tkinter.StringVar(),
            "Updated": tkinter.StringVar(),
        }
        self.data_variables_original: dict[str, tkinter.Variable] = {}
        self.controls: dict[str, tk.Widget] = {}
        self._build_data_panel()

    def _build_data_panel(self) -> None:
        self.columnconfigure(10, weight=30, minsize='10')
        self.columnconfigure(20, weight=70, minsize='50')
        # self.rowconfigure(100, weight=1)
        self.rowconfigure(200, weight=2)
        self.rowconfigure(201, weight=3)
        self.rowconfigure(210, weight=2)
        self.rowconfigure(211, weight=3)
        self.rowconfigure(220, weight=2)
        self.rowconfigure(221, weight=10, minsize=250)
        self.rowconfigure(230, weight=2)
        self.rowconfigure(231, weight=3)
        self.rowconfigure(240, weight=2)
        self.rowconfigure(241, weight=3)
        # self.add_label(row=100, label_text="Edit Project Details:")
        self.add_entry(row=200, label_text="ID:",
                       var=cast(tk.StringVar, self.data_variables["Id"]),
                       ctl_name="txtID", readonly=True)
        self.add_entry(row=210, label_text="Name:",
                       var=cast(tk.StringVar, self.data_variables["Name"]),
                       ctl_name="txtName")
        self.add_text(row=220, label_text="Description:",
                      var=cast(tk.StringVar,
                               self.data_variables["Description"]),
                      ctl_name="txtDescription")
        self.add_entry(row=230, label_text="Created:",
                       var=cast(tk.StringVar, self.data_variables["Created"]),
                       ctl_name="txtCreated", readonly=True)
        self.add_entry(row=240, label_text="Updated:",
                       var=cast(tk.StringVar, self.data_variables["Updated"]),
                       ctl_name="txtUpdated", readonly=True)

    def pull_data_row(self) -> dict[str, Any]:
        # probable to do - move this to a per-view viewmodel class so this
        # class can be model and view agnostic (a viewmodel-level concern)
        ctl_description = (cast(ScrolledText, self.controls["txtDescription"]))
        description = ctl_description.get("1.0", END)
        self.data_variables["Description"].set(description)
        result: dict[str, str] = {
            "id": cast(tk.StringVar, self.data_variables["Id"]).get(),
            "name": cast(tk.StringVar, self.data_variables["Name"]).get(),
            "description": description,
            "created": cast(tk.StringVar, self.data_variables["Created"]).get(),
            "updated": cast(tk.StringVar, self.data_variables["Updated"]).get()}
        return result

    def clear_data(self) -> None:
        self.push_data_row(["", "", "", "", ""])

    def push_data_row(self, row: List[Any]) -> None:
        # row[n] positions match column order in SQLite table Projects
        self.data_variables["Id"].set(row[0])
        self.data_variables["Name"].set(row[1])
        self.data_variables["Description"].set(row[2])
        txt_description = cast(ScrolledText, self.controls["txtDescription"])
        txt_description.replace("1.0", END, row[2])
        self.data_variables["Created"].set(row[3])
        self.data_variables["Updated"].set(row[4])
        self.data_variables_original = self.data_variables.copy()

    # def add_label(self, row: int, label_text: str):
    #     lbl: Label = tk.Label(master=self, text=label_text)
    #     lbl.grid(row=row, column=10, columnspan=2, sticky='nsew')
    #     self.controls["_label_panel_"] = lbl

    def add_entry(self, row: int, label_text: str, var: tk.StringVar,
                  ctl_name: str, readonly: bool = False) -> None:
        lbl = tk.Label(master=self, text=label_text)
        lbl.grid(row=row, column=10, columnspan=2, sticky='nsew')
        self.controls[F"_label_{ctl_name}_"] = lbl
        entry = tk.Entry(master=self, textvariable=var)
        if readonly:
            entry.config(state='readonly')
        entry.grid(row=row + 1, column=20, columnspan=1, sticky='nsew')
        self.controls[ctl_name] = entry

    def add_text(self, row: int, label_text: str, var: tk.StringVar,
                 ctl_name: str, readonly: bool = False) -> None:
        lbl = tk.Label(master=self, text=label_text)
        lbl.grid(row=row, column=10, columnspan=2, sticky='nsew')
        self.controls[F"_label_{ctl_name}_"] = lbl
        txt = ScrolledText(master=self, bg='white', width=40, height=10)
        txt.insert(END, var.get())
        if readonly:
            txt.config(state='disabled')
        txt.grid(row=row + 1, column=20, columnspan=1, sticky='nsew')
        self.controls[ctl_name] = txt

    # def add_entry_number(self):
    #     pass
    #
    # def add_checkbox(self):
    #     pass
    #
    # def add_combobox(self):
    #     pass
    #
    # def add_radio(self):
    #     pass

    # skip entry variants like password, ssn, email, phone, etc.; might
    # consider some kind of mask and/or RegExp validation some day

    # syntax check:
    #   flake8 --enable-extensions True --statistics datapanel.py
