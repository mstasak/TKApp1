import sqlite3
import re
from os.path import exists, isfile, join
from pathlib import Path
from platformdirs import user_data_dir
from typing import Any  # , List, Optional, Tuple
from datetime import datetime

from dataaccess.sqlite.idatasource import IDataSource


#from dataclasses import dataclass

#from dataaccess.sqlite import ProjectRow
#from dataaccess.sqlite.projectadapter import ProjectAdapter


# TODO: DocStrings, make a singleton (pick an approach), perhaps implement a
#  service provider to access the singleton


class DataSource(IDataSource):

    # Credit for regexp use from SQLite/python:
    # https://gist.github.com/eestrada/fd55398950c6ee1f1deb

    @staticmethod
    def adapt_date_iso(val: datetime) -> str:
        """Adapt datetime.date to ISO 8601 date."""
        return val.isoformat()

    @staticmethod
    def convert_datetime(val: bytes) -> datetime:
        """Convert ISO 8601 datetime to datetime.datetime object."""
        return datetime.fromisoformat(val.decode())

    @staticmethod
    def regexp(y: str, x: str, search=re.search) -> int:
        return 1 if search(y, x) else 0

    # _shared: DataSource = DataSource()
    #
    # @staticmethod
    # def shared() -> DataSource:
    #     return _shared

    def __init__(self) -> None:
        # """ if nest_opens is true, Datasource will count opens and closes and
        # keep connection open until count reaches zero. """
        # self.nest_opens : bool = True
        # self.open_count : int = 0
        #self.ProjectEntity = ProjectAdapter()
        super().__init__()
        sqlite3.register_adapter(datetime, DataSource.adapt_date_iso)
        sqlite3.register_converter("datetime",
                                   DataSource.convert_datetime)

    @staticmethod
    def _db_filepath() -> str:
        """ Get full path to database file """
        app_data_dir = user_data_dir(appname="TKAPP1", appauthor="mjstasak",
                                     version="0.001", roaming=False,
                                     ensure_exists=True)
        return join(app_data_dir, "tkapp1.db")

    @staticmethod
    def _db_file_exists() -> bool:
        """ Test if database file is present """
        _fpath = DataSource._db_filepath()
        return exists(_fpath) and isfile(_fpath)

    def create_database(self) -> bool:
        """ Create the SQLite database file (by trying to open non-existing
         file) """
        # consider: , skip_if_exists:bool = True, create_schema:bool = True,
        # add_sample_data = True
        if self.db is not None:
            return True  # connection was open therefore it exists
        if DataSource._db_file_exists():
            return True  # file present therefore it exists
        db_path = DataSource._db_filepath()
        self.db = sqlite3.connect(db_path, autocommit=False)
        # above will create db if file not found
        if self.db is None:
            return False  # create and open failed
        else:
            #self.create_schema()
            #self.load_sample_data()
            self.close_database()
            return True

    def drop_database(self) -> bool:
        """ Drop the database by closing and deleting its SQLite file """
        if self.db is not None:
            self.close_database()
        db_path = DataSource._db_filepath()
        path = Path(db_path)
        path.unlink(missing_ok=True)
        return True

    def open_database(self) -> bool:
        """ Open connection to the SQLite database file """
        if not DataSource._db_file_exists():
            self.create_database()
        db_path = DataSource._db_filepath()
        self.db = sqlite3.connect(db_path,
                                  autocommit=False,
                                  detect_types=sqlite3.PARSE_DECLTYPES)
        # will create db file if file not found
        self.db.row_factory = sqlite3.Row
        self.db.create_function('regexp', 2, DataSource.regexp)

        return self.db is not None

    def close_database(self) -> bool:
        """ Close the connection 'db' to the SQLite database file """
        if self.db is not None:
            self.db.close()
            self.db = None
        return True

    def query_scalar(self, query: str,
                     params: dict[str, Any] | None = None) -> Any:
        """ Fetch first value from first row returned by query, parameters """
        if params is None:
            params = {}
        result: Any = None
        was_open: bool = self.db is not None
        if not was_open:
            self.open_database()
        if self.db is None:
            return result
        cursor = self.db.execute(query, params)
        row1: tuple[Any, ...] = cursor.fetchone()
        result = row1[0]
        cursor.close()
        if not was_open:
            self.close_database()
        return result

    type RowFactoryType = Any  #((sqlite3.Cursor, sqlite3.Row) -> object) | None # object

    def query_row[RowType](self, query: str,
                           row_factory: RowFactoryType = None,
                           params: dict[str, Any] | None = None
                           ) -> RowType | None:
        """ Fetch first row returned by query, parameters as anonymous tuple """
        if params is None:
            params = {}
        result: RowType | None = None
        was_open: bool = self.db is not None
        if not was_open:
            self.open_database()
        if self.db is None:
            return result
        cursor: sqlite3.Cursor = self.db.execute(query, params)
        if row_factory:
            cursor.row_factory = row_factory
        result = cursor.fetchone()
        cursor.close()
        if not was_open:
            self.close_database()
        return result

    def query_multi_row[RowType](self, query: str,
                                 row_factory: RowFactoryType,
                                 params: dict[str, Any] | None = None
                                 ) -> list[RowType]:
        """ Fetch all rows returned by query, parameters as list of dataclass
         subclass objects"""

        if params is None:
            params = {}
        result: list[RowType] = []
        was_open: bool = self.db is not None
        if not was_open:
            self.open_database()
        if self.db is None:
            return result
        cursor: sqlite3.Cursor = self.db.execute(query, params)
        if row_factory:
            cursor.row_factory = row_factory
        result = cursor.fetchall()
        cursor.close()
        if not was_open:
            self.close_database()
        return result

    def execute(self, query: str,
                params: dict[str, Any] | None = None) -> bool:
        """ Execute a no result set query with optional parameters, returning
         True if successful """
        self.lastrowid = None
        if params is None:
            params = {}
        result: bool = False
        was_open: bool = self.db is not None
        if not was_open:
            self.open_database()
        if self.db is None:
            return result
        cursor = self.db.execute(query, params)
        self.lastrowid = cursor.lastrowid
        result = True
        self.db.commit()
        if not was_open:
            self.close_database()
        return result

