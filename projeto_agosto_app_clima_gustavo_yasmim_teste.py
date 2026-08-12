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

# --- PALETA DE CORES ---
COLOR_AZUL_ESC = "#004d6e"
COLOR_AZUL_MED = "#0081ab"
COLOR_AZUL_CLA = "#00b1cd"
COLOR_VERDE    = "#a6c844"
COLOR_AMARELO  = "#edce01"
COLOR_ACO      = "#4a3336"

# LINK DIRETO DE TESTE (Céu com nuvens via Unsplash)
URL_CAPA = "https://images.unsplash.com/photo-1513002749550-c59d786b8e6c?w=600&auto=format&fit=crop"

imagens_cache = {}

def carregar_foto_url(url, largura, altura):
    """Baixa a imagem da web simulando um navegador para evitar bloqueios."""
    if url in imagens_cache:
        return imagens_cache[url]
    
    try:
        # Cabeçalho completo para evitar que servidores (como Imgur) bloqueiem o Python
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'
        }
        resposta = requests.get(url, headers=headers, timeout=5)
        resposta.raise_for_status()
        
        imagem_dados = io.BytesIO(resposta.content)
        imagem_pil = Image.open(imagem_dados)
        imagem_pil = imagem_pil.resize((largura, altura), Image.Resampling.LANCZOS)
        
        foto_tk = ImageTk.PhotoImage(imagem_pil)
        imagens_cache[url] = foto_tk
        return foto_tk
    except Exception as e:
        print(f"Aviso: Não foi possível carregar a imagem da URL ({e})")
        return None

def obter_cor_temperatura(temperatura):
    if temperatura <= 10:
        return COLOR_AZUL_ESC, "#ffffff"
    elif 11 <= temperatura <= 18:
        return COLOR_AZUL_MED, "#ffffff"
    else:
        return COLOR_AZUL_CLA, COLOR_ACO

def formatar_horario(timestamp_utc, fuso_segundos):
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
            icone_codigo = dados["weather"][0]["icon"]
            vento = int(dados["wind"]["speed"] * 3.6)
            pais = dados["sys"].get("country", "")

            temp_min = int(dados["main"]["temp_min"])
            temp_max = int(dados["main"]["temp_max"])
            fuso_segundos = dados.get("timezone", 0)
            nascer_sol = formatar_horario(dados["sys"]["sunrise"], fuso_segundos)
            por_sol = formatar_horario(dados["sys"]["sunset"], fuso_segundos)

            # Baixar e exibir o ícone do clima correspondente
            url_icone_clima = f"https://openweathermap.org/img/wn/{icone_codigo}@2x.png"
            foto_icone = carregar_foto_url(url_icone_clima, 70, 70)
            if foto_icone:
                label_icone.config(image=foto_icone)
                label_icone.image = foto_icone

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
            messagebox.showerror("Erro 401", "Chave de API inválida ou ainda não ativada.")
        else:
            messagebox.showerror("Erro", f"Cidade '{cidade}' não encontrada!")

    except requests.exceptions.RequestException:
        messagebox.showerror("Erro de Conexão", "Não foi possível conectar à internet.")

def gerar_cidade_aleatoria():
    cidades_teste = ["Sao Paulo, BR", "Moscow, RU", "London, UK", "Tokyo, JP"]
    cidade_escolhida = random.choice(cidades_teste) if random.choice([True, False]) else fake.city()

    entry_cidade.delete(0, tk.END)
    entry_cidade.insert(0, cidade_escolhida)
    buscar_clima()

# --- Interface Gráfica Centralizada ---
janela = tk.Tk()
janela.title("App de Clima - Layout Centralizado")
janela.geometry("450x600")

# 1. IMAGEM DE FUNDO
label_fundo = tk.Label(janela, bg=COLOR_AZUL_ESC)
label_fundo.place(x=0, y=0, relwidth=1, relheight=1)

foto_fundo = carregar_foto_url(URL_CAPA, 450, 600)
if foto_fundo:
    label_fundo.config(image=foto_fundo)
    label_fundo.image = foto_fundo  # Mantém a referência da imagem salva na memória

# 2. CONTROLES DA INTERFACE
label_instrucao = tk.Label(
    janela, 
    text="Digite a cidade:", 
    font=("Segoe UI", 11, "bold"), 
    bg=COLOR_AZUL_ESC, 
    fg="#ffffff"
)
label_instrucao.pack(pady=(25, 5))

entry_cidade = tk.Entry(
    janela, 
    font=("Segoe UI", 11), 
    width=28, 
    bg="#ffffff", 
    fg=COLOR_ACO,
    relief="flat",
    highlightthickness=2,
    highlightbackground=COLOR_AZUL_MED,
    highlightcolor=COLOR_AZUL_CLA,
    justify="center"
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
    relief="flat",
    cursor="hand2",
    padx=15
)
botao_buscar.pack(pady=5)

botao_fake = tk.Button(
    janela, 
    text="🎲 Sortear Cidade", 
    command=gerar_cidade_aleatoria, 
    bg=COLOR_AZUL_CLA, 
    fg="#ffffff", 
    font=("Segoe UI", 9, "bold"),
    relief="flat",
    cursor="hand2",
    padx=15
)
botao_fake.pack(pady=5)

# Label para exibir o ícone do clima
label_icone = tk.Label(janela, bg=COLOR_AZUL_ESC)
label_icone.pack(pady=(10, 0))

label_resultado = tk.Label(
    janela, 
    text="", 
    font=("Segoe UI", 10, "bold"), 
    justify="left", 
    wraplength=380, 
    bg=COLOR_AZUL_ESC, 
    fg=COLOR_AMARELO, 
    padx=15, 
    pady=12,
    relief="ridge",
    bd=2
)
label_resultado.pack(pady=10)

janela.mainloop()