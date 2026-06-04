from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "name": "GYMATHOME API"
    })

@app.route("/get-stream/<video_id>", methods=["GET"])
def get_stream(video_id):
    return jsonify({
        "status": "teste-ok",
        "videoId": video_id,
        "streamUrl": "https://alhofamilygym.netlify.app/videos/test.mp4"
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)