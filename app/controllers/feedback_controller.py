from flask import Blueprint, request, jsonify
from app.services.feedback_service import save_feedback

feedback_controller = Blueprint('feedback_controller', __name__)

@feedback_controller.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    """
    Submit feedback with a voice message.
    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: device_ID
        in: formData
        type: string
        required: true
      - name: voice_message
        in: formData
        type: file
        required: true
    responses:
      200:
        description: Feedback submitted successfully
        schema:
          type: object
          properties:
            feedback_ID:
              type: string
      400:
        description: Bad request
    """
    device_ID = request.form.get('device_ID')
    file = request.files.get('voice_message')

    if not device_ID or not file or file.filename == '':
        return jsonify({"error": "Invalid input"}), 400

    feedback_ID = save_feedback(file, device_ID)
    return jsonify({"feedback_ID": feedback_ID})