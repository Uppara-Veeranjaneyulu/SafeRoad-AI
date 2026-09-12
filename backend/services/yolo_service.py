import os
import cv2
import numpy as np
from PIL import Image

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False

class YOLOService:
    def __init__(self, model_weight='yolov8n.pt'):
        self.model = None
        self.model_weight = model_weight
        if YOLO_AVAILABLE:
            try:
                print(f"[YOLOv8] Initializing {model_weight}...")
                self.model = YOLO(model_weight)
                print(f"[YOLOv8] Successfully loaded {model_weight}")
            except Exception as e:
                print(f"[YOLOv8] Warning: Failed to load YOLOv8 model ({e}). Fallback to heuristic.")

    def analyze(self, image_np):
        """
        Runs YOLOv8 object detection on an RGB numpy image array.
        Returns detected object counts, vehicle count, pedestrian count, and traffic density level.
        """
        if self.model is None:
            # Fallback if YOLO model couldn't load
            return {
                'vehicle_count': 0,
                'pedestrian_count': 0,
                'objects': [],
                'traffic_density': 'Moderate'
            }

        try:
            # YOLO expects BGR or RGB array
            results = self.model.predict(image_np, conf=0.25, verbose=False)
            result = results[0]
            
            object_counts = {}
            vehicle_classes = {'car', 'truck', 'bus', 'motorcycle', 'bicycle'}
            pedestrian_classes = {'person'}
            
            vehicle_count = 0
            pedestrian_count = 0

            for box in result.boxes:
                cls_id = int(box.cls[0])
                cls_name = result.names.get(cls_id, f'class_{cls_id}').lower()
                object_counts[cls_name] = object_counts.get(cls_name, 0) + 1
                
                if cls_name in vehicle_classes:
                    vehicle_count += 1
                elif cls_name in pedestrian_classes:
                    pedestrian_count += 1

            # Format for frontend
            yolo_objects = [
                {'label': k.capitalize(), 'count': v}
                for k, v in object_counts.items()
            ]

            # Density classification
            if vehicle_count == 0:
                traffic_density = 'Light'
            elif vehicle_count <= 4:
                traffic_density = 'Light'
            elif vehicle_count <= 9:
                traffic_density = 'Moderate'
            elif vehicle_count <= 16:
                traffic_density = 'Heavy'
            else:
                traffic_density = 'Very Heavy'

            return {
                'vehicle_count': vehicle_count,
                'pedestrian_count': pedestrian_count,
                'objects': yolo_objects,
                'traffic_density': traffic_density
            }

        except Exception as e:
            print(f"[YOLOv8] Error during inference: {e}")
            return {
                'vehicle_count': 0,
                'pedestrian_count': 0,
                'objects': [],
                'traffic_density': 'Light'
            }

yolo_service = YOLOService()
