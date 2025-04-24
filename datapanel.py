import tkinter
from datetime import datetime
from typing import cast  # , Any, List, Optional, Tuple
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter.constants import END

from dataaccess.sqlite.projectrow import ProjectRow


# from tkinter import Label  # , IntVar, StringVar
# import sqlite3
# import re
# from tkinter import ttk


def nvl(s: str | None, none_substitute: str) -> str:
    """
    Return a string s unless s is None; if None, return a substitute value.
    Similar to the C# null-coalescing operator (s ?? "default value")
    :param s: an optional string
    :param none_substitute: the alternative value to return if s is None
    :return: Original s value, or none_substitute if s is None
    """
    return s if s else none_substitute

def nvl_str(a: any, none_substitute: str) -> str:
    """
    Return a string str(s) unless s is None; if None, return a substitute value.
    Similar to the C# null-coalescing operator (s ?? "default value")
    :param a: an optional value
    :param none_substitute: the alternative value to return if s is None
    :return: Str() representation of riginal a value, or none_substitute if s
    is None
    """
    return str(a) if a else none_substitute

def date_string(d: datetime | None) -> str:
    if d:
        return d.strftime("%m/%d/%Y %H:%M:%S %p %Z")
    else:
        return ""

def iso_date_string(d: datetime | None) -> str:
    if d:
        return d.isoformat()
    else:
        return ""

class DataPanel(tk.Frame):
    """Build a frame with labels and data entry controls in a grid"""

    def __init__(self, parent: tk.Misc | None) -> None:
        super().__init__(parent)
        self.data_variables: dict[str, tkinter.Variable] = {
            "Id": tkinter.IntVar(),
            "Name": tkinter.StringVar(),
            "Description": tkinter.StringVar(),
            "Created": tkinter.StringVar(),  # readable format
            "Updated": tkinter.StringVar(),
            "RAW_Created": tkinter.StringVar(),  # iso format
            "RAW_Updated": tkinter.StringVar(),
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
        self.add_entry(grid_row=200, label_text="ID:",
                       var=cast(tk.StringVar, self.data_variables["Id"]),
                       ctl_name="txtID", readonly=True)
        self.add_entry(grid_row=210, label_text="Name:",
                       var=cast(tk.StringVar, self.data_variables["Name"]),
                       ctl_name="txtName")
        self.add_text(grid_row=220, label_text="Description:",
                      var=cast(tk.StringVar,
                               self.data_variables["Description"]),
                      ctl_name="txtDescription")
        self.add_entry(grid_row=230, label_text="Created:",
                       var=cast(tk.StringVar, self.data_variables["Created"]),
                       ctl_name="txtCreated", readonly=True)
        self.add_entry(grid_row=240, label_text="Updated:",
                       var=cast(tk.StringVar, self.data_variables["Updated"]),
                       ctl_name="txtUpdated", readonly=True)

    def pull_data_row(self) -> ProjectRow:
        # probable to do - move this to a per-view viewmodel class so this
        # class can be model and view agnostic (a viewmodel-level concern)
        ctl_description = (cast(ScrolledText, self.controls["txtDescription"]))
        description = ctl_description.get("1.0", END)
        self.data_variables["Description"].set(description)
        result: ProjectRow = ProjectRow(
            id = int(cast(tk.StringVar, self.data_variables["Id"]).get()),
            name = cast(tk.StringVar, self.data_variables["Name"]).get(),
            description = description,
            created = datetime.fromisoformat(cast(tk.StringVar, self.data_variables["RAW_Created"]).get()),
            updated = datetime.fromisoformat(cast(tk.StringVar, self.data_variables["RAW_Updated"]).get())
        )
        return result

    def clear_data(self) -> None:
        """
        Erase values from UI controls, used when no project list item is
        selected (perhaps after a project deletion?)
        """
        self.push_data_row(ProjectRow())

    def push_data_row(self, row: ProjectRow) -> None:
        """Copy the data values in row to the UI-bound self.data_variables, and
        also save a set of original values for dirty row testing when saving.

        :param row: A row DataClass, suitable for editing and saving.
        """
        self.data_variables["Id"].set(nvl_str(row.id, ""))
        self.data_variables["Name"].set(row.name)
        self.data_variables["Description"].set(nvl(row.description, ""))
        txt_description = cast(ScrolledText, self.controls["txtDescription"])
        txt_description.replace("1.0", END, nvl(row.description, ""))
        self.data_variables["Created"].set(date_string(row.created))
        self.data_variables["Updated"].set(date_string(row.updated))
        self.data_variables_original = self.data_variables.copy()
        self.data_variables_original["RAW_Created"].set(iso_date_string(row.created))
        self.data_variables_original["RAW_Updated"].set(iso_date_string(row.updated))

    # def add_label(self, row: int, label_text: str):
    #     lbl: Label = tk.Label(master=self, text=label_text)
    #     lbl.grid(row=row, column=10, columnspan=2, sticky='nsew')
    #     self.controls["_label_panel_"] = lbl

    def add_entry(self, grid_row: int, label_text: str, var: tk.StringVar,
                  ctl_name: str, readonly: bool = False) -> None:
        """Add and populate a Label and an Entry control to the DataPanel

        :param grid_row: the grid row for the label
        :param label_text: the name of the entry field (caption)
        :param var: the Tk variable containing the Entry value
        :param ctl_name: name for this control pair; typ. the dbrow column name
        :param readonly: True to disable editing the Entry
        """
        lbl = tk.Label(master=self, text=label_text, anchor='w', justify="left")
        lbl.grid(row=grid_row, column=10, columnspan=11, sticky='nsew')
        self.controls[F"_label_{ctl_name}_"] = lbl
        entry = tk.Entry(master=self, textvariable=var)
        if readonly:
            entry.config(state='readonly')
        entry.grid(row=grid_row + 1, column=20, columnspan=1, sticky='nsew')
        self.controls[ctl_name] = entry

    def add_text(self, grid_row: int, label_text: str, var: tk.StringVar,
                 ctl_name: str, readonly: bool = False) -> None:
        """Add and populate a Label and a ScrolledText control to the DataPanel

        :param grid_row: the grid row for the label
        :param label_text: the name of the ScrolledText field (caption)
        :param var: the Tk variable containing the ScrolledText value
        :param ctl_name: name for this control pair; typ. the dbrow column name
        :param readonly: True to disable editing the ScrolledText
        """
        lbl = tk.Label(master=self, text=label_text, anchor='w', justify="left")
        lbl.grid(row=grid_row, column=10, columnspan=11, sticky='nsew', )
        self.controls[F"_label_{ctl_name}_"] = lbl
        txt = ScrolledText(master=self, bg='white', width=40, height=10)
        txt.insert(END, var.get())
        if readonly:
            txt.config(state='disabled')
        txt.grid(row=grid_row + 1, column=20, columnspan=1, sticky='nsew')
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
