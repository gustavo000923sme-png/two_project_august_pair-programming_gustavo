'''
Objetivo: Apresentar a história da primeira grande 
investidora brasileira usando uma interface gráfica simples (tkinter).

Conceitos: História financeira do Brasil, diversificação 
internacional no século XIX, interfaces visuais (GUI).

COLOR_AZUL_ESC = "#004d6e"  # AE (Fundo da tela)
COLOR_AZUL_MED = "#0081ab"  # AM (Bordas e detalhes)
COLOR_AZUL_CLA = "#00b1cd"  # AC (Destaque do texto da senha)
COLOR_VERDE    = "#a6c844"  # V  (Botão Principal / Gerar)
COLOR_ROSA     = "#b83764"  # R  (Acentos e alertas de erro)
COLOR_AMARELO  = "#edce01"  # A  (Botão Copiar / Destaque)
COLOR_ACO      = "#4a3336"  # B  (Fundo dos campos e cards)

'''
import io
import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk


# 1. Função que exibe a mensagem do evento
def mostrar_fato(detalhe):
    # messagebox.showinfo("Fato Histórico", detalhe)
    messagebox.showinfo("Curiosidade Eufrasia", detalhe)


# 2. Configuração da Janela Principal
janela = tk.Tk()
janela.title("História Financeira: Eufrásia Teixeira Leite")
# janela.geometry("500x580")  # Ajustado o tamanho da tela
janela.geometry("500x580")  # Ajustado o tamanho da tela
janela.configure(bg="#f4f4f9")

# 3. Título e Subtítulo
lbl_titulo = tk.Label(
    janela,
    text="Eufrásia Teixeira Leite",
    font=("Times New Roman", 26, "bold"),
    bg="#f4f4f9",
    fg="#1b365d",
)
lbl_titulo.pack(pady=7)
# lbl_titulo.pack(pady=120)

lbl_subtitulo = tk.Label(
    janela,
    text="A primeira investidora global do Brasil",
    font=("Arial", 10, "italic"),
    bg="#f4f4f9",
)
lbl_subtitulo.pack(pady=2)

# 4. Carregando Imagem da Internet
url_imagem = "https://upload.wikimedia.org/wikipedia/commons/4/40/Eufr%C3%A1sia_Teixeira_Leite_aos_30_anos_%282%29.jpg"
# url_imagem = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Tarsila_do_Amaral%2C_ca._1925.jpg/960px-Tarsila_do_Amaral%2C_ca._1925.jpg"

# Criando variável global da foto para o Tkinter não apagar da memória
foto_eufrasia = None

try:
    # Headers para simular um navegador comum (evita bloqueios)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    resposta = requests.get(url_imagem, headers=headers, timeout=5)
    resposta.raise_for_status()  # Confirma que o download deu certo (status 200)

    dados_imagem = resposta.content

    # Processando a imagem com Pillow
    imagem_pil = Image.open(io.BytesIO(dados_imagem))
    imagem_pil = imagem_pil.resize(
        (130, 160), Image.Resampling.LANCZOS
    )  # Redimensiona

    foto_eufrasia = ImageTk.PhotoImage(imagem_pil)

    # Exibindo no Label
    lbl_imagem = tk.Label(janela, image=foto_eufrasia, bg="#f4f4f9")
    lbl_imagem.image = foto_eufrasia  # Guarda a referência da imagem
    lbl_imagem.pack(pady=10)

except Exception as erro:
    # Caso aconteça algum problema de conexão, exibe um aviso em texto na tela
    print(f"Erro ao carregar imagem: {erro}")
    lbl_erro = tk.Label(
        janela,
        text="[Foto de Eufrásia Teixeira Leite - Indisponível sem internet]",
        font=("Arial", 9, "italic"),
        fg="gray",
        bg="#f4f4f9",
    )
    lbl_erro.pack(pady=10)

# 5. Dados da Linha do Tempo (Dicionário)
eventos = {
    "1850 - Nascimento": "Nasceu em Vassouras (RJ), no auge do ciclo do café.",
    "1872 - Herança & Europa": "Após perder os pais, mudou-se para Paris e assumiu a gestão da fortuna da família.",
    "1873-1930 - Carteira Global": "Investiu em títulos, ações e ferrovias em 13 países e 7 moedas diferentes.",
    "1930 - Legado": "Faleceu deixando sua fortuna para causas sociais e educacionais no Brasil.",
    # herança, relacionamento.
}

# 6. Criação dos Botões
for data, detalhe in eventos.items():
    btn = tk.Button(
        janela,
        text=data,
        font=("Arial", 10, "bold"),
        bg="#1b365d",
        fg="white",
        relief="raised",
        command=lambda d=detalhe: mostrar_fato(d),
    )
    btn.pack(fill="x", padx=40, pady=6)

# 7. Loop Principal
janela.mainloop()