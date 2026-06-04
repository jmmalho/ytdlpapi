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
    # Constrói a URL do YouTube com o ID dinâmico recebido na rota
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"
    
    # Nome do ficheiro de cookies que guardaste na raiz do projeto
    cookies_file = 'cookies.txt'
    
    # Configurações otimizadas para o yt-dlp
    ydl_opts = {
        "format": "best[height<=720]/best",
        "quiet": True,
        "no_warnings": True,
        "extractor_args": {
            "youtube": {
                "player_client": ["web", "android"]
            }
        }
    }
    
    # Verifica se o ficheiro cookies.txt existe antes de o tentar usar
    if os.path.exists(cookies_file):
        print("Cookies encontrados:", os.path.abspath(cookies_file))
        ydl_opts['cookiefile'] = os.path.abspath(cookies_file)
    else:
        print("ERRO: cookies.txt não encontrado")

        
        print("Ficheiros na raiz:", os.listdir("."))

    try:
        # Usa o yt-dlp para extrair a informação sem transferir o ficheiro de vídeo
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            
            # Extrai os dados necessários do dicionário retornado pelo yt-dlp
            stream_url = info.get('url')
            video_title = info.get('title')
            
            return jsonify({
                "status": "success",
                "videoId": video_id,
                "title": video_title,
                "streamUrl": stream_url
            })
            
    except Exception as e:
        # Se o YouTube bloquear ou o ID for inválido, devolve o erro amigavelmente
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

if __name__ == "__main__":
    # Roda localmente na porta 5000 (o Render ignora esta linha e usa a porta dele em produção)
    app.run(debug=True, port=5000)