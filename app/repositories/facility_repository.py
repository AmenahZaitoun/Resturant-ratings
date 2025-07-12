from app.repositories.base_repository import Repository
# app/repositories/facility_repository.py
from app.models.facilities import Facilities
from app.models.owner import Owner
from app import db


class FacilityRepository(Repository):

    def create(self, facility_data):
        new_facility = Facilities(**facility_data)  # إنشاء الكائن هنا
        db.session.add(new_facility)
        db.session.commit()
        return new_facility

    def update(self, facility_name, **kwargs):
        facility = self.get(facility_name)
        if not facility:
            return None

        for key, value in kwargs.items():
            if hasattr(facility, key) and value is not None:
                setattr(facility, key, value)

        db.session.commit()
        return facility


    def get(self, facility_name):
        return Facilities.query.filter_by(facility_name=facility_name).first()

    
    def get_all(self):
        return db.session.query(Facilities)  # هذا يرجع query object

    def get_by_owner_username(self, username):
        return Facilities.query.join(Owner).filter(Owner.username == username).all()

    
    def get_by_type(self, facility_type):
        return Facilities.query.filter_by(facility_type=facility_type).all()

    def get_by_category(self, category):
        return Facilities.query.filter_by(facility_category=category).all()

    def get_by_min_rating(self, min_rating):
        return Facilities.query.filter(Facilities.rating >= min_rating).all()

    def get_by_type_and_category(self, facility_type, category):
        return Facilities.query.filter_by(facility_type=facility_type, facility_category=category).all()
    
    def get_by_owner(self, owner_id):
        return Facilities.query.filter_by(owner_id=owner_id).all()
    
    def get_all_defult(self):
         return Facilities.query.order_by(Facilities.rating.desc()).limit(10).all()    
    
    def delete(self, facility_name):
        facility = self.get(facility_name)
        if facility:
            db.session.delete(facility)
            db.session.commit()

