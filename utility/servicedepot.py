from datasource.sqlite import DataSource


class ServiceDepot:

    _db_service: DataSource | None = None

    def __init__(self) -> None:
        pass

    @classmethod
    def db_service(cls) -> DataSource:
        # create singleton only once
        if cls._db_service is None:
            cls._db_service = DataSource()
        return cls._db_service

    # TODO: log_service, maybe validation, testing, sample data population,
    # spell check, data classes?

    # syntax check:
    #   flake8 --enable-extensions True --statistics utility/servicedepot.py
