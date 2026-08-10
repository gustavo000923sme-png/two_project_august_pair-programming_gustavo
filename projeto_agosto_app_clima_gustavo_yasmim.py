import io
import random
import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from faker import Faker

# Configuração da API OpenWeather
API_KEY = "6f1e6fc120b7363a69229808e49eea48"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

fake = Faker('pt_BR')

# Links das imagens do Pinterest
URL_CAPA = "https://i.pinimg.com/564x/87/42/fa/8742fae96a40efb5ee2e3d30906e57df.jpg" # Foto inicial (Capa)
URL_NEVE = "https://i.pinimg.com/564x/0a/aa/be/0aaabe63ec3e33c37568f2dd7cb8bb13.jpg"
URL_SOL = "https://i.pinimg.com/564x/df/7e/fa/df7efa9a9a3b934b0bd9265f7253bd3c.jpg"
URL_CHUVA = "https://i.pinimg.com/564x/3b/b1/d1/3bb1d13fbe4e54e4dfdd01f464010378.jpg"

imagens_cache = {}

def carregar_foto_url(url):
    """Baixa e converte a imagem para o Tkinter."""
    if url in imagens_cache:
        return imagens_cache[url]
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        resposta = requests.get(url, headers=headers, timeout=5)
        resposta.raise_for_status()
        
        imagem_dados = io.BytesIO(resposta.content)
        imagem_pil = Image.open(imagem_dados)
        imagem_pil = imagem_pil.resize((400, 560))
        
        foto_tk = ImageTk.PhotoImage(imagem_pil)
        imagens_cache[url] = foto_tk
        return foto_tk
    except Exception:
        return None

def trocar_fundo(temperatura, descricao):
    """Troca a foto de fundo após a pesquisa de clima."""
    descricao = descricao.lower()
    
    if "rain" in descricao or "chuva" in descricao or "garoa" in descricao or "drizzle" in descricao:
        url_escolhida = URL_CHUVA
    elif temperatura <= 10 or "snow" in descricao or "neve" in descricao:
        url_escolhida = URL_NEVE
    else:
        url_escolhida = URL_SOL

    foto = carregar_foto_url(url_escolhida)
    if foto:
        label_fundo.config(image=foto)
        label_fundo.image = foto

def buscar_clima():
    cidade = entry_cidade.get().strip()
    if not cidade:
        messagebox.showwarning("Aviso", "Por favor, digite o nome de uma cidade.")
        return

    parametros = {
        'q': cidade,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'pt_br'
    }

    try:
        resposta = requests.get(BASE_URL, params=parametros, timeout=5)
        
        if resposta.status_code == 200:
            dados = resposta.json()

            temperatura = int(dados["main"]["temp"])
            sensacao = int(dados["main"]["feels_like"])
            umidade = dados["main"]["humidity"]
            descricao = dados["weather"][0]["description"]

            # Muda para a imagem correspondente ao clima da pesquisa
            trocar_fundo(temperatura, descricao)

            resultado_texto = (
                f"Clima em {dados['name']}:\n\n"
                f"🌡️ Temperatura: {temperatura}°C\n"
                f"🔥 Sensação: {sensacao}°C\n"
                f"☁️ Condição: {descricao.capitalize()}\n"
                f"💧 Umidade: {umidade}%"
            )
            label_resultado.config(text=resultado_texto)

        elif resposta.status_code == 401:
            messagebox.showerror("Erro de API", "A API Key da sua parceira ainda está em processo de ativação nos servidores. Aguarde mais um pouco!")
        else:
            messagebox.showerror("Erro", f"Cidade '{cidade}' não encontrada!")

    except requests.exceptions.RequestException:
        messagebox.showerror("Erro de Conexão", "Não foi possível conectar à internet.")

def gerar_cidade_aleatoria():
    cidades_teste = ["Moscow", "London", "Rio de Janeiro", "Tokyo", "Reykjavik"]
    
    if random.choice([True, False]):
        cidade_escolhida = fake.city()
    else:
        cidade_escolhida = random.choice(cidades_teste)

    entry_cidade.delete(0, tk.END)
    entry_cidade.insert(0, cidade_escolhida)
    buscar_clima()

# --- Interface Gráfica (Tkinter) ---
janela = tk.Tk()
janela.title("App de Clima - Pair Programming")
janela.geometry("400x560")

# Rótulo do fundo
label_fundo = tk.Label(janela, bg="#d1d1d1")
label_fundo.place(x=0, y=0, relwidth=1, relheight=1)

# Define a foto de capa (URL_CAPA) antes de qualquer busca
foto_capa = carregar_foto_url(URL_CAPA)
if foto_capa:
    label_fundo.config(image=foto_capa)

# Elementos da tela
label_instrucao = tk.Label(janela, text="Digite a cidade:", font=("Segoe UI", 11, "bold"), bg="#ffffff")
label_instrucao.pack(pady=(20, 5))

entry_cidade = tk.Entry(janela, font=("Segoe UI", 11), width=25)
entry_cidade.pack(pady=5)
entry_cidade.bind("<Return>", lambda event: buscar_clima())

botao_buscar = tk.Button(janela, text="Buscar Clima", command=buscar_clima, bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold"))
botao_buscar.pack(pady=5)

botao_fake = tk.Button(janela, text="🎲 Sortear Cidade", command=gerar_cidade_aleatoria, bg="#2196F3", fg="white", font=("Segoe UI", 9, "bold"))
botao_fake.pack(pady=5)

label_resultado = tk.Label(janela, text="", font=("Segoe UI", 11, "bold"), justify="left", wraplength=350, bg="#ffffff", padx=10, pady=10)
label_resultado.pack(pady=20)

janela.mainloop()