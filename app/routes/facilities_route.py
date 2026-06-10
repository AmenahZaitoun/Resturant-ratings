import os
import uuid

from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for
from werkzeug.utils import secure_filename

from app.forms.add_facility_form import FacilityForm
from app.models.facility_info import FacilityInfo
from app import db
from app.services.facilities_service import FacilityService

owner_facility_routes = Blueprint("owner_facility_routes", __name__)
facility_service = FacilityService()

ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp", "avif"}


def _save_uploaded_image(image_file):
    if not image_file or not image_file.filename:
        return None

    filename = secure_filename(image_file.filename)
    _, ext = os.path.splitext(filename)
    ext = ext.lower().lstrip(".")
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        return None

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)
    saved_name = f"{uuid.uuid4().hex}.{ext}"
    image_file.save(os.path.join(upload_folder, saved_name))
    return f"uploads/facilities/{saved_name}"


@owner_facility_routes.route("/owner/home")
def owner_home():
    owner = session.get("owner")
    if not owner:
        return redirect(url_for("auth_routes.login_form"))

    facilities = facility_service.get_facilities_by_owner_username(owner.get("username"))
    return render_template("html/owner_home.html", facilities=facilities)


@owner_facility_routes.route("/owner/facility/add", methods=["GET"])
def add_facility_form():
    return render_template("html/facility_add.html", form=FacilityForm())


@owner_facility_routes.route("/owner/facility/add", methods=["POST"])
def add_facility():
    owner = session.get("owner")
    if not owner:
        return redirect(url_for("auth_routes.login_form"))

    form = FacilityForm()
    if not form.validate_on_submit():
        return render_template("html/facility_add.html", form=form)

    image_path = _save_uploaded_image(form.image.data)
    if not image_path:
        flash("Please upload a valid image file.", "danger")
        return render_template("html/facility_add.html", form=form)

    data = {
        "owner_id": owner["id"],
        "facility_name": form.facility_name.data,
        "facility_type": form.facility_type.data,
        "facility_category": form.facility_category.data,
        "image": image_path,
    }
    result = facility_service.add_facility(data, user=owner)
    if result["success"]:
        facility = result["facility"]
        info = FacilityInfo(
            facility_id=facility.id,
            address=(form.address.data or "").strip() or None,
            phone=(form.phone.data or "").strip() or None,
            opening_hours=(form.opening_hours.data or "").strip() or None,
            price_range=(form.price_range.data or "").strip() or None,
            website=(form.website.data or "").strip() or None,
            menu_items=(form.menu_items.data or "").strip() or None,
        )
        db.session.add(info)
        db.session.commit()
        flash("Facility added successfully!", "success")
        return redirect(url_for("owner_facility_routes.owner_home"))

    flash(f"Error: {result.get('message', 'Unknown error')}", "danger")
    return render_template("html/facility_add.html", form=form)


@owner_facility_routes.route("/owner/facility/edit/<string:facility_name>", methods=["GET"])
def edit_facility_form(facility_name):
    facility = facility_service.repo.get(facility_name)
    if not facility:
        flash("Facility not found.", "warning")
        return redirect(url_for("owner_facility_routes.owner_home"))
    return render_template("html/facility_edit.html", facility=facility, info=facility.info)


@owner_facility_routes.route("/owner/facility/edit/<string:facility_name>", methods=["POST"])
def edit_facility(facility_name):
    owner = session.get("owner")
    if not owner:
        return redirect(url_for("auth_routes.login_form"))

    data = request.form.to_dict()
    image_file = request.files.get("image")
    if image_file and image_file.filename:
        image_path = _save_uploaded_image(image_file)
        if not image_path:
            flash("Please upload a valid image file.", "danger")
            return redirect(url_for("owner_facility_routes.edit_facility_form", facility_name=facility_name))
        data["image"] = image_path

    result = facility_service.update_facility_by_owner(
        facility_name, owner_id=owner["id"], user=owner, **data
    )
    if result["success"]:
        updated_facility = result["facility"]
        info = updated_facility.info or FacilityInfo(facility_id=updated_facility.id)
        info.address = (data.get("address") or "").strip() or None
        info.phone = (data.get("phone") or "").strip() or None
        info.opening_hours = (data.get("opening_hours") or "").strip() or None
        info.price_range = (data.get("price_range") or "").strip() or None
        info.website = (data.get("website") or "").strip() or None
        info.menu_items = (data.get("menu_items") or "").strip() or None
        db.session.add(info)
        db.session.commit()
        flash("Facility updated successfully!", "success")
        return redirect(url_for("owner_facility_routes.owner_home"))

    flash(result.get("message", "Unable to update facility"), "danger")
    return redirect(url_for("owner_facility_routes.edit_facility_form", facility_name=facility_name))


@owner_facility_routes.route("/owner/facility/delete/<string:facility_name>", methods=["POST"])
def delete_facility(facility_name):
    owner = session.get("owner")
    if not owner:
        return redirect(url_for("auth_routes.login_form"))

    result = facility_service.delete_facility_by_owner(
        facility_name, owner_id=owner["id"], user=owner
    )
    if result["success"]:
        flash("Facility deleted successfully!", "success")
        return redirect(url_for("owner_facility_routes.owner_home"))

    flash(result.get("message", "Unable to delete facility"), "danger")
    return redirect(url_for("owner_facility_routes.owner_home"))
