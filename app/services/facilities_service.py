# app/services/facilities_service.py

from app.repositories.facility_repository import FacilityRepository
from app.repositories.rating_repository import RatingsRepository
from app.strategies.filter_manager import FilterManager
from app.strategies.rating_filter import RatingFilter
from app.strategies.category_filter import CategoryFilter
from app.strategies.type_filter import TypeFilter
from app.States.context import UserContext

class FacilityService:
    def __init__(self):
        self.repo = FacilityRepository()
        self.ratings_repo = RatingsRepository()
        self.filter_manager = FilterManager()

    def get_suggestion_facilities(self):
        return self.repo.get_all_defult()

    def get_filtered_facilities(self, filters):
        filter_manager = FilterManager()

        if 'type' in filters:
            filter_manager.add_filter(TypeFilter(filters['type']))
        if 'category' in filters:
            filter_manager.add_filter(CategoryFilter(filters['category']))
        if 'rating' in filters:
            filter_manager.add_filter(RatingFilter(float(filters['rating'])))

        query = self.repo.get_all()
        filtered_query = filter_manager.apply_filters(query)
        return filtered_query.all()

    def searching_by_name(self, facility_name):
        return self.repo.get(facility_name=facility_name)

    def get_facility_details(self, facility_name):
        facility = self.repo.get(facility_name)
        if not facility:
            return {"success": False, "message": "Facility not found"}

        ratings = self.ratings_repo.get(facility_id=facility.id)
        ratings_data = [{
            "user_name": r.user.username if r.user else "Unknown",
            "service_quality": r.service_quality,
            "food_quality": r.food_quality,
            "mood": r.mood,
            "comment": r.comment
        } for r in ratings]

        return {
            "success": True,
            "facility": facility,
            "ratings": ratings_data
        }

    def get_facilities_by_owner_username(self, username):
        return self.repo.get_by_owner_username(username)

    def add_facility(self, facility_data, owner):
        context = UserContext(owner)
        if not context.can_manage_facilities():
            return {"success": False, "message": "Unauthorized"}

        created = self.repo.create(facility_data)
        return {"success": True, "facility": created}

    def update_facility_by_owner(self, facility_name, owner_id, owner, **kwargs):
        context = UserContext(owner)
        if not context.can_manage_facilities():
            return {"success": False, "message": "Unauthorized"}

        facility = self.repo.get(facility_name)
        if not facility:
            return {"success": False, "message": "Facility not found"}

        kwargs.pop("rating", None)
        updated = self.repo.update(facility_name, **kwargs)
        return {"success": True, "facility": updated}

    def delete_facility_by_owner(self, facility_name, owner_id, user):
        context = UserContext(user)
        if not context.can_manage_facilities():
            return {"success": False, "message": "Unauthorized"}

        facility = self.repo.get(facility_name)
        if not facility:
            return {"success": False, "message": "Facility not found"}

        self.repo.delete(facility_name)
        return {"success": True, "message": "Facility deleted successfully"}
