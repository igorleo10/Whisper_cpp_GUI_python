import os
import ssl
import subprocess
from pytube import YouTube
from whispercpp import Whisper
import tkinter as tk

# Ignorar erros de verificação de certificado SSL
ssl._create_default_https_context = ssl._create_unverified_context

# Função para baixar o áudio, transcrevê-lo e salvar a transcrição em um arquivo de texto
def execute(url):
    # Baixar o vídeo do YouTube em mp4
    yt = YouTube(url)

    # Define o nome do arquivo de saída
    output = os.path.join(".", f"audio.mp4")

    # Baixa o áudio do vídeo e salva no arquivo de saída
    audio = yt.streams.filter(only_audio=True).first()
    audio.download(output_path='.', filename='audio.mp4')

    # Converte o arquivo de áudio para o formato desejado
    wav_path = os.path.join(".", f"audio.wav")
    subprocess.run(["ffmpeg", "-i", "audio.mp4", "-ar", "16000", "-ac", "1", "-sample_fmt", "s16", wav_path], check=True)

    # Remove o arquivo de áudio original
    os.remove(output)

    # Transcrever o arquivo de áudio wav
    w = Whisper.from_pretrained("base.en")
    text = w.transcribe_from_file(wav_path)

    # Verificar se o arquivo já existe na pasta e adicionar um número ao nome do arquivo, se necessário
    output_filename = "output.txt"
    if os.path.exists(output_filename):
        i = 1
        while True:
            new_output_filename = f"output_{i}.txt"
            if not os.path.exists(new_output_filename):
                output_filename = new_output_filename
                break
            i += 1

    # Escrever o texto no arquivo de saída
    with open(output_filename, "w") as f:
        f.write(text)

    os.remove(wav_path)

    print(f"Transcrição salva em {output_filename}")

# Criar a janela principal
window = tk.Tk()

# Criar a etiqueta "Youtube URL"
url_label = tk.Label(window, text="Youtube URL:")
url_label.grid(row=0, column=0, sticky="w")

# Criar a entrada para a URL
url_entry = tk.Entry(window)
url_entry.grid(row=0, column=1, sticky="we")

# Criar o botão "Executar"
execute_button = tk.Button(window, text="Executar")
execute_button.grid(row=0, column=2, sticky="e")

# Criar o botão "Limpar"
clear_button = tk.Button(window, text="Limpar")
clear_button.grid(row=0, column=3, sticky="e")

# Função para chamar a função execute() com a URL inserida pelo usuário
def on_execute_button_click():
    # Obter a URL inserida pelo usuário
    url = url_entry.get()
    # Executar a função execute() com a URL
    execute(url)

# Associar a função on_execute_button_click() com o botão "Executar"
execute_button.config(command=on_execute_button_click)

# Função para limpar a URL inserida pelo usuário
def on_clear_button_click():
    # Limpar a entrada da URL
    url_entry.delete(0, tk.END)

# Associar a função on_clear_button_click() com o botão "Limpar"
clear_button.config(command=on_clear_button_click)

# Configurar a geometria do grid para permitir que a janela se expanda
window.grid_columnconfigure(1, weight=1)
window.grid_rowconfigure(0, weight=1)

# Iniciar a janela principal
window.mainloop()