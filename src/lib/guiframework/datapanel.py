# import sqlite3
# import re
# from os.path import exists, isfile, join
# from pathlib import Path
# from platformdirs import user_data_dir
import tkinter
from typing import Any, List, Optional, Tuple, cast
# from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter.constants import INSERT, END

# class DataPanelRow:
#     def __init__(self, parent, label, control_class_, control_args, *args, **kwargs):
#         self.nickname = ""
#         self.label_text = ""
#         self.control_type = ""
#         self.initial_value = ""
#         self.bindings = None

class DataPanel:
    """ Build a frame with labels and data entry controls in a grid """

    def __init__(self, parent):
        self.panel = ttk.LabelFrame(parent)
        # self.data_panel_rows: List[DataPanelRow]() = List[DataPanelRow]()
        self.data_variables: dict[str, tkinter.Variable] = {}
        self.data_variables_original: dict[str, tkinter.Variable] = {}
        self.controls: dict[str, tk.Widget] = {}
        self._build_data_source()
        self._build_data_panel()
        self.row_gen = 10

    def _build_data_source(self) -> None:
        # probable to do - move this to a per-table model class so this class needn't know the model in any way
        # (model-level concern)
        self.data_variables.clear()
        self.data_variables["Id"] = tkinter.IntVar()
        self.data_variables["Name"] = tkinter.StringVar()
        self.data_variables["Description"] = tkinter.StringVar()
        self.data_variables["Created"] = tkinter.StringVar()
        self.data_variables["Updated"] = tkinter.StringVar()

    def _build_data_panel(self) -> None:
        self.panel.columnconfigure(10, weight=30, minsize='10')
        self.panel.columnconfigure(20, weight=70, minsize='50')
        self.panel.rowconfigure(10, weight=1)
        self.panel.rowconfigure(100, weight=2)
        self.panel.rowconfigure(110, weight=3)
        self.panel.rowconfigure(120, weight=2)
        self.panel.rowconfigure(130, weight=3)
        self.panel.rowconfigure(140, weight=2)
        self.panel.rowconfigure(150, weight=10, minsize=250)
        self.panel.rowconfigure(160, weight=2)
        self.panel.rowconfigure(170, weight=3)
        self.panel.rowconfigure(180, weight=2)
        self.panel.rowconfigure(190, weight=3)
        self.row_gen = 10
        self.add_label(label_text="Edit Project Details:")
        self.row_gen = 100
        self.add_entry(label_text="ID:", var=cast(tk.StringVar, self.data_variables["Id"]), ctl_name="txtID", readonly=True)
        self.add_entry(label_text="Name:", var=cast(tk.StringVar, self.data_variables["Name"]), ctl_name="txtName")
        self.add_text(label_text="Description:", var=cast(tk.StringVar, self.data_variables["Name"]), ctl_name="txtDescription")
        self.add_entry(label_text="Created:", var=cast(tk.StringVar, self.data_variables["Created"]), ctl_name="txtCreated", readonly=True)
        self.add_entry(label_text="Updated:", var=cast(tk.StringVar, self.data_variables["Updated"]), ctl_name="txtUpdated", readonly=True)

    def pull_data_row(self) -> List[Any]:
        # probable to do - move this to a per-view viewmodel class so this class can be model and view agnostic
        # (viewmodel-level concern)
        result = List[Any]()
        result += self.data_variables["Id"].get()
        return result

    def clear_data(self):
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
        #self.data_variables["Name"].set("testinging")
        x = self.data_variables["Name"].get()
        print(F"x = {row}\n")

    def add_label(self, label_text: str):
        lbl = tk.Label(master=self.panel, text=label_text)
        lbl.grid(column=10, columnspan=2, row=self.row_gen, sticky='nsew')
        self.row_gen += 10
        self.controls["_label_panel_"] = lbl

    def add_entry(self, label_text: str, var: tk.StringVar, ctl_name: str, readonly: bool = False):
        lbl = tk.Label(master=self.panel, text=label_text)
        lbl.grid(column=10, columnspan=2, row=self.row_gen, sticky='nsew')
        self.row_gen += 10
        self.controls[F"_label_{ctl_name}_"] = lbl
        entry=tk.Entry(master=self.panel, textvariable=var)
        if readonly:
            entry.config(state='readonly')
        entry.grid(column=20, columnspan=1, row=self.row_gen, sticky='nsew')
        self.row_gen += 10
        self.controls[ctl_name] = entry

    def add_text(self, label_text: str, var: tk.StringVar, ctl_name: str, readonly: bool = False):
        lbl = tk.Label(master=self.panel, text=label_text)
        lbl.grid(column=10, columnspan=2, row=self.row_gen, sticky='nsew')
        self.row_gen += 10
        self.controls[F"_label_{ctl_name}_"] = lbl
        txt = ScrolledText(master=self.panel, bg='white', width=40, height=10)
        from tkinter.constants import END
        txt.insert(END, var.get())
        if readonly:
            txt.config(state='readonly')
        txt.grid(column=20, columnspan=1, row=self.row_gen, sticky='nsew')

        self.row_gen += 10
        self.controls[ctl_name] = txt

    def add_entry_number(self):
        pass

    def add_checkbox(self):
        pass

    def add_combobox(self):
        pass

    def add_radio(self):
        pass

    # skip entry variants like password, ssn, email, phone, etc; might consider some kind of mask and/or RE validation some day

    # # Python program demonstrating
    # # ScrolledText widget in tkinter
    #
    # import tkinter as tk
    # from tkinter import ttk
    # from tkinter import scrolledtext
    #
    # # Creating tkinter main window
    # win = tk.Tk()
    # win.title("ScrolledText Widget")
    #
    # # Title Label
    # ttk.Label(win,
    #         text = "ScrolledText Widget Example",
    #         font = ("Times New Roman", 15),
    #         background = 'green',
    #         foreground = "white").grid(column = 0,
    #                                     row = 0)
    #
    # # Creating scrolled text
    # # area widget
    # text_area = scrolledtext.ScrolledText(win,
    #                                     wrap = tk.WORD,
    #                                     width = 40,
    #                                     height = 10,
    #                                     font = ("Times New Roman",
    #                                             15))
    #
    # text_area.grid(column = 0, pady = 10, padx = 10)
    #
    # # Placing cursor in the text area
    # text_area.focus()
    # win.mainloop()
