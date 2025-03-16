import sqlite3
from os.path import exists, isfile, join
from pathlib import Path
import platformdirs
import typing

class DataSource:


    def __init__(self) -> None:
        #""" if nest_opens is true, Datasource will count opens and closes and keep connection open
        #    until close reaches zero. """
        #self.nest_opens : bool = True
        #self.open_count : int = 0
        self.db : sqlite3.Connection | None = None

    @staticmethod
    def _db_filepath() -> str:
        app_data_dir = platformdirs.user_data_dir(appname="TKAPP1", appauthor="mjstasak", version="0.001", roaming=False, ensure_exists=True)
        return join(app_data_dir, "tkapp1.db")
    
    @staticmethod
    def _db_file_exists() -> bool:
        _fpath = DataSource._db_filepath()
        return exists(_fpath) and isfile(_fpath)

    def create_database(self) -> bool:
        # consider: , skip_if_exists:bool = True, create_schema:bool = True, add_sample_data = True
        if self.db != None:
            return True  # connection was open therefore it exists
        if DataSource._db_file_exists():
            return True  # file present therefore it exists
        db_path = DataSource._db_filepath()
        #print(db_path)
        #raise RuntimeError(db_path)
        self.db = sqlite3.connect(db_path, autocommit=False)  # will create if file not found
        if (self.db == None):
            return False  # create and open failed
        else:
            self.create_schema()
            self.load_sample_data()
            self.close_database()
            return True

    def drop_database(self) -> bool:
        if (self.db != None):
            self.close_database()
        db_path = DataSource._db_filepath()
        path = Path(db_path)
        path.unlink(missing_ok=True)
        return True

    def open_database(self) -> bool:
        if not DataSource._db_file_exists():
            self.create_database()
        db_path = DataSource._db_filepath()
        self.db = sqlite3.connect(db_path, autocommit=False)  # will create if file not found
        return self.db != None

    def close_database(self) -> bool:
        if self.db != None:
            self.db.close()
            self.db = None
        return True

    def create_schema(self) -> bool:
        was_open = self.db != None
        if not was_open:
            self.open_database()

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
        
        # NOTE: This would likely fail if trying to drop tables referenced by foreign keys

        was_open = self.db != None
        if not was_open:
            self.open_database()
        
        self.execute("DROP TABLE project")

        if not was_open:
            self.close_database()
        
        return True

    def load_sample_data(self) -> bool:
        raise NotImplementedError()

    def truncate_data(self) -> bool:
        raise NotImplementedError()

    def query_scalar(self, query:str, params:typing.Optional[dict[str, object]] = None) -> typing.Any:
        raise NotImplementedError()

    def query_row(self, query:str, params:typing.Optional[dict[str, object]] = None) -> typing.Any:
        raise NotImplementedError()

    def query_multi_row(self, query:str, params:typing.Optional[dict[str, object]] = None) -> typing.Any:
        raise NotImplementedError()

    def execute(self, query:str, params:typing.Optional[dict[str, object]] = None) -> bool:
        if self.db == None:
            return False
        self.db.execute(query, params)
        self.db.commit()
        return True
