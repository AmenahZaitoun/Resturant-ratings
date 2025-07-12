from app.States.state import State 

class OwnerState(State):
    def can_view_facility(self):
        return True

    def can_add_rating(self):
        return False  

    def can_manage_facilities(self):
        return True
