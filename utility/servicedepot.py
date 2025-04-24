from dataaccess.sqlite.iprojectadapter import IProjectAdapter
from dataaccess.sqlite.idatasource import IDataSource
from utility.iservicedepot import IServiceDepot


class ServiceDepot(IServiceDepot):

    def __init__(self) -> None:
        super().__init__()
        #self._db_service: DataSource | None = None
        #self._project_service: ProjectAdapter | None = None

    def db_service(self) -> IDataSource:
        # create singleton only once
        from dataaccess.sqlite.datasource import DataSource
        if self._db_service is None:
            self._db_service = DataSource()
        return self._db_service

    # TODO: log_service, maybe validation, testing, sample data population,
    # spell check, data classes?

    def project_service(self) -> IProjectAdapter:
        # create singleton only once
        from dataaccess.sqlite.projectadapter import ProjectAdapter
        if self._project_service is None:
            self._project_service = ProjectAdapter()
        return self._project_service

    # syntax check:
    #   flake8 --enable-extensions True --statistics utility/servicedepot.py
