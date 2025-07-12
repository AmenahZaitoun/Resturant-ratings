from flask import flash, Blueprint, render_template, request, session, redirect, jsonify, url_for
from app.services.facilities_service import FacilityService
from app.forms.add_facility_form import FacilityForm

owner_facility_routes = Blueprint("owner_facility_routes", __name__)
facility_service = FacilityService()

# الصفحة الرئيسية للمالك - عرض منشآته
@owner_facility_routes.route("/owner/home")
def owner_home():
    owner = session.get("owner")
    if not owner:
        return redirect(url_for("auth_routes.login_form"))

    owner_name = owner.get("username") 
    facilities = facility_service.get_facilities_by_owner_username(owner_name)
    return render_template("html/owner_home.html", facilities=facilities)


# عرض فورم إضافة منشأة
@owner_facility_routes.route("/owner/facility/add", methods=["GET"])
def add_facility_form():
    form = FacilityForm()
    return render_template("html/facility_add.html", form=form)


# إرسال بيانات إضافة منشأة
@owner_facility_routes.route("/owner/facility/add", methods=["POST"])
def add_facility():
    owner = session.get("owner")
    if not owner:
        return redirect(url_for("auth_routes.login_form"))

    form = FacilityForm()
    if form.validate_on_submit():
        data = form.data
        data["owner_id"] = owner["id"]
        result = facility_service.add_facility(data, user=owner)  # ✅ تعديل هنا

        if result["success"]:
            flash("Facility added successfully!", "success")
            return redirect(url_for("owner_facility_routes.owner_home"))  # ✅ تعديل: استخدم redirect
        else:
            flash(f"Error: {result.get('message', 'Unknown error')}", "danger")

    return render_template("html/facility_add.html", form=form)


# عرض فورم التعديل لمنشأة معيّنة
@owner_facility_routes.route("/owner/facility/edit/<string:facility_name>", methods=["GET"])
def edit_facility_form(facility_name):
    facility = facility_service.repo.get(facility_name)
    return render_template("html/facility_edit.html", facility=facility)


# إرسال تعديل منشأة
@owner_facility_routes.route("/owner/facility/edit/<string:facility_name>", methods=["POST"])
def edit_facility(facility_name):
    owner = session.get("owner")
    if not owner:
        return redirect("/owner/login")

    data = request.form.to_dict()
    result = facility_service.update_facility_by_owner(
        facility_name, owner_id=owner["id"], user=owner, **data  # ✅ تعديل هنا
    )

    if result["success"]:
        return redirect("/owner/home")
    return jsonify(result), 403


# حذف منشأة
@owner_facility_routes.route("/owner/facility/delete/<string:facility_name>", methods=["POST"])
def delete_facility(facility_name):
    owner = session.get("owner")
    if not owner:
        return redirect("/owner/login")

    result = facility_service.delete_facility_by_owner(
        facility_name, owner_id=owner["id"], user=owner  # ✅ تعديل هنا
    )

    if result["success"]:
        return redirect("/owner/home")
    return jsonify(result), 403
