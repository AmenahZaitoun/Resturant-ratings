from abc import ABC , abstractmethod

class Repository(ABC):
    @abstractmethod
    def create(self, entity):
        pass
    @abstractmethod
    def update(self, entity):
        pass
    @abstractmethod
    def get(self, entity_name):
        pass
    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def delete(self, entity_name):
        pass
        