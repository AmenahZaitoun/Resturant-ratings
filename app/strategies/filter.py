from abc import ABC , abstractmethod


class Filter_Strategy(ABC):
    @abstractmethod
    def apply(self, query):
        pass
