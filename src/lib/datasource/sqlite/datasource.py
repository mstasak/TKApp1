import sqlite3
import re
from os.path import exists, isfile, join
from pathlib import Path
from platformdirs import user_data_dir
from typing import Any, List, Optional, Tuple
from datetime import datetime

# TODO: DocStrings, make a singleton (pick an approach), perhaps implement a service provider to access the singleton

class DataSource:

    # Credit for regexp use from SQLite/python: https://gist.github.com/eestrada/fd55398950c6ee1f1deb

    @staticmethod
    def adapt_date_iso(val: datetime) -> str:
        """Adapt datetime.date to ISO 8601 date."""
        return val.isoformat()

    @staticmethod
    def convert_datetime(val: bytes) -> datetime:
        """Convert ISO 8601 datetime to datetime.datetime object."""
        return datetime.fromisoformat(val.decode())

    @staticmethod
    def regexp(y, x, search=re.search):
        return 1 if search(y, x) else 0

    # _shared: DataSource = DataSource()
    #
    # @staticmethod
    # def shared() -> DataSource:
    #     return _shared

    def __init__(self) -> None:
        #""" if nest_opens is true, Datasource will count opens and closes and keep connection open
        #    until close reaches zero. """
        #self.nest_opens : bool = True
        #self.open_count : int = 0
        self.db : sqlite3.Connection | None = None
        sqlite3.register_adapter(datetime, DataSource.adapt_date_iso)
        sqlite3.register_converter("datetime", DataSource.convert_datetime)

    @staticmethod
    def _db_filepath() -> str:
        """ Get full path to database file """
        app_data_dir = user_data_dir(appname="TKAPP1", appauthor="mjstasak",
                                     version="0.001", roaming=False, ensure_exists=True)
        return join(app_data_dir, "tkapp1.db")
    
    @staticmethod
    def _db_file_exists() -> bool:
        """ Test if database file is present """
        _fpath = DataSource._db_filepath()
        return exists(_fpath) and isfile(_fpath)

    def create_database(self) -> bool:
        """ Create the SQLite database file (by trying to open non-existing file) """
        # consider: , skip_if_exists:bool = True, create_schema:bool = True, add_sample_data = True
        if self.db is not None:
            return True  # connection was open therefore it exists
        if DataSource._db_file_exists():
            return True  # file present therefore it exists
        db_path = DataSource._db_filepath()
        self.db = sqlite3.connect(db_path, autocommit=False)  # will create if file not found
        if self.db is None:
            return False  # create and open failed
        else:
            self.create_schema()
            self.load_sample_data()
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
        self.db = sqlite3.connect(db_path, autocommit=False)  # will create if file not found
        self.db.create_function('regexp', 2, DataSource.regexp)

        return self.db is not None

    def close_database(self) -> bool:
        """ Close the connection 'db' to the SQLite database file """
        if self.db is not None:
            self.db.close()
            self.db = None
        return True

    def create_schema(self) -> bool:
        """ Create the database schema (tables, constraints, relationships, etc.) """
        was_open = self.db is not None
        if not was_open:
            self.open_database()
        # TODO: detect if schema already exists and leave alone
        # alternatively, use 'CREATE IF NOT EXISTS'-type DDL statements
        self.execute(
            """
            CREATE TABLE project (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name VARCHAR NOT NULL,
              description VARCHAR,
              created DATETIME,
              updated DATETIME,
              CONSTRAINT u_project_name UNIQUE(name)
            )
            """
        )
        if not was_open:
            self.close_database()
        return True

    def drop_schema(self) -> bool:
        """ drop all objects from the database schema """
        # NOTE: This might fail if trying to drop tables with rows referenced by foreign keys
        was_open = self.db is not None
        if not was_open:
            self.open_database()
        self.execute("DROP TABLE project")
        if not was_open:
            self.close_database()
        return True
    
    def data_present(self) -> bool:
        """ check if at least one row is present in the project table """
        count: int = self.query_scalar("select count(*) from project")
        return count > 0

    def load_sample_data(self) -> bool:
        """ Install some sample data for development/testing """
        if self.data_present():
            return True
        was_open = self.db is not None
        if not was_open:
            self.open_database()
        
        dt_now = datetime.now()
        self.execute("""INSERT INTO project (name,description,created,updated)
                     values ('Work on TKAPP1','Learn Python and make app useful.',:now,:now)""",
                     {"now": dt_now})

        dt_now = datetime.now()
        self.execute("""INSERT INTO project (name,description,created,updated)
                     values ('Clean kitchen','Dishes AND floor, oh NO!.',:now,:now)""",
                     {"now": dt_now})

        dt_now = datetime.now()
        self.execute("""INSERT INTO project (name,description,created,updated)
                     values ('NCAA Tournament','Watch UF crush opponents (hopefully).',:now,:now)""",
                     {"now": dt_now})

        if not was_open:
            self.close_database()
        return True

    def truncate_data(self) -> bool:
        """ Remove all data from table(s) """
        # NOTE: remember to delete child table rows before parent table rows
        was_open = self.db is not None
        if not was_open:
            self.open_database()
        self.execute("DELETE FROM project")
        if not was_open:
            self.close_database()
        return True


    def query_scalar(self, query:str, params: Optional[dict[str, Any]] = None) -> Any:
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

    def query_row(self, query:str, params: Optional[dict[str, Any]] = None) -> Optional[Tuple[Any, ...]]:
        """ Fetch first row returned by query, parameters as anonymous tuple """
        if params is None:
            params = {}
        result: Optional[Tuple[Any, ...]] = None
        was_open: bool = self.db is not None
        if not was_open:
            self.open_database()
        if self.db is None:
            return result
        cursor: sqlite3.Cursor = self.db.execute(query, params)
        result = cursor.fetchone()
        cursor.close()
        if not was_open:
            self.close_database()
        return result

    def query_multi_row(self, query:str, params: Optional[dict[str, Any]] = None) -> List[Tuple[Any, ...]]:
        """ Fetch all rows returned by query, parameters as list of anonymous tuples """
        if params is None:
            params = {}
        result: List[Tuple[Any, ...]] = [ ]
        was_open: bool = self.db is not None
        if not was_open:
            self.open_database()
        if self.db is None:
            return result
        cursor: sqlite3.Cursor = self.db.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
        if not was_open:
            self.close_database()
        return result

    def execute(self, query:str, params: Optional[dict[str, Any]] = None) -> bool:
        """ Execute a query with optional parameters, returning True if successful """
        if params is None:
            params = {}
        result: bool = False
        was_open: bool = self.db is not None
        if not was_open:
            self.open_database()
        if self.db is None:
            return result
        self.db.execute(query, params)
        result = True
        self.db.commit()
        if not was_open:
            self.close_database()
        return result

    def get_project_list(self, reg_exp_pattern: str = "") -> List[Tuple[Any, ...]] | None:
        result: List[Tuple[Any, ...]] | None = None
        was_open: bool = self.db is not None
        if not was_open:
            self.open_database()
        if self.db is None:
            return result
        #self.db.execute(query, params)
        #result = True
        #self.db.commit()
        query: str = "SELECT id, name FROM project"
        params: dict[str, Any] | None = None
        if reg_exp_pattern != "":
            #params = {':name', reg_exp_pattern}
            query += " WHERE name REGEXP '[Cc]lean'"
        query += " ORDER BY name"
        result = self.query_multi_row(query, params)
        if not was_open:
            self.close_database()
        return result
