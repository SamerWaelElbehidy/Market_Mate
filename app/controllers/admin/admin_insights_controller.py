from flask import Blueprint, render_template, redirect, url_for, session
from app.db import db
from datetime import datetime, timedelta
import numpy as np
from bson import ObjectId

admin_insights_controller = Blueprint('admin_insights_controller', __name__, url_prefix='/insights')

def is_logged_in():
    return "admin_id" in session

def format_class_name(class_name):
    """Format the class name for better display"""
    if not class_name:
        return "Unknown"
    # Remove any extra whitespace and quotes
    class_name = str(class_name).strip().strip('"\'')
    # Split into words and capitalize each word
    words = class_name.replace('_', ' ').split()
    # Handle special case for FreshX and RottenX
    if len(words) == 1 and ('Fresh' in words[0] or 'Rotten' in words[0]):
        quality = 'Fresh' if 'Fresh' in words[0] else 'Rotten'
        fruit = words[0].replace('Fresh', '').replace('Rotten', '')
        words = [quality, fruit]
    return ' '.join(word.capitalize() for word in words)

def safe_float(value):
    """Safely convert a value to float"""
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            # Remove any % sign and convert to decimal
            return float(value.strip('%')) / 100 if '%' in value else float(value)
        except (ValueError, TypeError):
            return None
    return None

@admin_insights_controller.route("/")
def show_insights():
    if not is_logged_in():
        return redirect(url_for("auth_controller.login"))
    try:
        # Get all results, no need for timestamp sorting since we don't have it
        results = list(db.results.find())
        if not results:
            # Return empty data if no results
            return render_template("insights.html",
                quality_distribution=[0, 0, 0],
                confidence_distribution=[0, 0, 0, 0, 0],
                daily_labels=[(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)],
                daily_activity=[0] * 7,
                top_items_labels=["No Data"],
                top_items_data=[0],
                error_rate_labels=[(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)],
                error_rate_data=[0] * 7,
                device_labels=['Mobile', 'Tablet', 'Desktop', 'Other'],
                device_data=[0] * 4,
                categories=[],
                accuracy_data=[],
                confidence_data=[],
                hours=[f"{hour:02d}:00" for hour in range(24)],
                hourly_activity=[0] * 24,
                total_predictions=0,
                avg_confidence=0,
                error_rate=0,
                active_devices=0
            )
        
        # Quality Distribution with better categorization
        fresh_count = sum(1 for r in results if 'Fresh' in str(r.get('predicted_class', '')))
        rotten_count = sum(1 for r in results if 'Rotten' in str(r.get('predicted_class', '')))
        other_count = len(results) - (fresh_count + rotten_count)
        
        quality_distribution = [fresh_count, rotten_count, other_count]
        
        # Enhanced Confidence Distribution
        confidences = []
        for r in results:
            conf = safe_float(r.get('confidence_level'))
            if conf is not None and 0 <= conf <= 1:
                confidences.append(conf)
        
        confidence_ranges = [(0.9, 1.0), (0.8, 0.9), (0.7, 0.8), (0.6, 0.7), (0, 0.6)]
        confidence_distribution = [
            sum(1 for c in confidences if low <= c < high)
            for low, high in confidence_ranges
        ]
        
        # Daily labels for time-based charts
        today = datetime.now()
        daily_labels = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
        daily_activity = [0] * 7  # Initialize with zeros
        
        # Get daily activity using actual timestamps
        for result in results:
            image_id = result.get('image_ID')
            if image_id:
                image = db.images.find_one({'image_ID': image_id})
                if image and 'timestamp' in image:
                    try:
                        # Parse the timestamp string
                        timestamp = datetime.strptime(image['timestamp'], '%Y-%m-%dT%H:%M:%S.%f')
                        # Find which day this timestamp belongs to
                        for i, day in enumerate(daily_labels):
                            if timestamp.strftime('%Y-%m-%d') == day:
                                daily_activity[i] += 1
                                break
                    except (ValueError, TypeError):
                        continue
        
        # Enhanced Top Items with better formatting
        item_counts = {}
        for r in results:
            pred_class = format_class_name(r.get('predicted_class', ''))
            if pred_class != "Unknown":
                # Remove Fresh/Rotten prefix for grouping
                base_class = pred_class.replace('Fresh ', '').replace('Rotten ', '')
                item_counts[base_class] = item_counts.get(base_class, 0) + 1
        
        # Get top 5 items
        top_items = sorted(item_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        if not top_items:
            top_items = [("No Data", 0)]
        top_items_labels = [item[0] for item in top_items]
        top_items_data = [item[1] for item in top_items]
        
        # Error Rate Timeline
        total_results = len(results)
        if total_results > 0:
            error_count = sum(1 for r in results if r.get('error_flag', 0) == 1)
            error_rate = error_count / total_results
            error_rate_data = [error_rate] * 7
        else:
            error_rate_data = [0] * 7
        
        # Enhanced Device Usage with proper categorization
        devices = list(db.devices.find())
        device_types = {
            'mobile': ['mobile', 'phone', 'android', 'ios', 'iphone'],
            'tablet': ['tablet', 'ipad'],
            'desktop': ['desktop', 'laptop', 'pc', 'computer', 'windows', 'mac', 'linux'],
            'other': []
        }
        
        device_counts = {'Mobile': 0, 'Tablet': 0, 'Desktop': 0, 'Other': 0}
        for device in devices:
            device_type = str(device.get('device_type', '')).lower()
            categorized = False
            for category, keywords in device_types.items():
                if any(keyword in device_type for keyword in keywords):
                    device_counts[category.capitalize()] += 1
                    categorized = True
                    break
            if not categorized:
                device_counts['Other'] += 1
        
        device_labels = list(device_counts.keys())
        device_data = list(device_counts.values())
        
        # Enhanced Model Performance by Category
        all_classes = [
            'Apple', 'Banana', 'Orange', 'Mango', 'Strawberry',
            'Tomato', 'Cucumber', 'Carrot', 'Bellpepper', 'Potato',
            'Other'
        ]
        
        confidence_data = []
        
        for category in all_classes:
            # Skip 'Other' as it's a special case
            if category == 'Other':
                other_results = [r for r in results 
                               if 'Other' in str(r.get('predicted_class', ''))]
            else:
                # Match both Fresh and Rotten variants
                category_results = [r for r in results 
                                  if category.lower() in str(r.get('predicted_class', '')).lower()]
            
            results_to_process = other_results if category == 'Other' else category_results
            
            if results_to_process:
                # Calculate average confidence
                valid_confidences = []
                for r in results_to_process:
                    conf = safe_float(r.get('confidence_level'))
                    if conf is not None and 0 <= conf <= 1:
                        valid_confidences.append(conf)
                
                avg_confidence = np.mean(valid_confidences) if valid_confidences else 0
                confidence_data.append(round(avg_confidence, 2))
            else:
                confidence_data.append(0)
        
        # Time Distribution
        hour_labels = [f"{hour:02d}:00" for hour in range(24)]
        hourly_activity = [0] * 24

        # Get timestamps from images collection and match with results
        for result in results:
            image_id = result.get('image_ID')
            if image_id:
                image = db.images.find_one({'image_ID': image_id})
                if image and 'timestamp' in image:
                    try:
                        # Parse the timestamp string
                        timestamp = datetime.strptime(image['timestamp'], '%Y-%m-%dT%H:%M:%S.%f')
                        hour = timestamp.hour
                        hourly_activity[hour] += 1
                    except (ValueError, TypeError):
                        continue
        
        # Calculate summary statistics
        total_predictions = len(results)
        avg_confidence = round(np.mean(confidences) * 100, 1) if confidences else 0
        overall_error_rate = round(sum(1 for r in results if r.get('error_flag', 0) == 1) 
                                 / len(results) * 100, 1) if results else 0
        active_devices = len(devices)
        
        return render_template("insights.html",
            quality_distribution=quality_distribution,
            confidence_distribution=confidence_distribution,
            daily_labels=daily_labels,
            daily_activity=daily_activity,
            top_items_labels=top_items_labels,
            top_items_data=top_items_data,
            error_rate_labels=daily_labels,
            error_rate_data=error_rate_data,
            device_labels=device_labels,
            device_data=device_data,
            categories=all_classes,
            accuracy_data=[],
            confidence_data=confidence_data,
            hours=hour_labels,
            hourly_activity=hourly_activity,
            total_predictions=total_predictions,
            avg_confidence=avg_confidence,
            error_rate=overall_error_rate,
            active_devices=active_devices
        )
        
    except Exception as e:
        print(f"Insights error: {str(e)}")
        return render_template("error.html", message="Failed to load insights data"), 500 