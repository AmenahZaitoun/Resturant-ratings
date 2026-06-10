from app import db


class FacilityInfo(db.Model):
    __tablename__ = "facility_info"

    id = db.Column(db.Integer, primary_key=True)
    facility_id = db.Column(db.Integer, db.ForeignKey("facilities.id"), nullable=False, unique=True)
    address = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(40), nullable=True)
    opening_hours = db.Column(db.String(255), nullable=True)
    price_range = db.Column(db.String(50), nullable=True)
    website = db.Column(db.String(255), nullable=True)
    menu_items = db.Column(db.Text, nullable=True)

    facility = db.relationship("Facilities", back_populates="info")
