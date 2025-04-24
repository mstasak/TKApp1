from datetime import datetime
from dataclasses import dataclass

@dataclass()
class ProjectRow:
    """hold a row from the project table"""
    id: int | None = None
    name: str = ""
    description: str | None = None
    created: datetime | None = None
    updated: datetime | None = None
