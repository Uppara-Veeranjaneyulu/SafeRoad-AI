import io
import numpy as np
from PIL import Image
from flask import Blueprint, request, jsonify
from services.yolo_service import yolo_service
from services.model_service import model_service
from services.history_service import history_service

predict_bp = Blueprint('predict_bp', __name__)

@predict_bp.route('/predict', methods=['POST'])
def predict():
    # 1. Validate Image
    if 'image' not in request.files and 'file' not in request.files:
        return jsonify({'error': 'No image file provided in request'}), 400

    file = request.files.get('image') or request.files.get('file')
    if file.filename == '':
        return jsonify({'error': 'Empty filename uploaded'}), 400

    try:
        image_bytes = file.read()
        pil_image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    except Exception as e:
        return jsonify({'error': f'Invalid image format: {str(e)}'}), 400

    # 2. Extract query or form params
    requested_model = request.args.get('model') or request.form.get('model') or 'best'

    # 3. Run YOLOv8 Context Detection
    np_image = np.array(pil_image)
    yolo_context = yolo_service.analyze(np_image)

    # 4. Run Risk Classification with Selected DL Model
    try:
        prediction_result = model_service.predict(
            pil_image,
            requested_model=requested_model,
            yolo_context=yolo_context
        )
    except Exception as e:
        return jsonify({'error': f'Prediction engine failure: {str(e)}'}), 500

    # 5. Assemble final response payload
    response_payload = {
        'risk': prediction_result['risk'],
        'riskLevel': prediction_result['riskLevel'],
        'confidence': prediction_result['confidence'],
        'model': prediction_result['model'],
        'model_key': prediction_result['model_key'],
        'inferenceTime': prediction_result['inferenceTime'],
        'inference_time_ms': prediction_result['inference_time_ms'],
        'vehicle_count': yolo_context['vehicle_count'],
        'pedestrian_count': yolo_context['pedestrian_count'],
        'trafficDensity': yolo_context['traffic_density'],
        'traffic_density': yolo_context['traffic_density'],
        'yoloObjects': yolo_context['objects'],
        'weather': 'Clear Daylight',
        'roadType': 'Urban Road' if yolo_context['vehicle_count'] > 4 else 'Open Highway',
        'possibleCauses': prediction_result['possibleCauses'],
        'recommendations': prediction_result['recommendations'],
        'recommendation': prediction_result['recommendations'][0] if prediction_result['recommendations'] else 'Proceed with caution',
        'class_probabilities': prediction_result['class_probabilities']
    }

    # 6. Record to History
    history_service.add_record({
        'image': file.filename,
        'model': prediction_result['model'],
        'risk': prediction_result['risk'],
        'confidence': prediction_result['confidence'],
        'traffic': yolo_context['traffic_density'],
        'weather': response_payload['weather'],
        'duration': prediction_result['inferenceTime']
    })

    return jsonify(response_payload), 200
