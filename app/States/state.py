from abc import ABC, abstractmethod


class State(ABC):
    @abstractmethod
    def can_view_facility(self):
        pass

    @abstractmethod
    def can_add_rating(self):
        pass

    @abstractmethod
    def can_manage_facilities(self):
        pass