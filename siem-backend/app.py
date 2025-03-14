from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

# Store logs and alerts in memory (for now)
logs = []
alerts = []

@app.route('/log', methods=['POST'])
def log_event():
    data = request.json
    data['timestamp'] = datetime.datetime.utcnow().isoformat()
    logs.append(data)
    
    # Basic threat detection
    if 'ignore previous instructions' in data.get('input', '').lower():
        alerts.append({
            'type': 'Prompt Injection Attempt',
            'timestamp': data['timestamp'],
            'input': data['input']
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