from flask import Blueprint, render_template, request, redirect, url_for, session, send_file, make_response
from app.db import db
import csv
from io import StringIO
from datetime import datetime
import traceback

admin_device_controller = Blueprint('admin_device_controller', __name__, url_prefix='/devices')

def is_logged_in():
    return "admin_id" in session

@admin_device_controller.route("/")
def list_devices():
    if not is_logged_in():
        return redirect(url_for("auth_controller.login"))
    try:
        page = int(request.args.get('page', 1))
        per_page = 10
        devices = list(db.devices.find().skip((page-1)*per_page).limit(per_page))
        return render_template("devices.html", devices=devices, page=page)
    except Exception as e:
        print(f"Devices list error: {e}")
        return render_template("error.html", message="Failed to load devices"), 500

@admin_device_controller.route("/download-csv")
def download_devices_csv():
    if not is_logged_in():
        return redirect(url_for("auth_controller.login"))
    try:
        # Get all devices
        devices = list(db.devices.find())
        print(f"Found {len(devices)} devices")
        
        # Create a string buffer and write to it
        si = StringIO()
        writer = csv.writer(si)
        
        # Write headers
        writer.writerow(['Device ID', 'Device Type', 'Device Model', 'Timestamp'])
        
        # Write data rows
        for device in devices:
            try:
                row = [
                    str(device.get('device_ID', '')),
                    str(device.get('device_type', '')),
                    str(device.get('device_model', '')),
                    str(device.get('timestamp', ''))
                ]
                writer.writerow(row)
            except Exception as row_error:
                print(f"Error writing row for device: {device}")
                print(f"Row error: {str(row_error)}")
                continue
        
        # Create the response
        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = f"attachment; filename=devices_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        output.headers["Content-type"] = "text/csv"
        return output
        
    except Exception as e:
        error_details = traceback.format_exc()
        print(f"Download devices CSV error: {str(e)}")
        print(f"Error traceback: {error_details}")
        return render_template("error.html", message=f"Failed to download devices: {str(e)}"), 500

@admin_device_controller.route("/delete-all")
def delete_all_devices():
    if not is_logged_in():
        return redirect(url_for("auth_controller.login"))
    try:
        # Delete all device records
        db.devices.delete_many({})
        
        # Delete associated analysis results and images
        db.results.delete_many({})
        db.images.delete_many({})

        return redirect(url_for("admin_device_controller.list_devices"))
    except Exception as e:
        print(f"Delete all devices error: {e}")
        return render_template("error.html", message="Failed to delete all devices"), 500