from flask import Blueprint, render_template, redirect, session
from app.services.facilities_service import FacilityService

owner_routes = Blueprint("owner_routes", __name__)
facility_service = FacilityService()

@owner_routes.route("/owner/home")
def owner_home():
    owner = session.get("user")
    if not owner or owner.get("role") != "owner":
        return redirect("/login")

    owner_id = owner.get("id")
    facilities = facility_service.repo.get_by_owner(owner_id)

    return render_template("html/owner_home.html", facilities=facilities)
