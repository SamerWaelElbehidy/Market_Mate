from flask import Blueprint, request, jsonify
from app.services.device_service import insert_device

device_controller = Blueprint('device_controller', __name__)

@device_controller.route('/register-device', methods=['POST'])
def register_device():
    """
    Register a new device.
    ---
    consumes:
      - application/json
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            device_model:
              type: string
            device_type:
              type: string
    responses:
      200:
        description: Device registered successfully
        schema:
          type: object
          properties:
            device_ID:
              type: string
      400:
        description: Bad request
    """
    data = request.get_json()
    if not data or 'device_model' not in data or 'device_type' not in data:
        return jsonify({"error": "Invalid input"}), 400

    device_ID = insert_device(data['device_model'], data['device_type'])
    return jsonify({"device_ID": device_ID})