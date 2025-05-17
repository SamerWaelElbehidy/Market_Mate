import os
import uuid
from datetime import datetime
from app.db import db

def save_feedback(file, device_ID):
    feedback_ID = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()
    feedback_folder = 'static/feedbacks'
    os.makedirs(feedback_folder, exist_ok=True)

    file_path = os.path.join(feedback_folder, f"{feedback_ID}_{file.filename}")
    file.save(file_path)

    db.feedbacks.insert_one({
        "feedback_ID": feedback_ID,
        "device_ID": device_ID,
        "file_path": file_path,
        "timestamp": timestamp,
        "viewed_flag": False
    })

    return feedback_ID