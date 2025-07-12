from app.strategies.filter import Filter_Strategy
from app.models.facilities import Facilities


class RatingFilter(Filter_Strategy):
    def __init__(self, min_rating):
        self.min_rating = min_rating

    def apply(self, query):
        return query.filter(Facilities.rating >= self.min_rating)
