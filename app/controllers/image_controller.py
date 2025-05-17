from flask import Blueprint, request, jsonify
from app.services.image_service import save_image, predict_image

image_controller = Blueprint('image_controller', __name__)

@image_controller.route('/upload-image', methods=['POST'])
def upload_image():
    """
    Upload an image and get a prediction.
    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: device_ID
        in: formData
        type: string
        required: true
      - name: image
        in: formData
        type: file
        required: true
    responses:
      200:
        description: Prediction result
        schema:
          type: object
          properties:
            prediction:
              type: string
            image_ID:
              type: string
      400:
        description: Bad request
    """
    device_ID = request.form.get('device_ID')
    file = request.files.get('image')

    if not device_ID or not file or file.filename == '':
        return jsonify({"error": "Invalid input"}), 400

    image_metadata, prediction_result = save_image(file, device_ID)
    return jsonify({
        "image_ID": image_metadata['image_ID'],
        "prediction": prediction_result['predicted_class']
    })