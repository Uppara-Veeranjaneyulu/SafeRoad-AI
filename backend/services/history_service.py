import os
import json
import time
from datetime import datetime

class HistoryService:
    def __init__(self, storage_file='backend/data/prediction_history.json'):
        self.storage_file = storage_file
        os.makedirs(os.path.dirname(storage_file), exist_ok=True)
        self.history = self._load()

    def _load(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def _save(self):
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            print(f"[HistoryService] Save error: {e}")

    def add_record(self, record):
        """Adds a prediction record to history and updates persistent storage."""
        rec_id = f"PR-{len(self.history) + 1:04d}"
        entry = {
            'id': rec_id,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'time_ago': 'Just now',
            **record
        }
        self.history.insert(0, entry) # Most recent first
        # Keep last 500 records
        if len(self.history) > 500:
            self.history = self.history[:500]
        self._save()
        return entry

    def get_history(self, limit=50):
        return self.history[:limit]

    def get_stats(self):
        total = len(self.history)
        if total == 0:
            return {
                'totalPredictions': 0,
                'totalImages': 6949,
                'avgConfidence': 94.5,
                'riskDistribution': {'Safe': 0, 'Moderate Risk': 0, 'High Risk': 0},
                'trafficDistribution': {'Light': 0, 'Moderate': 0, 'Heavy': 0, 'Very Heavy': 0},
                'latestPrediction': {
                    'risk': 'Safe',
                    'confidence': 95.0,
                    'timestamp': 'No predictions yet'
                }
            }

        confidences = [r.get('confidence', 0) for r in self.history]
        avg_conf = round(sum(confidences) / len(confidences), 1)

        risk_dist = {'Safe': 0, 'Moderate Risk': 0, 'High Risk': 0}
        traffic_dist = {'Light': 0, 'Moderate': 0, 'Heavy': 0, 'Very Heavy': 0}

        for r in self.history:
            risk = r.get('risk', 'Safe')
            traffic = r.get('trafficDensity', 'Light')
            if risk in risk_dist:
                risk_dist[risk] += 1
            if traffic in traffic_dist:
                traffic_dist[traffic] += 1

        latest = self.history[0] if self.history else None

        return {
            'totalPredictions': total,
            'totalImages': 6949 + total,
            'avgConfidence': avg_conf,
            'riskDistribution': risk_dist,
            'trafficDistribution': traffic_dist,
            'latestPrediction': {
                'risk': latest.get('risk', 'Safe') if latest else 'Safe',
                'confidence': latest.get('confidence', 95.0) if latest else 95.0,
                'timestamp': latest.get('time_ago', 'Recently') if latest else 'Recently'
            }
        }

history_service = HistoryService()
