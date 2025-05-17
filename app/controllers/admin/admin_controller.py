from flask import Blueprint, render_template, request, redirect, url_for, session
from app.db import db
import uuid

admin_controller = Blueprint('admin_controller', __name__)
admins_collection = db["admins"]

def generate_id(prefix):
    return prefix + str(uuid.uuid4())[:8]

def is_logged_in():
    return "admin_id" in session

@admin_controller.route("/admins")
def list_admins():
    if not is_logged_in():
        return redirect(url_for("auth_controller.login"))
    try:
        admins = list(admins_collection.find({}, {"password": 0}))
        return render_template("admins.html", admins=admins)
    except Exception as e:
        print(f"Admin list error: {e}")
        return redirect(url_for("dashboard_controller.show_dashboard"))

@admin_controller.route("/admins/add", methods=["POST"])
def add_admin():
    if not is_logged_in():
        return redirect(url_for("auth_controller.login"))
    try:
        new_admin = {
            "admin_ID": generate_id("ADM"),
            "email": request.form.get("email", "").strip(),
            "password": request.form.get("password", "")  # no hashing
        }
        admins_collection.insert_one(new_admin)
        return redirect(url_for("admin_controller.list_admins"))
    except Exception as e:
        print(f"Add admin error: {e}")
        return redirect(url_for("admin_controller.list_admins"))

@admin_controller.route("/admins/<admin_id>/delete")
def delete_admin(admin_id):
    if not is_logged_in():
        return redirect(url_for("auth_controller.login"))
    if str(session.get("admin_id")) == admin_id:
        return redirect(url_for("admin_controller.list_admins", error="Cannot delete current admin"))
    try:
        admins_collection.delete_one({"admin_ID": admin_id})
        return redirect(url_for("admin_controller.list_admins"))
    except Exception as e:
        print(f"Delete admin error: {e}")
        return redirect(url_for("admin_controller.list_admins"))

@admin_controller.route("/admins/<admin_id>/edit", methods=["GET", "POST"])
def edit_admin(admin_id):
    if not is_logged_in():
        return redirect(url_for("auth_controller.login"))
    try:
        admin = admins_collection.find_one({"admin_ID": admin_id})
        if not admin:
            return redirect(url_for("admin_controller.list_admins"))
        if request.method == "POST":
            update_data = {"email": request.form.get("email", "").strip()}
            if request.form.get("password"):
                update_data["password"] = request.form.get("password")
            admins_collection.update_one(
                {"admin_ID": admin_id},
                {"$set": update_data}
            )
            return redirect(url_for("admin_controller.list_admins"))
        return render_template("edit_admin.html", admin=admin)
    except Exception as e:
        print(f"Edit admin error: {e}")
        return redirect(url_for("admin_controller.list_admins"))