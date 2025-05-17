from flask import Blueprint, render_template, redirect, url_for, session, send_file
from app.db import db
import os
import zipfile
from io import BytesIO
from datetime import datetime

admin_feedback_controller = Blueprint('admin_feedback_controller', __name__, url_prefix='/feedbacks')

def is_logged_in():
    return "admin_id" in session

@admin_feedback_controller.route("/")
def list_feedbacks():
    if not is_logged_in():
        return redirect(url_for("auth_controller.login"))
    try:
        feedbacks = list(db.feedbacks.find())
        return render_template("feedbacks.html", feedbacks=feedbacks)
    except Exception as e:
        print(f"Feedbacks error: {e}")
        return render_template("error.html", message="Failed to load feedbacks"), 500

@admin_feedback_controller.route("/<feedback_id>/delete")
def delete_feedback(feedback_id):
    if not is_logged_in():
        return redirect(url_for("auth_controller.login"))
    try:
        # Get the feedback document first
        feedback = db.feedbacks.find_one({"feedback_ID": feedback_id})
        if not feedback:
            return redirect(url_for("admin_feedback_controller.list_feedbacks"))

        # Delete the physical audio file
        if feedback.get('file_path') and os.path.exists(feedback['file_path']):
            os.remove(feedback['file_path'])

        # Delete the feedback record from the database
        db.feedbacks.delete_one({"feedback_ID": feedback_id})

        return redirect(url_for("admin_feedback_controller.list_feedbacks"))
    except Exception as e:
        print(f"Delete feedback error: {e}")
        return render_template("error.html", message="Failed to delete feedback"), 500

@admin_feedback_controller.route("/download-all")
def download_all_feedbacks():
    if not is_logged_in():
        return redirect(url_for("auth_controller.login"))
    try:
        feedbacks = list(db.feedbacks.find())
        if not feedbacks:
            return redirect(url_for("admin_feedback_controller.list_feedbacks"))

        # Create a BytesIO object to store the ZIP file
        memory_file = BytesIO()
        
        # Create the ZIP file
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for feedback in feedbacks:
                if feedback.get('file_path') and os.path.exists(feedback['file_path']):
                    # Get original filename from path
                    original_name = os.path.basename(feedback['file_path'])
                    # Add file to ZIP with original name
                    zf.write(feedback['file_path'], original_name)

        # Seek to the beginning of the BytesIO object
        memory_file.seek(0)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'all_feedbacks_{timestamp}.zip'
        )
    except Exception as e:
        print(f"Download all feedbacks error: {e}")
        return render_template("error.html", message="Failed to download feedbacks"), 500

@admin_feedback_controller.route("/delete-all")
def delete_all_feedbacks():
    if not is_logged_in():
        return redirect(url_for("auth_controller.login"))
    try:
        feedbacks = list(db.feedbacks.find())
        
        # Delete all physical feedback files
        for feedback in feedbacks:
            if feedback.get('file_path') and os.path.exists(feedback['file_path']):
                os.remove(feedback['file_path'])

        # Delete all feedback records
        db.feedbacks.delete_many({})

        return redirect(url_for("admin_feedback_controller.list_feedbacks"))
    except Exception as e:
        print(f"Delete all feedbacks error: {e}")
        return render_template("error.html", message="Failed to delete all feedbacks"), 500