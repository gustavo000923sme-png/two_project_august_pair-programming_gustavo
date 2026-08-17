'''
Objetivo: Aplicação completa em abas, com identidade visual inspirada na B3 (azul escuro e amarelo/dourado), incluindo controle de caixa, simulação de compra de Criptoativos e Extrato.

Conceitos: Componentes avançados (ttk.Notebook), gerenciamento de estado da aplicação, simulação de ativos digitais.

'''



import tkinter as tk
from tkinter import messagebox, ttk

# 1. Constantes e Variáveis Globais
COR_AZUL = "#001E62"
COR_AMARELO = "#F2A900"
COR_FUNDO = "#F5F5F5"

saldo = 1000.00
cripto_btc = 0.0
historico = ["Saldo inicial depositado: R$ 1000.00"]


# 2. Funções de Atualização da Interface
def atualizar_extrato():
    lst_extrato.delete(0, tk.END)
    for item in historico:
        lst_extrato.insert(tk.END, item)


def atualizar_tudo():
    lbl_saldo.config(text=f"Saldo Disponível: R$ {saldo:.2f}")
    lbl_btc.config(text=f"Seu Saldo BTC: {cripto_btc:.6f}")
    atualizar_extrato()


# 3. Funções das Operações Financeiras
def creditar():
    global saldo
    try:
        v = float(ent_valor_conta.get())
        if v <= 0:
            messagebox.showwarning("Aviso", "Digite um valor positivo.")
            return

        saldo += v
        historico.append(f"Depósito: +R$ {v:.2f}")
        ent_valor_conta.delete(0, tk.END)
        atualizar_tudo()
    except ValueError:
        messagebox.showerror("Erro", "Valor inválido.")


def debitar():
    global saldo
    try:
        v = float(ent_valor_conta.get())
        if v <= 0:
            messagebox.showwarning("Aviso", "Digite um valor positivo.")
            return

        if v <= saldo:
            saldo -= v
            historico.append(f"Saque/Pagamento: -R$ {v:.2f}")
            ent_valor_conta.delete(0, tk.END)
            atualizar_tudo()
        else:
            messagebox.showwarning("Erro", "Saldo insuficiente.")
    except ValueError:
        messagebox.showerror("Erro", "Valor inválido.")


def comprar_btc():
    global saldo, cripto_btc
    custo = 100.00
    if saldo >= custo:
        saldo -= custo
        qtd = custo / 300000.0
        cripto_btc += qtd
        historico.append(
            f"Compra Cripto: R$ 100.00 em BTC ({qtd:.6f} BTC)"
        )
        atualizar_tudo()
    else:
        messagebox.showwarning(
            "Erro", "Saldo insuficiente para comprar R$ 100,00 em BTC."
        )


# 4. Janela Principal e Estilos
janela = tk.Tk()
janela.title("Simulador Financeiro - Padrão B3")
janela.geometry("600x450")
janela.configure(bg=COR_FUNDO)

style = ttk.Style()
style.theme_use("default")
style.configure("TNotebook", background=COR_FUNDO)
style.configure(
    "TNotebook.Tab", background=COR_AZUL, foreground="white", padding=[10, 5]
)
style.map(
    "TNotebook.Tab",
    background=[("selected", COR_AMARELO)],
    foreground=[("selected", "black")],
)

# Header
header = tk.Frame(janela, bg=COR_AZUL, height=50)
header.pack(fill="x")
lbl_titulo = tk.Label(
    header,
    text="B3 - SIMULADOR EDUCACIONAL",
    font=("Arial", 14, "bold"),
    fg="white",
    bg=COR_AZUL,
)
lbl_titulo.pack(pady=10)

# Estrutura de Abas (Notebook)
notebook = ttk.Notebook(janela)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

aba_conta = ttk.Frame(notebook)
aba_cripto = ttk.Frame(notebook)
aba_extrato = ttk.Frame(notebook)

notebook.add(aba_conta, text="Conta Corrente")
notebook.add(aba_cripto, text="Criptoativos")
notebook.add(aba_extrato, text="Extrato")

# --- Montagem da Aba 1: Conta Corrente ---
lbl_saldo = tk.Label(
    aba_conta,
    text=f"Saldo Disponível: R$ {saldo:.2f}",
    font=("Arial", 12, "bold"),
)
lbl_saldo.pack(pady=15)

lbl_instrucao = tk.Label(aba_conta, text="Valor (R$):")
lbl_instrucao.pack()

ent_valor_conta = tk.Entry(aba_conta)
ent_valor_conta.pack(pady=5)

btn_frame = tk.Frame(aba_conta)
btn_frame.pack(pady=10)

btn_entrada = tk.Button(
    btn_frame, text="Entrada (+)", bg="#008052", fg="white", command=creditar
)
btn_entrada.grid(row=0, column=0, padx=5)

btn_saida = tk.Button(
    btn_frame, text="Saída (-)", bg="#c8102e", fg="white", command=debitar
)
btn_saida.grid(row=0, column=1, padx=5)

# --- Montagem da Aba 2: Criptoativos ---
lbl_cripto_titulo = tk.Label(
    aba_cripto,
    text="Mercado Digital - Bitcoin (Simulado)",
    font=("Arial", 11, "bold"),
)
lbl_cripto_titulo.pack(pady=10)

lbl_cotacao = tk.Label(
    aba_cripto, text="Cotação Fixa: 1 BTC = R$ 300.000,00"
)
lbl_cotacao.pack()

lbl_btc = tk.Label(
    aba_cripto,
    text=f"Seu Saldo BTC: {cripto_btc:.6f}",
    font=("Arial", 10, "bold"),
    fg="#001E62",
)
lbl_btc.pack(pady=10)

btn_comprar_btc = tk.Button(
    aba_cripto,
    text="Comprar R$ 100,00 em BTC",
    bg=COR_AMARELO,
    command=comprar_btc,
)
btn_comprar_btc.pack(pady=10)

# --- Montagem da Aba 3: Extrato ---
lst_extrato = tk.Listbox(aba_extrato, width=60, height=10)
lst_extrato.pack(padx=10, pady=10, fill="both", expand=True)

# Inicializa a lista com o valor inicial
atualizar_extrato()

# Loop Principal
janela.mainloop()