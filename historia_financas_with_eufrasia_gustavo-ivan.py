import io
import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTK


COLOR_AZUL_ESC = "#004d6e" # AE (Fundo da tela)
COLOR_AZUL_MED = "#0081ab" # AM (Bordas e detalhes)
COLOR_AZUL_CLA = "#00b1cd" # AC (Destaque do texto da senha)
COLOR_VERDE    = "#a6c844" # V  (Botão Principal / Gerar)
COLOR_ROSA     = "#b83764" # R  (Acentos e alert as de erro)
COLOR_AMARELO  = "#edce01" # A  (Botão Copiar / Destaque)
COLOR_ACO      = "#4a3336" # B  (Fundo dos campos e cards)

def mostrar_fato(detalhe):
    messagebox.showinfo("Curiosidade Eufrasia", detalhe)


janela = tk.Tk()
janela.title("História Financeira: Eufrásia Teixeira Leite")
janela.geometry("500x580")  # Ajustado o tamanho da tela
janela.configure(bg="#f4f4f9")

lbl_titulo = tk.Label(
    janela,
    text="Eufrásia Teixeira Leite",
    font=("Times New Roman", 26, "bold"),
    bg="#f4f4f9",
    fg="#1b365d"
)
lbl_titulo.pack(pady=7)

lbl_subtitulo = tk.Label(
    janela,
    text="A primeira investidora global do Brasil",
    font=("Arial", 10, "italic"),
    bg="#f4f4f9"
)
lbl_subtitulo.pack(pady=2)

url_imagem = "https://upload.wikimedia.org/wikipedia/commons/4/40/Eufr%C3%A1sia_Teixeira_Leite_aos_30_anos_%282%29.jpg"

foto_eufrasia = None 

try:
     headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    resposta = requests.get(url_imagem, headers=headers, timeout=5)
    resposta.raise_for_status()

    dados_imagem = resposta.content

    imagem_pill = Image.open(io.BytesIO(dados_imagem))
    imagem_pill = imagem_pill.resize(
            (130, 160), Image.Resampling.LANCZOS
    )

    foto_eufrasia = ImageTk.PhotoImage(imagem_pill)

    lbl_imagem = tk.Label(janela, image=foto_eufrasia, bg="#f4f4f9")
    lbl_imagem.imagem = foto_eufrasia
    lbl_imagem.pack(pady=10)

except Exception as erro:
    print(f"Erro ao carregar imagem: {erro}")
    lbl_erro = tk.Label(
            janela,
            text="[Foto de Eufrásia Teixeira Leite - Indisponível sem internet]",
            font=("Arial", 9, "italic"),
            fg="gray",
            bg="#f4f4f9",
        )
    lbl_erro.pack(pady=10)

    eventos = {
    "1850 - Nascimento": "Nasceu em Vassouras (RJ), no auge do café",
    "1872 - Herança & Europa": "Após perder os pais, mudou-se para paris e assumiu a gestão da fortuna  da família.",
    "1873-1930 - Carteira global": "Investiu em títulos, ações e ferrovias em 13 países e 7 moedas diferentes",
    "1930 - Legado": "Faleceu deixando sua fortuna para causas sociais e educacionais no Brasil.",
    "Curiosidade": "O tempo que levou para fazer o inventário de sua fortuna foi de 22 anos (de 1930 a 1952)",
    "Legado" : "Eufrásia quase não casou e não teve filhos, o homem que quase casou com ela foi o Joaquim Nabuco.",
}


for data, detalhe in eventos.items():
    btn = tk.Button(
        janela,
        text=data,
        font=("Arial", 11),
        bg="#0081ab",
        fg="white",
        relief="flat",
        command=lambda d=detalhe: mostrar_fato(d)
    )
    btn.pack(fill="x", padx=40, pady=6)

janela.mainloop()