from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)

def analyze_risk():
    hour = datetime.datetime.now().hour
    return hour > 22

@app.route('/sos', methods=['POST'])
def sos():
    data = request.json
    message = data.get("message", "Help needed!")

    if analyze_risk():
        message = "🚨 HIGH RISK! " + message

    return jsonify({
        "status": "SOS sent",
        "message": message
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
