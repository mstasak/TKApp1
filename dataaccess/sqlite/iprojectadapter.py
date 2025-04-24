from abc import ABCMeta, abstractmethod


class IProjectAdapter(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def new_row():
        pass

    @abstractmethod
    def load_row(self, id_):
        pass

    @abstractmethod
    def save_row(self, row):
        pass

    @staticmethod
    @abstractmethod
    def dataclass_factory(cursor, row):
        pass

    @abstractmethod
    def get_project_list(self, reg_exp_pattern):
        pass

    @abstractmethod
    def create_schema(self):
        """ Create the database schema (tables, constraints, relationships,
        etc.) """
        pass

    @abstractmethod
    def load_sample_data(self):
        """ Install some sample data for development/testing """
        pass

    @abstractmethod
    def drop_schema(self):
        """ drop all objects from the database schema """
        pass

    @abstractmethod
    def data_present(self):
        """ check if at least one row is present in the project table """
        pass

    @abstractmethod
    def truncate_data(self):
        """ Remove all data from table(s) """
        pass