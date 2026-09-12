import os
import json
from flask import Blueprint, jsonify

models_bp = Blueprint('models_bp', __name__)

@models_bp.route('/models/list', methods=['GET'])
def list_models():
    """Returns list of selectable trained models for the Prediction UI dropdown."""
    models_dir = 'trained_models'
    trained = []
    
    meta_path = os.path.join(models_dir, 'best_model_meta.json')
    best_key = 'cnn'
    best_name = 'Custom CNN Baseline'
    if os.path.exists(meta_path):
        try:
            with open(meta_path, 'r') as f:
                meta = json.load(f)
                best_key = meta.get('best_model_key', 'cnn')
                best_name = meta.get('best_model_name', 'Custom CNN Baseline')
        except Exception:
            pass

    available_map = {
        'best': f"Best Model ({best_name})",
        'cnn': 'Custom CNN Baseline',
        'mobilenetv2': 'MobileNetV2',
        'efficientnetb0': 'EfficientNetB0',
        'resnet50': 'ResNet50'
    }

    for key, label in available_map.items():
        if key == 'best':
            trained.append({'key': key, 'name': label, 'is_best': True})
        else:
            w_path = os.path.join(models_dir, f"{key}_best.keras")
            is_trained = os.path.exists(w_path)
            trained.append({'key': key, 'name': label, 'trained': is_trained, 'is_best': False})

    return jsonify({'models': trained, 'best_model': best_name}), 200

@models_bp.route('/models/comparison', methods=['GET'])
def get_comparison():
    """Returns actual measured comparison table across models."""
    comparison_file = 'results/model_comparison.json'
    if os.path.exists(comparison_file):
        with open(comparison_file, 'r') as f:
            data = json.load(f)
        return jsonify(data), 200

    # Fallback to reading individual metrics
    metrics = []
    for m in ['cnn', 'mobilenetv2', 'efficientnetb0', 'resnet50']:
        path = f'results/{m}/test_metrics.json'
        if os.path.exists(path):
            with open(path, 'r') as f:
                metrics.append(json.load(f))

    return jsonify({'comparison': metrics, 'best_model': metrics[0] if metrics else None}), 200

@models_bp.route('/models/metrics', methods=['GET'])
def get_metrics():
    """Returns metrics, curves, and confusion matrix data for Analytics."""
    models_data = {}
    for m in ['cnn', 'mobilenetv2', 'efficientnetb0', 'resnet50']:
        metric_file = f'results/{m}/test_metrics.json'
        hist_file = f'results/{m}/history.json'
        data = {}
        if os.path.exists(metric_file):
            with open(metric_file, 'r') as f:
                data['metrics'] = json.load(f)
        if os.path.exists(hist_file):
            with open(hist_file, 'r') as f:
                data['history'] = json.load(f)
        if data:
            models_data[m] = data

    return jsonify(models_data), 200
