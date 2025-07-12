from app.strategies.filter import Filter_Strategy
from app.models.facilities import Facilities

class TypeFilter(Filter_Strategy):
    def __init__(self, selected_type):
        self.selected_type = selected_type

    def apply(self, query):
        return query.filter(Facilities.facility_type == self.selected_type)