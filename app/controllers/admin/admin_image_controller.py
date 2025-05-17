from flask import Blueprint, render_template, redirect, url_for, session, send_file
from app.db import db
import os
import zipfile
from io import BytesIO
from datetime import datetime

admin_image_controller = Blueprint('admin_image_controller', __name__, url_prefix='/images')

def is_logged_in():
    return "admin_id" in session

@admin_image_controller.route("/")
def list_images():
    if not is_logged_in():
        return redirect(url_for("auth_controller.login"))
    try:
        images = list(db.images.find())
        return render_template("images.html", images=images)
    except Exception as e:
        print(f"Images error: {e}")
        return render_template("error.html", message="Failed to load images"), 500

@admin_image_controller.route("/<image_id>/delete")
def delete_image(image_id):
    if not is_logged_in():
        return redirect(url_for("auth_controller.login"))
    try:
        # Get the image document first
        image = db.images.find_one({"image_ID": image_id})
        if not image:
            return redirect(url_for("admin_image_controller.list_images"))

        # Delete the physical image file
        if image.get('path') and os.path.exists(image['path']):
            os.remove(image['path'])

        # Delete the image record from the database
        db.images.delete_one({"image_ID": image_id})

        # Delete associated analysis results
        db.results.delete_many({"image_ID": image_id})

        return redirect(url_for("admin_image_controller.list_images"))
    except Exception as e:
        print(f"Delete image error: {e}")
        return render_template("error.html", message="Failed to delete image"), 500

@admin_image_controller.route("/download-all")
def download_all_images():
    if not is_logged_in():
        return redirect(url_for("auth_controller.login"))
    try:
        images = list(db.images.find())
        if not images:
            return redirect(url_for("admin_image_controller.list_images"))

        # Create a BytesIO object to store the ZIP file
        memory_file = BytesIO()
        
        # Create the ZIP file
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for image in images:
                if image.get('path') and os.path.exists(image['path']):
                    # Get original filename from path
                    original_name = os.path.basename(image['path'])
                    # Add file to ZIP with original name
                    zf.write(image['path'], original_name)

        # Seek to the beginning of the BytesIO object
        memory_file.seek(0)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'all_images_{timestamp}.zip'
        )
    except Exception as e:
        print(f"Download all images error: {e}")
        return render_template("error.html", message="Failed to download images"), 500

@admin_image_controller.route("/delete-all")
def delete_all_images():
    if not is_logged_in():
        return redirect(url_for("auth_controller.login"))
    try:
        images = list(db.images.find())
        
        # Delete all physical image files
        for image in images:
            if image.get('path') and os.path.exists(image['path']):
                os.remove(image['path'])

        # Delete all image records
        db.images.delete_many({})
        
        # Delete all analysis results
        db.results.delete_many({})

        return redirect(url_for("admin_image_controller.list_images"))
    except Exception as e:
        print(f"Delete all images error: {e}")
        return render_template("error.html", message="Failed to delete all images"), 500