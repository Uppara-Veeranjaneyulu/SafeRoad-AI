import os
import sys

# Ensure backend root and project root are in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Set working directory to project root so models and results paths always resolve
os.chdir(project_root)

from flask import Flask, jsonify
from flask_cors import CORS

from routes.predict import predict_bp
from routes.models import models_bp
from routes.stats import stats_bp

app = Flask(__name__)
# Enable CORS for all routes (allows Vite frontend at localhost:5173 to connect)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Register blueprints
app.register_blueprint(predict_bp, url_prefix='/api')
app.register_blueprint(models_bp, url_prefix='/api')
app.register_blueprint(stats_bp, url_prefix='/api')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'online',
        'service': 'SafeRoad AI Backend',
        'version': '1.0.0',
        'message': 'Road Scene Risk Classification & YOLOv8 Traffic Monitoring API is active'
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting SafeRoad AI Backend on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False)
