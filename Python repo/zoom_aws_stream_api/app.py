from flask import Flask, request, jsonify
from zoom_service import ZoomService
import os

app = Flask(__name__)

@app.route('/create_meeting', methods=['POST'])
def create_meeting():
    data = request.get_json()
    zoom_meeting_id = data.get('zoom_meeting_id', None)
    zoom_passcode = data.get('zoom_passcode', None)

    if not zoom_meeting_id or not zoom_passcode:
        return jsonify({"error": "Missing Zoom meeting ID or passcode"}), 400

    aws_access_key = os.getenv('AWS_ACCESS_KEY')
    aws_secret_key = os.getenv('AWS_SECRET_KEY')

    if not aws_access_key or not aws_secret_key:
        return jsonify({"error": "Missing AWS access key or secret key"}), 400

    zoom_service = ZoomService(zoom_meeting_id, zoom_passcode, aws_access_key, aws_secret_key)
    stream_details = zoom_service.create_meeting()

    if 'error' in stream_details:
        return jsonify(stream_details), 500

    return jsonify(stream_details), 200

if __name__ == '__main__':
    app.run(debug=True)