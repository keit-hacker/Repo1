from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

# In-memory storage for received data
received_data = []

@app.route('/receive', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Add timestamp to the received data
        data['timestamp'] = datetime.now().isoformat()
        received_data.append(data)
        
        # Save to file for persistence
        save_data_to_file()
        
        return jsonify({
            "message": "Data received successfully",
            "received_data": data
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(received_data), 200

def save_data_to_file():
    """Save received data to a JSON file"""
    with open('received_data.json', 'w') as f:
        json.dump(received_data, f, indent=2)

def load_data_from_file():
    """Load previously saved data from JSON file"""
    global received_data
    if os.path.exists('received_data.json'):
        with open('received_data.json', 'r') as f:
            received_data = json.load(f)

if __name__ == '__main__':
    # Load any previously saved data
    load_data_from_file()
    
    # Run the server
    app.run(host='0.0.0.0', port=5000, debug=True) 