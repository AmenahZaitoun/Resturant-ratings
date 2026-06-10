from datetime import datetime

from app import db


class Favorite(db.Model):
    __tablename__ = "favorite"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    facility_id = db.Column(db.Integer, db.ForeignKey("facilities.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        db.UniqueConstraint("user_id", "facility_id", name="uq_user_facility_favorite"),
    )


class RatingLike(db.Model):
    __tablename__ = "rating_like"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    rating_id = db.Column(db.Integer, db.ForeignKey("ratings.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user = db.relationship("User", lazy=True)
    rating = db.relationship("Ratings", lazy=True)

    __table_args__ = (
        db.UniqueConstraint("user_id", "rating_id", name="uq_user_rating_like"),
    )


class RatingComment(db.Model):
    __tablename__ = "rating_comment"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    rating_id = db.Column(db.Integer, db.ForeignKey("ratings.id"), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user = db.relationship("User", lazy=True)
    rating = db.relationship("Ratings", lazy=True)
