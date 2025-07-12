from flask import abort, render_template, session, redirect, url_for 
from app import create_app, db
from app.services.facilities_service import FacilityService
from flask import Blueprint, render_template, request, abort
from flask import render_template, request
from app import create_app, db
from app.services.facilities_service import FacilityService
from flask import session, redirect, url_for 

app = create_app()
facility_service = FacilityService()
@app.route("/", methods=["GET"])
def home():
    search_query = request.args.get("search")
    filters = {
        "type": request.args.get("type"),
        "category": request.args.get("category"),
        "rating": request.args.get("rating")
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

    return render_template("html/home.html", facilities=facilities, message=message)

 # أضف هذا في الأعلى إن لم يكن موجودًا

@app.route("/facility/<string:facility_name>")
def facility_details(facility_name):
    result = facility_service.get_facility_details(facility_name)
    if not result["success"]:
        abort(404, description=result["message"])

    # ✅ إزالة التحويل التلقائي للمستخدم
    facility = result["facility"]
    ratings = result.get("ratings", [])
    return render_template("html/facility_details.html", facility=facility, ratings=ratings)


# تشغيل التطبيق
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)