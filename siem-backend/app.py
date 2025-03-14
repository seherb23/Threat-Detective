from flask import Flask, request, jsonify
import time
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/logs": {"origins": "http://localhost:3000"}})

# Store logs and alerts in memory (for now)
logs = []
alerts = []

# app.config['JWT_SECRET_KEY'] = '12345678'
# jwt = JWTManager(app)

# @app.route('/protected', methods=['GET'])
# @jwt_required()
# def protected():
#     return jsonify({"message": "You are authorized"}), 200

@app.route('/log', methods=['POST'])
def log_event():
    data = request.json
    data['timestamp'] = time.time()
    logs.append(data)
    
    # Basic threat detection
    if 'ignore previous instructions' in data.get('input', '').lower():
        alerts.append({
            'type': 'Prompt Injection Attempt',
            'timestamp': data['timestamp'],
            'input': data['input']
        })
    
    if len(data['response']) > 500 or "password" in data['response']:
        alerts.append({
            'type': 'Data Exfiltration Attempt',
            'timestamp': data['timestamp'],
            'response': data['response']
        })
    
    return jsonify({"status": "logged"}), 200

@app.route('/logs', methods=['GET'])
def get_logs():
    return jsonify(logs), 200

@app.route('/alerts', methods=['GET'])
def get_alerts():
    return jsonify(alerts), 200

if __name__ == '__main__':
    app.run(debug=True)