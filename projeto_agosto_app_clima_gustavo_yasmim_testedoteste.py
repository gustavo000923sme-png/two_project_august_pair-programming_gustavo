import io
import random
import threading
import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from faker import Faker
from datetime import datetime, timezone, timedelta

API_KEY = "6f1e6fc120b7363a69229808e49eea48"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

fake = Faker('pt_BR')

COLOR_AZUL_ESC = "#1e293b"
COLOR_AZUL_MED = "#334155"
COLOR_AZUL_CLA = "#0284c7"
COLOR_VERDE    = "#16a34a"
COLOR_AMARELO  = "#fde047"
COLOR_ACO      = "#0f172a"

URL_CAPA = "https://i.pinimg.com/736x/20/0c/81/200c81c51c0eb0ce5d314af4c0ef2dd5.jpg"

imagens_cache = {}

def carregar_foto_url(url, largura, altura):
    if url in imagens_cache:
        return imagens_cache[url]
    
    try:
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
        return "#0f172a", "#ffffff"
    elif 11 <= temperatura <= 18:
        return "#1e293b", "#ffffff"
    else:
        return "#0284c7", "#ffffff"

def formatar_horario(timestamp_utc, fuso_segundos):
    fuso = timezone(timedelta(seconds=fuso_segundos))
    data_hora = datetime.fromtimestamp(timestamp_utc, tz=fuso)
    return data_hora.strftime("%H:%M")

def _executar_busca(cidade):
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

            url_icone_clima = f"https://openweathermap.org/img/wn/{icone_codigo}@2x.png"
            foto_icone = carregar_foto_url(url_icone_clima, 80, 80)
            
            def atualizar_ui():
                if foto_icone:
                    canvas.itemconfig(item_icone, image=foto_icone)
                    canvas.foto_icone_ref = foto_icone

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
                botao_buscar.config(state="normal", text="Buscar Clima")

            janela.after(0, atualizar_ui)

        elif resposta.status_code == 401:
            janela.after(0, lambda: exibir_erro("Chave de API inválida ou ainda não ativada."))
        else:
            janela.after(0, lambda: exibir_erro(f"Cidade '{cidade}' não encontrada!"))

    except requests.exceptions.RequestException:
        janela.after(0, lambda: exibir_erro("Não foi possível conectar à internet."))

def exibir_erro(mensagem):
    label_resultado.config(
        text=f"❌ {mensagem}", 
        bg="#7f1d1d", 
        fg="#ffffff"
    )
    botao_buscar.config(state="normal", text="Buscar Clima")

def buscar_clima():
    cidade = entry_cidade.get().strip()
    if not cidade:
        messagebox.showwarning("Aviso", "Por favor, digite o nome de uma cidade.")
        return

    botao_buscar.config(state="disabled", text="Buscando...")
    label_resultado.config(text="Carregando informações...", bg=COLOR_AZUL_ESC, fg="#ffffff")

    threading.Thread(target=_executar_busca, args=(cidade,), daemon=True).start()

def gerar_cidade_aleatoria():
    cidades_teste = ["Sao Paulo, BR", "Moscow, RU", "London, UK", "Tokyo, JP"]
    cidade_escolhida = random.choice(cidades_teste) if random.choice([True, False]) else fake.city()

    entry_cidade.delete(0, tk.END)
    entry_cidade.insert(0, cidade_escolhida)
    buscar_clima()

janela = tk.Tk()
janela.title("App de Clima - Vocação")
janela.geometry("450x600")

canvas = tk.Canvas(janela, width=450, height=600, highlightthickness=0)
canvas.pack(fill="both", expand=True)

foto_fundo = carregar_foto_url(URL_CAPA, 450, 600)
if foto_fundo:
    canvas.create_image(0, 0, image=foto_fundo, anchor="nw")
    canvas.foto_fundo_ref = foto_fundo

item_icone = canvas.create_image(225, 290, anchor="center")

label_instrucao = tk.Label(
    janela, 
    text="Digite a cidade:", 
    font=("Segoe UI", 11, "bold"), 
    bg=COLOR_AZUL_ESC, 
    fg="#ffffff"
)
label_instrucao.place(relx=0.5, y=35, anchor="center")

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
entry_cidade.place(relx=0.5, y=75, anchor="center")
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
botao_buscar.place(relx=0.5, y=115, anchor="center")

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
botao_fake.place(relx=0.5, y=155, anchor="center")

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
label_resultado.place(relx=0.5, y=450, anchor="center")

janela.mainloop()