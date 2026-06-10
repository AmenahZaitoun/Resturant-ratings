# app/services/facilities_service.py

from app.repositories.facility_repository import FacilityRepository
from app.repositories.rating_repository import RatingsRepository
from app.strategies.filter_manager import FilterManager
from app.strategies.rating_filter import RatingFilter
from app.strategies.category_filter import CategoryFilter
from app.strategies.type_filter import TypeFilter
from app.States.context import UserContext
from app.models.engagement import RatingLike, RatingComment

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
        ratings = sorted(ratings, key=lambda x: x.id, reverse=True)

        review_count = len(ratings)
        service_avg = round(sum(r.service_quality for r in ratings) / review_count, 2) if review_count else 0
        food_avg = round(sum(r.food_quality for r in ratings) / review_count, 2) if review_count else 0
        mood_avg = round(sum(r.mood for r in ratings) / review_count, 2) if review_count else 0
        overall_avg = round((service_avg + food_avg + mood_avg) / 3, 2) if review_count else 0

        stars_distribution = {i: 0 for i in range(1, 6)}
        for r in ratings:
            overall = round((r.service_quality + r.food_quality + r.mood) / 3)
            overall = min(5, max(1, int(overall)))
            stars_distribution[overall] += 1

        def _percent(value):
            if review_count == 0:
                return 0
            return round((value / review_count) * 100, 1)

        ratings_data = [{
            "id": r.id,
            "user_name": r.user.username if r.user else "Unknown",
            "service_quality": r.service_quality,
            "food_quality": r.food_quality,
            "mood": r.mood,
            "overall_score": round((r.service_quality + r.food_quality + r.mood) / 3, 2),
            "comment": r.comment,
            "likes_count": RatingLike.query.filter_by(rating_id=r.id).count(),
            "comments": [
                {
                    "user_name": c.user.username if getattr(c, "user", None) else "User",
                    "comment": c.comment,
                    "created_at": c.created_at,
                }
                for c in RatingComment.query.filter_by(rating_id=r.id).order_by(RatingComment.created_at.asc()).all()
            ],
        } for r in ratings]

        return {
            "success": True,
            "facility": facility,
            "ratings": ratings_data,
            "summary": {
                "review_count": review_count,
                "overall_avg": overall_avg,
                "service_avg": service_avg,
                "food_avg": food_avg,
                "mood_avg": mood_avg,
                "stars_distribution": stars_distribution,
                "stars_distribution_percent": {k: _percent(v) for k, v in stars_distribution.items()},
            },
        }

    def get_facilities_by_owner_username(self, username):
        return self.repo.get_by_owner_username(username)

    def _can_manage_facilities(self, user):
        if not user:
            return False

        # Session payload for owner.
        if isinstance(user, dict):
            return user.get("role") == "owner"

        context = UserContext(user)
        return context.can_manage_facilities()

    def add_facility(self, facility_data, user):
        if not self._can_manage_facilities(user):
            return {"success": False, "message": "Unauthorized"}

        allowed_keys = {"owner_id", "facility_name", "facility_type", "facility_category", "image"}
        payload = {k: v for k, v in facility_data.items() if k in allowed_keys}

        required = {"owner_id", "facility_name", "facility_type", "facility_category", "image"}
        if not required.issubset(payload.keys()):
            return {"success": False, "message": "Missing required facility fields"}

        created = self.repo.create(payload)
        return {"success": True, "facility": created}

    def update_facility_by_owner(self, facility_name, owner_id, user, **kwargs):
        if not self._can_manage_facilities(user):
            return {"success": False, "message": "Unauthorized"}

        facility = self.repo.get(facility_name)
        if not facility:
            return {"success": False, "message": "Facility not found"}
        if facility.owner_id != owner_id:
            return {"success": False, "message": "You can only update your own facility"}

        kwargs.pop("rating", None)
        kwargs.pop("owner_id", None)
        kwargs.pop("csrf_token", None)
        kwargs.pop("submit", None)
        updated = self.repo.update(facility_name, **kwargs)
        return {"success": True, "facility": updated}

    def delete_facility_by_owner(self, facility_name, owner_id, user):
        if not self._can_manage_facilities(user):
            return {"success": False, "message": "Unauthorized"}

        facility = self.repo.get(facility_name)
        if not facility:
            return {"success": False, "message": "Facility not found"}
        if facility.owner_id != owner_id:
            return {"success": False, "message": "You can only delete your own facility"}

        self.repo.delete(facility_name)
        return {"success": True, "message": "Facility deleted successfully"}
