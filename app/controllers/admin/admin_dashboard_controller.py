from flask import Blueprint, render_template, redirect, url_for, session
from app.db import db
import traceback

admin_dashboard_controller = Blueprint('admin_dashboard_controller', __name__)

def is_logged_in():
    return "admin_id" in session

@admin_dashboard_controller.route("/")
def show_dashboard():
    if not is_logged_in():
        print("Not logged in, redirecting to login page")
        return redirect(url_for("auth_controller.login"))
    try:
        print("Fetching dashboard data...")
        # Get counts of all collections
        counts = {
            "admins": db.admins.count_documents({}),
            "devices": db.devices.count_documents({}),
            "images": db.images.count_documents({}),
            "feedbacks": db.feedbacks.count_documents({})
        }
        print(f"Collection counts: {counts}")

        # Get all results to count items by category
        results = list(db.results.find())
        print(f"Found {len(results)} results")
        
        # Count items by category
        fresh_count = sum(1 for res in results if 'Fresh' in str(res.get('predicted_class', '')))
        rotten_count = sum(1 for res in results if 'Rotten' in str(res.get('predicted_class', '')))
        other_count = sum(1 for res in results 
                         if not any(category in str(res.get('predicted_class', '')) 
                                  for category in ['Fresh', 'Rotten']))
        
        quality_counts = {
            "fresh": fresh_count,
            "rotten": rotten_count,
            "other": other_count
        }
        print(f"Quality counts: {quality_counts}")

        return render_template("dashboard.html",
            counts=counts,
            quality_counts=quality_counts
        )
    except Exception as e:
        print(f"Dashboard error: {str(e)}")
        print("Traceback:", traceback.format_exc())
        return render_template("error.html", message="Failed to load dashboard data"), 500