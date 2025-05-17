from flask import Blueprint, render_template, request, redirect, session, url_for
from app.db import db
import traceback

admin_auth_controller = Blueprint('auth_controller', __name__)
admins_collection = db["admins"]

@admin_auth_controller.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "")
            
            print(f"Login attempt for email: {email}")
            
            admin = admins_collection.find_one({"email": email})
            if admin and admin["password"] == password:
                session.clear()
                session["admin_id"] = str(admin["admin_ID"])
                session.permanent = True
                print(f"Login successful for email: {email}")
                return redirect(url_for("admin_dashboard_controller.show_dashboard"))
            
            print(f"Invalid credentials for email: {email}")
            return render_template("login.html", error="Invalid credentials")
        except Exception as e:
            print(f"Login error: {str(e)}")
            print("Traceback:", traceback.format_exc())
            return render_template("login.html", error="An error occurred during login")
    return render_template("login.html")

@admin_auth_controller.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth_controller.login"))