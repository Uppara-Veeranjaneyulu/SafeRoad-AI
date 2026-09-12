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

    # 3. Validate that the uploaded image is a valid road scene (Reject portraits/selfies)
    np_image = np.array(pil_image)
    h, w = np_image.shape[:2]
    ymin, ymax = int(h * 0.15), int(h * 0.75)
    xmin, xmax = int(w * 0.20), int(w * 0.80)
    center = np_image[ymin:ymax, xmin:xmax]

    r = center[:, :, 0].astype(float)
    g = center[:, :, 1].astype(float)
    b = center[:, :, 2].astype(float)
    y_val = 0.299 * r + 0.587 * g + 0.114 * b
    cb = -0.1687 * r - 0.3313 * g + 0.5 * b + 128
    cr = 0.5 * r - 0.4187 * g - 0.0813 * b + 128
    skin_pixels = (cr >= 135) & (cr <= 180) & (cb >= 85) & (cb <= 135) & (y_val >= 50)
    skin_ratio = float(np.mean(skin_pixels))

    bot_y = int(h * 0.65)
    bot = np_image[bot_y:, :]
    br = bot[:, :, 0].astype(float)
    bg = bot[:, :, 1].astype(float)
    bb = bot[:, :, 2].astype(float)
    asphalt_mask = (np.abs(br - bg) < 32) & (np.abs(br - bb) < 32) & (br < 210) & (bg < 210)
    asphalt_ratio = float(np.mean(asphalt_mask))

    is_portrait = skin_ratio > 0.35 or (skin_ratio > 0.18 and asphalt_ratio < 0.35)
    if is_portrait:
        return jsonify({
            'isInvalidScene': True,
            'sceneType': 'portrait',
            'risk': 'Invalid Input',
            'riskLevel': 'invalid',
            'title': 'Portrait / Personal Photo Detected',
            'message': 'The uploaded image contains a portrait or personal photo. SafeRoad AI models are trained exclusively on forward-facing road scenes and dashcam video.',
            'recommendation': 'Please upload an authentic road scene (highway, intersection, or urban street).',
            'details': {
                'skinRatio': f"{skin_ratio * 100:.1f}%",
                'roadProfile': f"{asphalt_ratio * 100:.1f}%"
            }
        }), 400

    # 4. Run YOLOv8 Context Detection
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
