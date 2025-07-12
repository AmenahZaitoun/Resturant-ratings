from app.States.guest_state import GuestState
from app.States.user_state import UserState
from app.States.owner_state import OwnerState

class UserContext:
    def __init__(self, user=None):
        self.user = user
        self.state = self._determine_state()

    def _determine_state(self):
        if not self.user:
            return GuestState()

        # نحصل على role إن وجد
        role = getattr(self.user, "role", None)

        if role is None:
            return GuestState()

        role_name = getattr(role, "name", None)

        if not role_name:
            return GuestState()

        role_name = role_name.lower()

        if role_name == "owner":
            return OwnerState()
        elif role_name == "user":
            return UserState()
        else:
            return GuestState()

    def can_view_facility(self):
        return self.state.can_view_facility()

    def can_add_rating(self):
        return self.state.can_add_rating()

    def can_manage_facilities(self):
        return self.state.can_manage_facilities()
