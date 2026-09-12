import os
import time
import json
import numpy as np
from PIL import Image
import tensorflow as tf

CLASS_NAMES = ['Safe', 'Moderate Risk', 'High Risk']
RISK_LEVEL_MAP = {
    'Safe': 'low',
    'Moderate Risk': 'moderate',
    'High Risk': 'high'
}

class ModelService:
    def __init__(self, models_dir='trained_models', results_dir='results'):
        self.models_dir = models_dir
        self.results_dir = results_dir
        self.loaded_models = {}
        self.best_model_name = None
        self.best_model_key = None
        self.refresh_best_model_info()

    def refresh_best_model_info(self):
        meta_path = os.path.join(self.models_dir, 'best_model_meta.json')
        if os.path.exists(meta_path):
            try:
                with open(meta_path, 'r') as f:
                    data = json.load(f)
                    self.best_model_name = data.get('best_model_name', 'EfficientNetB0')
                    self.best_model_key = data.get('best_model_key', 'efficientnetb0')
            except Exception as e:
                print(f"[ModelService] Error reading meta: {e}")
        else:
            self.best_model_name = 'Custom CNN'
            self.best_model_key = 'cnn'

    def get_model(self, model_key=None):
        self.refresh_best_model_info()
        if not model_key or model_key == 'best':
            model_key = self.best_model_key or 'cnn'

        model_key = model_key.lower().replace(' ', '').replace('_', '')
        # Map common aliases
        alias_map = {
            'cnn': 'cnn',
            'customcnn': 'cnn',
            'mobilenet': 'mobilenetv2',
            'mobilenetv2': 'mobilenetv2',
            'efficientnet': 'efficientnetb0',
            'efficientnetb0': 'efficientnetb0',
            'resnet': 'resnet50',
            'resnet50': 'resnet50'
        }
        canonical_key = alias_map.get(model_key, self.best_model_key or 'cnn')

        if canonical_key in self.loaded_models:
            return self.loaded_models[canonical_key], canonical_key

        model_filename = f"{canonical_key}_best.keras"
        model_filepath = os.path.join(self.models_dir, model_filename)

        if not os.path.exists(model_filepath):
            # Fallback to any available trained model
            available = [f for f in os.listdir(self.models_dir) if f.endswith('.keras')]
            if available:
                model_filepath = os.path.join(self.models_dir, available[0])
                canonical_key = available[0].split('_')[0]
            else:
                raise FileNotFoundError(f"No trained model found in {self.models_dir}. Please train models first!")

        print(f"[ModelService] Loading model weights from {model_filepath}...")
        model = tf.keras.models.load_model(model_filepath, safe_mode=False)
        self.loaded_models[canonical_key] = model
        return model, canonical_key

    def preprocess_image(self, pil_image):
        """Converts PIL image to RGB, resizes to 224x224, and normalizes to [0, 1]."""
        img = pil_image.convert('RGB')
        img = img.resize((224, 224), Image.Resampling.BILINEAR)
        arr = np.array(img, dtype=np.float32) / 255.0
        arr = np.expand_dims(arr, axis=0)  # Shape (1, 224, 224, 3)
        return arr

    def predict(self, pil_image, requested_model='best', yolo_context=None):
        """
        Executes inference using the requested or best trained model.
        Calculates confidence, risk label, inference time, causes, and recommendations.
        """
        model, active_key = self.get_model(requested_model)
        input_tensor = self.preprocess_image(pil_image)

        # Warmup and time inference
        start_time = time.time()
        preds = model.predict(input_tensor, verbose=0)[0]
        inference_time_ms = round((time.time() - start_time) * 1000.0, 1)

        pred_class_idx = int(np.argmax(preds))
        confidence = float(preds[pred_class_idx])
        confidence_percent = round(confidence * 100.0, 1)
        risk_name = CLASS_NAMES[pred_class_idx]
        risk_level = RISK_LEVEL_MAP.get(risk_name, 'moderate')

        # Display names
        display_names = {
            'cnn': 'Custom CNN Baseline',
            'mobilenetv2': 'MobileNetV2',
            'efficientnetb0': 'EfficientNetB0',
            'resnet50': 'ResNet50'
        }
        display_model_name = display_names.get(active_key, active_key.capitalize())

        # Generate context-aware causes & recommendations
        causes, recommendations = self._generate_advice(risk_name, yolo_context)

        return {
            'risk': risk_name,
            'riskLevel': risk_level,
            'confidence': confidence_percent,
            'raw_confidence': confidence,
            'class_probabilities': {
                CLASS_NAMES[i]: round(float(preds[i]) * 100.0, 2)
                for i in range(len(CLASS_NAMES))
            },
            'model': display_model_name,
            'model_key': active_key,
            'inferenceTime': f"{inference_time_ms}ms",
            'inference_time_ms': inference_time_ms,
            'possibleCauses': causes,
            'recommendations': recommendations
        }

    def _generate_advice(self, risk_name, yolo_context):
        veh_count = yolo_context.get('vehicle_count', 0) if yolo_context else 0
        ped_count = yolo_context.get('pedestrian_count', 0) if yolo_context else 0
        density = yolo_context.get('traffic_density', 'Moderate') if yolo_context else 'Moderate'

        if risk_name == 'High Risk':
            causes = [
                f"Elevated traffic density ({density}) with {veh_count} vehicles in immediate proximity",
                "Hazardous spatial proximity reducing driver safe stopping buffer",
                "Potential intersection conflict or lane-merging congestion detected",
            ]
            if ped_count > 0:
                causes.append(f"Vulnerable road users ({ped_count} pedestrian(s)) detected in traffic corridor")
            
            recs = [
                "Reduce vehicle speed immediately and increase headway distance to at least 3-4 seconds",
                "Maintain lane discipline and avoid abrupt overtaking or aggressive maneuvering",
                "Scan ahead for sudden braking waves or pedestrian movements",
                "Ensure headlights/fog lamps are active if visibility is compromised"
            ]
        elif risk_name == 'Moderate Risk':
            causes = [
                f"Moderate vehicle density ({density}) requiring heightened situational awareness",
                "Intermittent road scene clutter or developing traffic bottleneck",
                "Variable following distances observed among nearby vehicles"
            ]
            recs = [
                "Maintain steady cruising speed and anticipate traffic signal or junction slowdowns",
                "Keep a safe 2-second following buffer from lead vehicles",
                "Avoid unnecessary mobile distractions and monitor blind spots"
            ]
        else: # Safe
            causes = [
                f"Unobstructed road corridor with smooth traffic flow ({density} traffic)",
                "Adequate sightlines and minimal proximity hazards identified",
                "No urgent road obstacle or pedestrian intrusion detected"
            ]
            recs = [
                "Proceed at designated speed limit while maintaining situational awareness",
                "Continue scanning mirrors and upcoming roadway geometry",
                "Enjoy safe driving and adhere to all posted traffic signals"
            ]

        return causes, recs

model_service = ModelService()
