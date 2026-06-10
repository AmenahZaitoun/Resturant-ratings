from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app import db
from app.models.engagement import Favorite
from app.models.facilities import Facilities

favorites_routes = Blueprint("favorites_routes", __name__)


def _require_user():
    return session.get("role") == "user" and session.get("id")


@favorites_routes.route("/favorites")
def favorites_page():
    if not _require_user():
        flash("Please login as a user first.", "warning")
        return redirect(url_for("auth_routes.login_form"))

    rows = (
        db.session.query(Facilities)
        .join(Favorite, Favorite.facility_id == Facilities.id)
        .filter(Favorite.user_id == session["id"])
        .all()
    )
    return render_template("html/favorites.html", facilities=rows)


@favorites_routes.route("/favorites/toggle/<string:facility_name>", methods=["POST"])
def toggle_favorite(facility_name):
    if not _require_user():
        flash("Please login as a user first.", "warning")
        return redirect(url_for("auth_routes.login_form"))

    facility = Facilities.query.filter_by(facility_name=facility_name).first()
    if not facility:
        flash("Facility not found.", "danger")
        return redirect(url_for("home"))

    existing = Favorite.query.filter_by(user_id=session["id"], facility_id=facility.id).first()
    if existing:
        db.session.delete(existing)
        flash("Removed from favorites.", "info")
    else:
        db.session.add(Favorite(user_id=session["id"], facility_id=facility.id))
        flash("Added to favorites.", "success")
    db.session.commit()

    return redirect(request.referrer or url_for("home"))
