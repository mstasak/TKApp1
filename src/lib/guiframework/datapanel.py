# import sqlite3
# import re
# from os.path import exists, isfile, join
# from pathlib import Path
# from platformdirs import user_data_dir
from typing import Any, List, Optional, Tuple
# from datetime import datetime
import tkinter as tk
from tkinter import ttk

class DataPanelRow:
    def __init__(self, parent, label, control_class_, control_args, *args, **kwargs):
        self.nickname = ""
        self.label_text = ""
        self.control_type = ""
        self.initial_value = ""
        self.bindings = None

class DataPanel:
    """ Build a frame with labels and data entry controls in a grid """

    def __init__(self):
        self.panel = ttk.LabelFrame()
        self.data_panel_rows = List[DataPanelRow]()
        self.build_data_panel()

    def pull_data_row(self) -> Tuple[Any]:
        pass

    def push_data_row(self, row: Tuple[Any]) -> None:
        pass

    def build_data_panel(self):
        self.add_label("Edit Project Details:")

    def add_label(self, label_text):
        pass

    def add_entry(self):
        pass

    def add_entry_multiline(self):
        pass

    def add_entry_number(self):
        pass

    def add_checkbox(self):
        pass

    def add_combobox(self):
        pass

    def add_radio(self):
        pass

    # skip entry variants like ssn, email, phone, etc; might consider some kind of mask and/or RE validation some day

