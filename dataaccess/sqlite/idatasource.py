import sqlite3
from abc import ABCMeta, abstractmethod


class IDataSource(metaclass=ABCMeta):
    def __init__(self):
        self.db: sqlite3.Connection | None = None
        self.lastrowid : int | None = None

    @abstractmethod
    def create_database(self):
        """ Create the SQLite database file (by trying to open non-existing
        file) """
        pass

    @abstractmethod
    def drop_database(self):
        """ Drop the database by closing and deleting its SQLite file """
        pass

    @abstractmethod
    def open_database(self):
        """ Open connection to the SQLite database file """
        pass

    @abstractmethod
    def close_database(self):
        """ Close the connection 'db' to the SQLite database file """
        pass

    @abstractmethod
    def query_scalar(self, query, params):
        """ Fetch first value from first row returned by query, parameters """
        pass

    @abstractmethod
    def query_row(self, query, row_factory, params):
        """ Fetch first row returned by query, parameters as anonymous tuple """
        pass

    @abstractmethod
    def query_multi_row(self, query, row_factory, params):
        """ Fetch all rows returned by query, parameters as list of dataclass
        subclass objects"""
        pass

    @abstractmethod
    def execute(self, query, params):
        """ Execute a no result set query with optional parameters, returning
        True if successful """
        pass

    @property
    def is_open(self) -> bool:
        return self.db is not None