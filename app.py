from flask import Flask, jsonify
import yt_dlp
import os

app = Flask(__name__)

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
        'format': 'best',  # Escolhe o melhor formato disponível (vídeo + áudio juntos)
        'quiet': True,     # Evita encher os logs do Render com texto desnecessário
        'no_warnings': True
    }
    
    # Verifica se o ficheiro cookies.txt existe antes de o tentar usar
    if os.path.exists(cookies_file):
        ydl_opts['cookiefile'] = cookies_file
    else:
        # Se não existir, a API ainda tenta rodar, mas avisa no terminal/logs
        print(f"Aviso: O ficheiro '{cookies_file}' não foi encontrado na raiz. A tentar sem cookies...")

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