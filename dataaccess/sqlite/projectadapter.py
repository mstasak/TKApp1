# from dataaccess.sqlite.datasource import DataSource
from typing import Any  # , List, Optional, Tuple
from datetime import datetime

from dataaccess.sqlite.iprojectadapter import IProjectAdapter
# from utility.iservicedepot import IServiceDepot
from globals import service_depot
from dataaccess.sqlite.projectrow import ProjectRow


class ProjectAdapter(IProjectAdapter):
    """Service for managing the "project" table"""

    def __init__(self) -> None:
        self.db = service_depot.db_service()

    @staticmethod
    def new_row() -> ProjectRow:
        return ProjectRow()

    def load_row(self, id_: int) -> ProjectRow | None:
        was_open: bool = self.db.is_open
        if not was_open:
            self.db.open_database()
        if not self.db.is_open:
            return None
        query: str = \
            """
            SELECT id, name, description, created, updated
            FROM project
            WHERE id = :id
            """
        params: dict[str, Any] = {"id": id_}
        result: ProjectRow | None = \
            self.db.query_row(query, ProjectAdapter.dataclass_factory, params)
        if not was_open:
            self.db.close_database()
        return result

    def save_row(self, row: ProjectRow) -> int | None:
        was_open: bool = self.db.is_open
        result: int | None = None
        if not was_open:
            self.db.open_database()
        if not self.db.is_open:
            return None
        count: int | None = 0
        if row.id is not None:
            query: str = \
                """
                SELECT count(*)
                FROM project
                WHERE id = id
                """
            params: dict[str, Any] = {"id": row.id}
            count = self.db.query_scalar(query, params)
            if count is None:
                count = 0
        now: datetime = datetime.now()
        created: datetime = row.created
        if created is None or created == "":
            created = now
        if count > 0:
            # update existing row
            query = \
                """UPDATE project
                      SET name=:name, 
                          description=:description,
                          created=:created,
                          updated=:updated
                    WHERE id=:id"""
            params = {
                "id": row.id,
                "name": row.name,
                "description": row.description,
                "created": created,
                "updated": now,
            }
            self.db.execute(query, params)
        else:
            # insert new row
            created = now
            query = \
                """INSERT INTO project (name, description, created, updated)
                    VALUES (:name, :description, :created, :updated)"""
            params = {
                "name": row.name,
                "description": row.description,
                "created": created,
                "updated": now,
            }
            self.db.execute(query, params)

            result = self.db.lastrowid
            row.id = result
        if not was_open:
            self.db.close_database()
        row.created = created
        row.updated = now
        return result

    @staticmethod
    def dataclass_factory(cursor, row):
        fields = [column[0] for column in cursor.description]
        return ProjectRow(**{k: v for k, v in zip(fields, row)})

    def get_project_list(self, reg_exp_pattern: str = ""
                         ) -> list[ProjectRow] | None:
        was_open: bool = self.db.is_open
        if not was_open:
            self.db.open_database()
        if not self.db.is_open:
            return None
        query: str = "SELECT id, name, description, created, updated FROM project"
        params: dict[str, Any] | None = None
        if reg_exp_pattern != "":
            params = {':reg_exp': reg_exp_pattern}
            query += " WHERE name REGEXP :reg_exp"
        query += " ORDER BY name"
        result: list[ProjectRow] = \
            self.db.query_multi_row(query, ProjectAdapter.dataclass_factory,
                                    params)
        if not was_open:
            self.db.close_database()
        return result

    def create_schema(self) -> bool:
        """ Create the database schema (tables, constraints, relationships,
        etc.) """
        was_open = self.db.is_open
        if not was_open:
            self.db.open_database()
        # TODO: detect if schema already exists and leave alone
        # alternatively, use 'CREATE IF NOT EXISTS'-type DDL statements
        self.db.execute(
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
            self.db.close_database()
        return True

    def load_sample_data(self) -> bool:
        """ Install some sample data for development/testing """
        if self.data_present():
            return True
        was_open = self.db.is_open
        if not was_open:
            self.db.open_database()

        dt_now = datetime.now()
        self.db.execute(
            """INSERT INTO project (name,description,created,updated)
            values ('Work on TKAPP1','Learn Python and make app useful.',
                    :now,:now)""",
            {"now": dt_now})

        dt_now = datetime.now()
        self.db.execute("""INSERT INTO project (name,description,created,updated)
                     values ('Clean kitchen','Dishes AND floor, oh NO!.',:now,:now)""",
                        {"now": dt_now})

        dt_now = datetime.now()
        self.db.execute("""INSERT INTO project (name,description,created,updated)
                     values ('NCAA Tournament','Watch UF crush opponents (hopefully).',:now,:now)""",
                        {"now": dt_now})

        if not was_open:
            self.db.close_database()
        return True

    def drop_schema(self) -> bool:
        """ drop all objects from the database schema """
        # NOTE: This might fail if trying to drop tables with rows referenced
        # by foreign keys
        was_open = self.db.is_open
        if not was_open:
            self.db.open_database()
        self.db.execute("DROP TABLE project")
        if not was_open:
            self.db.close_database()
        return True

    def data_present(self) -> bool:
        """ check if at least one row is present in the project table """
        count: int = self.db.query_scalar("select count(*) from project")
        return count > 0

    def truncate_data(self) -> bool:
        """ Remove all data from table(s) """
        # NOTE: remember to delete child table rows before parent table rows
        was_open = self.db.is_open
        if not was_open:
            self.db.open_database()
        self.db.execute("DELETE FROM project")
        if not was_open:
            self.db.close_database()
        return True
