import os
import json
from flask import Blueprint, jsonify
from services.history_service import history_service

stats_bp = Blueprint('stats_bp', __name__)

@stats_bp.route('/predictions/stats', methods=['GET'])
def get_prediction_stats():
    """Returns aggregated live dashboard statistics."""
    stats = history_service.get_stats()
    
    # Check best model from metadata
    meta_path = 'trained_models/best_model_meta.json'
    best_model_name = 'EfficientNetB0'
    if os.path.exists(meta_path):
        try:
            with open(meta_path, 'r') as f:
                data = json.load(f)
                best_model_name = data.get('best_model_name', 'EfficientNetB0')
        except Exception:
            pass

    stats['bestModel'] = best_model_name
    return jsonify(stats), 200

@stats_bp.route('/predictions/history', methods=['GET'])
def get_prediction_history():
    """Returns recent prediction records."""
    records = history_service.get_history(limit=50)
    return jsonify(records), 200

@stats_bp.route('/datasets/stats', methods=['GET'])
def get_dataset_stats():
    """Returns actual dataset audit numbers, class distributions, and split metadata."""
    return jsonify({
        'totalImages': 6949,
        'trainSplit': 4864,
        'trainPercent': '70.0%',
        'validationSplit': 1042,
        'validationPercent': '15.0%',
        'testSplit': 1043,
        'testPercent': '15.0%',
        'classes': ['Safe', 'Moderate Risk', 'High Risk'],
        'classDistribution': {
            'Safe': {
                'count': 2350,
                'percentage': '33.82%',
                'train': 1645,
                'val': 353,
                'test': 352,
                'weight': 0.9856
            },
            'Moderate Risk': {
                'count': 307,
                'percentage': '4.42%',
                'train': 215,
                'val': 46,
                'test': 46,
                'weight': 7.5411
            },
            'High Risk': {
                'count': 4292,
                'percentage': '61.76%',
                'train': 3004,
                'val': 643,
                'test': 645,
                'weight': 0.5397
            }
        },
        'sources': [
            {
                'name': 'BDD100K',
                'fullName': 'Berkeley DeepDrive 100K',
                'description': 'Diverse driving dataset covering highway, urban streets, varying daylight, night, rain, and snow conditions across US cities.',
                'imagesUsed': 3240,
                'color': '#2563EB'
            },
            {
                'name': 'IDD',
                'fullName': 'India Driving Dataset',
                'description': 'Challenging Indian road environments capturing mixed traffic, pedestrian crossings, unstructured intersections, and chaotic movement.',
                'imagesUsed': 2150,
                'color': '#F59E0B'
            },
            {
                'name': 'Custom YouTube Intersections',
                'fullName': 'Real-World Intersection CCTV & Video Captures',
                'description': 'Curated high-risk intersection scenarios, collision trajectories, hazardous vehicle proximity, and sudden pedestrian conflicts.',
                'imagesUsed': 1559,
                'color': '#EF4444'
            }
        ],
        'splitRatio': '70% Train · 15% Validation · 15% Test',
        'resolution': '224 × 224 × 3',
        'randomSeed': 42,
        'augmentations': ['Random Horizontal Flip', 'Small Rotation (±10°)', 'Random Zoom (±10%)', 'Brightness Variation (±10%)'],
        'preprocessing': ['Read Image', 'Convert to RGB', 'Resize to 224×224', 'Normalize to [0, 1]']
    }), 200
