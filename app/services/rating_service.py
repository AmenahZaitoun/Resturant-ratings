from flask import session
from app.repositories.rating_repository import RatingsRepository
from app.repositories.facility_repository import FacilityRepository
from app.models.ratings import Ratings
from app.models.user import User
from app import db
from app.States.context import UserContext

class RatingService:
    def __init__(self):
        self.rating_repo = RatingsRepository()
        self.facility_repo = FacilityRepository()

    def rate_facility(self, facility_name, service_quality, food_quality, mood, comment):
        # ✅ استخراج id من الجلسة
        user_id = session.get("id")
        if not user_id:
            return {"success": False, "message": "User not logged in."}

        # ✅ جلب المستخدم من قاعدة البيانات
        user = User.query.get(user_id)
        if not user:
            return {"success": False, "message": "User not found."}

        # ✅ التحقق من الصلاحيات
        context = UserContext(user)
        if not context.can_add_rating():
            return {"success": False, "message": "You can't add a rating unless you're signed in."}

        # 🔍 البحث عن المنشأة بالاسم
        facility = self.facility_repo.get(facility_name)
        if not facility:
            return {"success": False, "message": f"Facility '{facility_name}' not found."}

        facility_name = facility_name

        # ✅ حساب متوسط تقييم المستخدم
        user_avg = round((service_quality + food_quality + mood) / 3, 2)

        # 📝 إنشاء تقييم جديد
    # 📝 إنشاء تقييم جديد
        new_rating = Ratings(
            user_id=user.id,
            facility_id=facility.id,  # ✅ هذا هو التعديل المهم
            service_quality=service_quality,
            food_quality=food_quality,
            mood=mood,
            comment=comment
        )   

        db.session.add(new_rating)
        db.session.commit()

        # 📊 جلب كل التقييمات
        all_ratings = self.rating_repo.get(facility_name)
        if all_ratings:
            total_avg = round(
                sum(new_rating.service_quality + new_rating.food_quality + new_rating.mood for r in all_ratings) / (3 * len(all_ratings)), 2
            )
        else:
            total_avg = user_avg

        # ✅ تحديث تقييم المنشأة
        self.facility_repo.update(facility_name, rating=total_avg)

        return {"success": True, "new_avg": total_avg}
