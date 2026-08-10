import io
import random
import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from faker import Faker
from datetime import datetime, timezone, timedelta

# Configuração da API OpenWeather
API_KEY = "6f1e6fc120b7363a69229808e49eea48"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

fake = Faker('pt_BR')

# --- PALETA DE CORES DEFINIDA ---
COLOR_AZUL_ESC = "#004d6e"  # Frio Extremo / Header
COLOR_AZUL_MED = "#0081ab"  # Frio Moderado / Bordas
COLOR_AZUL_CLA = "#00b1cd"  # Agradável / Destaques
COLOR_VERDE    = "#a6c844"  # Botão Sucesso
COLOR_ROSA     = "#b83764"  # Alertas
COLOR_AMARELO  = "#edce01"  # Calor / Destaque
COLOR_ACO      = "#4a3336"  # Texto Escuro

# Links das imagens do Pinterest
URL_CAPA  = "https://i.pinimg.com/564x/87/42/fa/8742fae96a40efb5ee2e3d30906e57df.jpg"
URL_NEVE  = "https://i.pinimg.com/564x/0a/aa/be/0aaabe63ec3e33c37568f2dd7cb8bb13.jpg"
URL_SOL   = "https://i.pinimg.com/564x/df/7e/fa/df7efa9a9a3b934b0bd9265f7253bd3c.jpg"
URL_CHUVA = "https://i.pinimg.com/564x/3b/b1/d1/3bb1d13fbe4e54e4dfdd01f464010378.jpg"

imagens_cache = {}

def carregar_foto_url(url):
    """Baixa e converte a imagem para o Tkinter no formato 500x500."""
    if url in imagens_cache:
        return imagens_cache[url]
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        resposta = requests.get(url, headers=headers, timeout=5)
        resposta.raise_for_status()
        
        imagem_dados = io.BytesIO(resposta.content)
        imagem_pil = Image.open(imagem_dados)
        imagem_pil = imagem_pil.resize((500, 500))
        
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

def obter_cor_temperatura(temperatura):
    """Muda a cor do quadro: mais escuro no frio e mais claro no calor."""
    if temperatura <= 10:
        return COLOR_AZUL_ESC, COLOR_AMARELO
    elif 11 <= temperatura <= 18:
        return COLOR_AZUL_MED, "#ffffff"
    elif 19 <= temperatura <= 25:
        return COLOR_AZUL_CLA, COLOR_ACO
    else:
        return COLOR_AMARELO, COLOR_ACO

def formatar_horario(timestamp_utc, fuso_segundos):
    """Converte o timestamp UTC para o horário local da cidade."""
    fuso = timezone(timedelta(seconds=fuso_segundos))
    data_hora = datetime.fromtimestamp(timestamp_utc, tz=fuso)
    return data_hora.strftime("%H:%M")

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
            vento = int(dados["wind"]["speed"] * 3.6)
            pais = dados["sys"].get("country", "")

            temp_min = int(dados["main"]["temp_min"])
            temp_max = int(dados["main"]["temp_max"])
            fuso_segundos = dados.get("timezone", 0)
            nascer_sol = formatar_horario(dados["sys"]["sunrise"], fuso_segundos)
            por_sol = formatar_horario(dados["sys"]["sunset"], fuso_segundos)

            trocar_fundo(temperatura, descricao)

            # Aplica a cor dinâmica baseada na temperatura
            cor_bg, cor_fg = obter_cor_temperatura(temperatura)
            label_resultado.config(bg=cor_bg, fg=cor_fg)

            resultado_texto = (
                f"Clima em {dados['name']}, {pais}:\n\n"
                f"🌡️ Temp: {temperatura}°C (Mín: {temp_min}°C | Máx: {temp_max}°C)\n"
                f"🔥 Sensação: {sensacao}°C\n"
                f"☁️ Condição: {descricao.capitalize()}\n"
                f"💧 Umidade: {umidade}%\n"
                f"💨 Vento: {vento} km/h\n"
                f"🌅 Nascer do Sol: {nascer_sol}\n"
                f"🌇 Pôr do Sol: {por_sol}"
            )
            label_resultado.config(text=resultado_texto)

        elif resposta.status_code == 401:
            messagebox.showerror("Erro de API", "A API Key está em processo de ativação. Aguarde um momento!")
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

# --- Interface Gráfica ---
janela = tk.Tk()
janela.title("App de Clima - Pair Programming")
janela.geometry("500x400")

label_fundo = tk.Label(janela, bg=COLOR_AZUL_ESC)
label_fundo.place(x=0, y=0, relwidth=1, relheight=1)

foto_capa = carregar_foto_url(URL_CAPA)
if foto_capa:
    label_fundo.config(image=foto_capa)

label_instrucao = tk.Label(
    janela, 
    text="Digite a cidade:", 
    font=("Segoe UI", 11, "bold"), 
    bg=COLOR_AZUL_ESC, 
    fg="#ffffff",
    padx=10, 
    pady=3
)
label_instrucao.pack(pady=(15, 5))

entry_cidade = tk.Entry(
    janela, 
    font=("Segoe UI", 11), 
    width=28, 
    bg="#ffffff", 
    fg=COLOR_ACO,
    relief="flat",
    highlightthickness=2,
    highlightbackground=COLOR_AZUL_MED,
    highlightcolor=COLOR_AZUL_CLA
)
entry_cidade.pack(pady=5)
entry_cidade.bind("<Return>", lambda event: buscar_clima())

botao_buscar = tk.Button(
    janela, 
    text="Buscar Clima", 
    command=buscar_clima, 
    bg=COLOR_VERDE, 
    fg="#ffffff", 
    font=("Segoe UI", 10, "bold"),
    activebackground=COLOR_AZUL_MED,
    relief="flat",
    cursor="hand2",
    padx=10
)
botao_buscar.pack(pady=5)

botao_fake = tk.Button(
    janela, 
    text="🎲 Sortear Cidade", 
    command=gerar_cidade_aleatoria, 
    bg=COLOR_AZUL_CLA, 
    fg="#ffffff", 
    font=("Segoe UI", 9, "bold"),
    activebackground=COLOR_AZUL_MED,
    relief="flat",
    cursor="hand2",
    padx=10
)
botao_fake.pack(pady=5)

label_resultado = tk.Label(
    janela, 
    text="", 
    font=("Segoe UI", 10, "bold"), 
    justify="left", 
    wraplength=440, 
    bg=COLOR_AZUL_ESC, 
    fg=COLOR_AMARELO, 
    padx=15, 
    pady=12,
    relief="ridge",
    bd=2
)
label_resultado.pack(pady=15)

janela.mainloop()