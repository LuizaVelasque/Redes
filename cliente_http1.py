import requests
import time

arquivos = ["1mb.bin", "10mb.bin", "100mb.bin"]
url_base = "http://localhost:5000/"

for arquivo in arquivos:
    inicio = time.time()
    resposta = requests.get(url_base + arquivo)
    fim = time.time()
    print(f"Arquivo: {arquivo} | Tempo: {fim - inicio:.2f} segundos | Status: {resposta.status_code}")
