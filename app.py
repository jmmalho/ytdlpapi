from flask import Flask, jsonify
import yt_dlp
import os

app = Flask(__name__)


@app.route("/debug")
def debug():
    cookies_file = "cookies.txt"

    return jsonify({
        "cookies_exists": os.path.exists(cookies_file),
        "cookies_path": os.path.abspath(cookies_file),
        "files": os.listdir(".")
    })


@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "name": "GYMATHOME API"
    })


@app.route("/get-stream/<video_id>", methods=["GET"])
def get_stream(video_id):
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"
    cookies_file = "cookies.txt"

    ydl_opts = {
        "format": "18/22/best",
        "quiet": True,
        "no_warnings": True,
        "extractor_args": {
            "youtube": {
                "player_client": ["web"]
            }
        }
    }

    if os.path.exists(cookies_file):
        print("Cookies encontrados:", os.path.abspath(cookies_file))
        ydl_opts["cookiefile"] = os.path.abspath(cookies_file)
    else:
        print("ERRO: cookies.txt não encontrado")
        print("Ficheiros na raiz:", os.listdir("."))

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)

        stream_url = info.get("url")

        if stream_url:
            return jsonify({
                "status": "success",
                "videoId": video_id,
                "title": info.get("title"),
                "formatId": info.get("format_id"),
                "ext": info.get("ext"),
                "height": info.get("height"),
                "protocol": info.get("protocol"),
                "formatNote": info.get("format_note"),
                "streamUrl": stream_url
            })

        formats = info.get("formats", [])

        playable_formats = [
            f for f in formats
            if f.get("url")
            and f.get("vcodec") != "none"
            and f.get("acodec") != "none"
        ]

        if not playable_formats:
            return jsonify({
                "status": "error",
                "message": "Nenhum formato direto com vídeo + áudio disponível.",
                "availableFormats": [
                    {
                        "format_id": f.get("format_id"),
                        "ext": f.get("ext"),
                        "height": f.get("height"),
                        "vcodec": f.get("vcodec"),
                        "acodec": f.get("acodec"),
                        "protocol": f.get("protocol")
                    }
                    for f in formats
                ]
            }), 400

        best_format = sorted(
            playable_formats,
            key=lambda f: f.get("height") or 0,
            reverse=True
        )[0]

        return jsonify({
            "status": "success",
            "videoId": video_id,
            "title": info.get("title"),
            "formatId": best_format.get("format_id"),
            "ext": best_format.get("ext"),
            "height": best_format.get("height"),
            "protocol": best_format.get("protocol"),
            "formatNote": best_format.get("format_note"),
            "streamUrl": best_format.get("url")
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400


if __name__ == "__main__":
    app.run(debug=True, port=5000)
