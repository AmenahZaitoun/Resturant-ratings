from app.strategies.filter import Filter_Strategy
from app.models.facilities import Facilities


class CategoryFilter(Filter_Strategy):
    def __init__(self, selected_category):
        self.selected_category = selected_category

    def apply(self, query):
        return query.filter(Facilities.facility_category == self.selected_category)