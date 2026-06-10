from flask import abort, render_template, request, session

from app import create_app, db
from app.models.facilities import Facilities
from app.models.owner import Owner
from app.models.ratings import Ratings
from app.models.role import Role
from app.models.user import User
from app.models.engagement import Favorite, RatingComment, RatingLike
from app.services.facilities_service import FacilityService

app = create_app()
facility_service = FacilityService()


def initialize_database():
    db.create_all()
    for role_name in ("user", "owner", "admin"):
        if not Role.query.filter_by(name=role_name).first():
            db.session.add(Role(name=role_name))
    db.session.commit()


@app.route("/", methods=["GET"])
def home():
    search_query = request.args.get("search")
    filters = {
        "type": request.args.get("type"),
        "category": request.args.get("category"),
        "rating": request.args.get("rating"),
    }
    filters = {k: v for k, v in filters.items() if v}

    facilities = []
    message = None

    if search_query:
        facility = facility_service.searching_by_name(search_query)
        if facility:
            facilities = [facility]
        else:
            message = "Facility not found"
    elif filters:
        facilities = facility_service.get_filtered_facilities(filters)
        if not facilities:
            message = "No facilities match the selected filters."
    else:
        facilities = facility_service.get_suggestion_facilities()

    favorite_ids = set()
    if session.get("role") == "user" and session.get("id"):
        favorite_ids = {
            x.facility_id
            for x in Favorite.query.filter_by(user_id=session["id"]).all()
        }

    return render_template(
        "html/home.html",
        facilities=facilities,
        message=message,
        favorite_ids=favorite_ids,
    )


@app.route("/facility/<string:facility_name>")
def facility_details(facility_name):
    result = facility_service.get_facility_details(facility_name)
    if not result["success"]:
        abort(404, description=result["message"])

    is_favorite = False
    liked_rating_ids = set()
    if session.get("role") == "user" and session.get("id"):
        is_favorite = (
            Favorite.query.filter_by(
                user_id=session["id"],
                facility_id=result["facility"].id,
            ).first()
            is not None
        )
        liked_rating_ids = {
            row.rating_id
            for row in RatingLike.query.filter_by(user_id=session["id"]).all()
        }

    return render_template(
        "html/facility_details.html",
        facility=result["facility"],
        ratings=result.get("ratings", []),
        summary=result.get("summary", {}),
        is_favorite=is_favorite,
        liked_rating_ids=liked_rating_ids,
    )

@app.route("/about")
def about():
    return render_template("html/about.html")


if __name__ == "__main__":
    with app.app_context():
        initialize_database()
    app.run(debug=True)
