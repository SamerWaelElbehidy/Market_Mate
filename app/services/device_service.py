import uuid
from datetime import datetime
from app.db import db 

def insert_device(device_model, device_type):
    device_ID = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()

    db.devices.insert_one({
        "device_ID": device_ID,
        "device_model": device_model,
        "device_type": device_type,
        "timestamp": timestamp
    })

    return device_ID