from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.services.rating_service import RatingService
from app.forms.ratings import RatingForm
from app.models.ratings import Ratings
from app.models.engagement import RatingLike, RatingComment
from app import db

ratings_routes = Blueprint("ratings_routes", __name__)
rating_service = RatingService()

# ✅ تحقق من أن المستخدم المسجل لديه صلاحية "user"
def login_required_user(func):
    def wrapper(*args, **kwargs):
        user = session.get("user")
        if not user or user.get("role") != "user":
            flash("You must be logged in as a user to rate facilities.", "warning")
            return redirect(url_for("auth_routes.login_form"))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

# ✅ عرض نموذج التقييم
@ratings_routes.route("/rate/<facility_name>", methods=["GET"])
@login_required_user
def show_rating_form(facility_name):
    form = RatingForm()
    return render_template("html/rate_facility.html", form=form, facility_name=facility_name)

# ✅ إرسال التقييم
@ratings_routes.route("/rate/<facility_name>", methods=["POST"])
@login_required_user
def submit_rating(facility_name):
    form = RatingForm(request.form)

    if not form.validate():
        flash("Please fill in all required fields correctly.", "danger")
        return redirect(url_for("ratings_routes.show_rating_form", facility_name=facility_name))

    try:
        service_quality = int(form.service_quality.data)
        food_quality = int(form.food_quality.data)
        mood = int(form.mood.data)
    except ValueError:
        flash("Invalid rating values. Please enter valid numbers.", "danger")
        return redirect(url_for("ratings_routes.show_rating_form", facility_name=facility_name))

    comment = form.comment.data or ""

    # ✅ استدعاء الخدمة
    result = rating_service.rate_facility(
        facility_name=facility_name,
        service_quality=service_quality,
        food_quality=food_quality,
        mood=mood,
        comment=comment
    )

    if result.get("success"):
        flash("Your rating has been submitted successfully!", "success")
        return redirect(url_for("facility_details", facility_name=facility_name))

    flash(result.get("message", "Failed to submit your rating."), "danger")
    return redirect(url_for("ratings_routes.show_rating_form", facility_name=facility_name))


@ratings_routes.route("/rating/<int:rating_id>/like", methods=["POST"])
@login_required_user
def toggle_rating_like(rating_id):
    rating = db.session.get(Ratings, rating_id)
    facility_name = request.form.get("facility_name")
    if not rating:
        flash("Rating not found.", "danger")
        return redirect(url_for("home"))

    if not facility_name:
        facility_name = rating.facility.facility_name if rating.facility else None

    user_id = session.get("id")
    existing = RatingLike.query.filter_by(user_id=user_id, rating_id=rating_id).first()
    if existing:
        db.session.delete(existing)
        flash("Like removed.", "info")
    else:
        db.session.add(RatingLike(user_id=user_id, rating_id=rating_id))
        flash("Thanks for your like.", "success")
    db.session.commit()

    if facility_name:
        return redirect(url_for("facility_details", facility_name=facility_name))
    return redirect(url_for("home"))


@ratings_routes.route("/rating/<int:rating_id>/comment", methods=["POST"])
@login_required_user
def add_rating_comment(rating_id):
    rating = db.session.get(Ratings, rating_id)
    facility_name = request.form.get("facility_name")
    text = (request.form.get("comment_text") or "").strip()
    if not rating:
        flash("Rating not found.", "danger")
        return redirect(url_for("home"))

    if not facility_name:
        facility_name = rating.facility.facility_name if rating.facility else None

    if not text:
        flash("Comment cannot be empty.", "warning")
        if facility_name:
            return redirect(url_for("facility_details", facility_name=facility_name))
        return redirect(url_for("home"))

    db.session.add(
        RatingComment(
            user_id=session.get("id"),
            rating_id=rating_id,
            comment=text[:500],
        )
    )
    db.session.commit()
    flash("Comment added.", "success")
    if facility_name:
        return redirect(url_for("facility_details", facility_name=facility_name))
    return redirect(url_for("home"))
