from abc import ABCMeta, abstractmethod
from dataaccess.sqlite.iprojectadapter import IProjectAdapter
from dataaccess.sqlite.idatasource import IDataSource


class IServiceDepot(metaclass=ABCMeta):
    def __init__(self) -> None:
        self._db_service: IDataSource | None = None
        self._project_service: IProjectAdapter | None = None

    @abstractmethod
    def db_service(self) -> IDataSource:
        pass

    @abstractmethod
    def project_service(self) -> IProjectAdapter:
        pass
