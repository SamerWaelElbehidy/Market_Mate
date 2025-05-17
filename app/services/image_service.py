import os
import uuid
from datetime import datetime
from app.db import db
from app.services.predict_service import PredictService

predict_service = PredictService()

def save_image(file, device_ID):
    image_ID = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()
    upload_folder = 'static/uploads'
    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, f"{image_ID}_{file.filename}")
    file.save(file_path)

    predicted_class, confidence, error_flag = predict_image(file_path)

    # Use the exact predicted class as the folder name
    if predicted_class == 'Other Item':
        class_folder = 'Other Item'
    elif predicted_class == 'Error':
        class_folder = 'Error'
    else:
        class_folder = predicted_class  # This will create folders like 'RottenApple', 'FreshBanana', etc.

    final_folder = os.path.join('static/images', class_folder)
    os.makedirs(final_folder, exist_ok=True)
    final_path = os.path.join(final_folder, os.path.basename(file_path))
    os.rename(file_path, final_path)

    # Save image metadata
    db.images.insert_one({
        "image_ID": image_ID,
        "device_ID": device_ID,
        "timestamp": timestamp,
        "path": final_path
    })

    # Save prediction results
    db.results.insert_one({
        "result_ID": str(uuid.uuid4()),
        "image_ID": image_ID,
        "confidence_level": confidence,
        "error_flag": error_flag,
        "predicted_class": predicted_class
    })

    return {
        "image_ID": image_ID,
        "path": final_path
    }, {
        "predicted_class": predicted_class,
        "confidence_level": confidence,
        "error_flag": error_flag
    }

def predict_image(image_path):
    try:
        predicted_class, confidence, error_flag = predict_service.predict(image_path)
        return predicted_class, confidence, error_flag
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        return "Error", 0, True