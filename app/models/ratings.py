from app import db

class Ratings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    facility_id = db.Column(db.Integer, db.ForeignKey("facilities.id"), nullable=False)
    service_quality = db.Column(db.Float, nullable=False)
    food_quality = db.Column(db.Float, nullable=False)
    mood = db.Column(db.Float, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    user = db.relationship("User", back_populates="user_ratings")
    def __repr__(self):
        return f"<Rating {self.id} - Facility ID: {self.facility_id}>"

    
    
    