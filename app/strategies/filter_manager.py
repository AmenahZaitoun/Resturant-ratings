# app/strategies/filter_manager.py

class FilterManager:
    def __init__(self):
        self.strategies = []

    def add_filter(self, strategy):
        self.strategies.append(strategy)

    def apply_filters(self, base_query):
        for strategy in self.strategies:
            base_query = strategy.apply(base_query)
        return base_query
