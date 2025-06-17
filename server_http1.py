from flask import Flask, send_file
import os

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

@app.route('/')
def index():
    return """
    <h1>Servidor HTTP/1.1 Rodando</h1>
    <p>Para baixar arquivos, acesse /1mb.bin, /10mb.bin ou /100mb.bin</p>
    """

@app.route('/<path:filename>')
def serve_file(filename):
    file_path = os.path.join(BASE_DIR, 'files', filename)
    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        return "Arquivo não encontrado", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
