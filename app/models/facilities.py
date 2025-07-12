from app import db


class Facilities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("owner.id"), nullable=False)
    facility_name = db.Column(db.String(100), nullable=False)
    facility_type = db.Column(db.String(50), nullable=False)
    facility_category = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(20), nullable=False, default="default_icon.jpg")
    rating = db.Column(db.Float)
    ratings = db.relationship("Ratings", backref="facility", lazy=True)
    
    def __repr__(self):
        return f"<Facility {self.facility_name} - Type: {self.facility_type}>"
