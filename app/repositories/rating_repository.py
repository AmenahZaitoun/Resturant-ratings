from app.repositories.base_repository import Repository
from app.models.ratings import Ratings
from app import db


class RatingsRepository(Repository):

    def create(self, rating):
        db.session.add(rating)
        db.session.commit()
        return rating

    def update(self, rating):
        db.session.commit()
        return rating

    def get(self, facility_id):
        return Ratings.query.filter_by(facility_id=facility_id).all()

    def get_all(self):
        return Ratings.query.all()
    
    def delete(self, rating_id):
        rating = self.get(rating_id)
        if rating:
            db.session.delete(rating)
            db.session.commit()