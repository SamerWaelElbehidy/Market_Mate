from flask import Blueprint, render_template, redirect, url_for, session, send_file, make_response
from app.db import db
import csv
from io import StringIO
from datetime import datetime
import traceback

admin_analysis_controller = Blueprint('admin_analysis_controller', __name__, url_prefix='/analysis')

def is_logged_in():
    return "admin_id" in session

@admin_analysis_controller.route("/")
def list_analysis():
    if not is_logged_in():
        return redirect(url_for("auth_controller.login"))
    try:
        results = list(db.results.find())
        return render_template("analysis.html", results=results)
    except Exception as e:
        print(f"Analysis error: {e}")
        return render_template("error.html", message="Failed to load analysis results"), 500

@admin_analysis_controller.route("/download-csv")
def download_analysis_csv():
    if not is_logged_in():
        return redirect(url_for("auth_controller.login"))
    try:
        # Get all results with image information
        results = list(db.results.find())
        print(f"Found {len(results)} analysis results")
        
        # Create a string buffer and write to it
        si = StringIO()
        writer = csv.writer(si)
        
        # Write headers
        writer.writerow(['Image ID', 'Predicted Class', 'Quality Score', 'Error Flag', 'Category'])
        
        # Write data rows
        for result in results:
            try:
                predicted_class = str(result.get('predicted_class', ''))
                
                # Determine category (matching dashboard logic)
                if result.get('error_flag'):
                    category = 'Error'
                elif 'Fresh' in predicted_class:
                    category = 'Fresh'
                elif 'Rotten' in predicted_class:
                    category = 'Rotten'
                else:
                    category = 'Other'
                
                row = [
                    str(result.get('image_ID', '')),
                    predicted_class,
                    str(result.get('quality_score', '')),
                    'Yes' if result.get('error_flag') else 'No',
                    category
                ]
                writer.writerow(row)
            except Exception as row_error:
                print(f"Error writing row for result: {result}")
                print(f"Row error: {str(row_error)}")
                continue
        
        # Create the response
        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = f"attachment; filename=analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        output.headers["Content-type"] = "text/csv"
        return output
        
    except Exception as e:
        error_details = traceback.format_exc()
        print(f"Download analysis CSV error: {str(e)}")
        print(f"Error traceback: {error_details}")
        return render_template("error.html", message=f"Failed to download analysis results: {str(e)}"), 500