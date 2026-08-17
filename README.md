# 🐍 Projetos Educacionais em Python - Finanças, História e Clima

Este repositório contém uma coleção de aplicações gráficas desenvolvidas em Python utilizando Tkinter. Os projetos foram elaborados com foco didático para alunos do programa Jovem Aprendiz, integrando conceitos de programação procedural, educação financeira, história do Brasil e consumo de APIs em tempo real.

---

## 🎯 Objetivos Didáticos

* **Lógica Procedural:** Estruturação de código sem o uso de Orientação a Objetos (POO), facilitando a assimilação inicial de funções, parâmetros e escopo global (`global`).
* **Interface Gráfica (GUI):** Construção de telas interativas com `tkinter` e componentes modernos (`ttk.Notebook`, `tk.Canvas`, `Listbox`, `Frame`, etc.).
* **Tratamento de Exceções:** Uso de blocos `try/except` para validação de entradas numéricas, manipulação de arquivos de imagem e tratamento de erros de conexão HTTP/rede.
* **Consumo de Requisições HTTP e APIs:** Integração com a web (`requests`, API OpenWeatherMap), manipulação e redimensionamento de imagens (`Pillow`) e concorrência para execução assíncrona (`threading`).
* **Geração de Dados Sintéticos:** Uso da biblioteca `Faker` para sorteio dinâmico de cidades para testes.

---

## 🚀 Projetos Incluídos

### 1. 📜 Linha do Tempo: Eufrásia Teixeira Leite (`historia_financas_with_eufrasia_seunome.py`)
Uma interface interativa sobre Eufrásia Teixeira Leite (1850–1930), a primeira investidora global do Brasil.
* **Destaques:**
  * Download e exibição de imagem histórica via requisição HTTP (`requests` e `Pillow` com filtro `LANCZOS`).
  * Tratamento de falhas de conexão com fallback visual para manter a aplicação funcional mesmo offline.
  * Botões interativos para exibição de fatos históricos, curiosidades e legado em caixas de diálogo (`messagebox`).

### 2. 💵 Simulador de Aportes (`financas_aportes_bankb3_seunome.py`)
Uma calculadora de fluxo de caixa simplificada para ensinar operações de depósito e saque.
* **Destaques:**
  * Controle de saldo em tempo real.
  * Validação de entrada para impedir valores nulos, negativos ou saques maiores do que o saldo disponível.
  * Atualização dinâmica dos rótulos e campos de texto (`Entry.delete` e `Label.config`).

### 3. 📊 Dashboard Financeiro - Padrão B3 (`financas_dashboard_bankb3_seunome.py`)
Um painel completo com a identidade visual inspirada na Bolsa de Valores brasileira (B3 — azul `#001E62` e amarelo `#F2A900`).
* **Destaques:**
  * Uso de abas interativas (`ttk.Notebook`) para navegar entre **Conta Corrente**, **Criptoativos** e **Extrato**.
  * Simulação de compra de frações de Bitcoin (BTC) a uma cotação fixa (R$ 300.000,00/BTC).
  * Histórico de transações em tempo real com controle de estado mantido em lista (`historico`) e renderizado via `tk.Listbox`.

### 4. 🌤️ App de Clima - Vocação (`app_clima_vocacao_seunome.py`)
Uma aplicação meteorológica interativa que consulta a API OpenWeatherMap em tempo real.
* **Destaques:**
  * **Threading Assíncrono:** Execução das requisições HTTP em segundo plano via `threading.Thread` para evitar o congelamento da interface do Tkinter.
  * **Modo Claro / Modo Escuro:** Alternância dinâmica de tema ajustando paletas de cores (`PALETA_ESCURA` / `PALETA_CLARA`) e cor adaptativa da caixa de temperatura de acordo com a faixa térmica (°C).
  * **Sorteio de Cidades:** Integração com a biblioteca `Faker` (`pt_BR`) para geração e busca automática de cidades aleatórias.
  * **Canvas & Transparência:** Renderização de imagem de fundo e download/exibição de ícones de clima em tempo real sobre o `tk.Canvas`.
  * **Dados Detalhados:** Exibição de temperatura (mín/máx), sensação térmica, umidade, velocidade do vento (convertida para km/h) e horários de nascer/pôr do sol calculados a partir do fuso horário retornado da API.

---

## 🛠️ Pré-requisitos e Instalação

Para executar os projetos, você precisará do **Python 3.10+** instalado em sua máquina.

### 1. Instalar as dependências do projeto

Abra o terminal ou prompt de comando e execute:

```bash
pip install requests pillow faker

python -m pip install requests pillow faker
sudo apt-get install python3-tkinter

# 1. Executar a Linha do Tempo de Eufrásia
python historia_financas_with_eufrasia_seunome.py

# 2. Executar o Simulador de Aportes
python financas_aportes_bankb3_seunome.py

# 3. Executar o Dashboard B3
python financas_dashboard_bankb3_seunome.py

# 4. Executar o App de Clima
python app_clima_vocacao_seunome.py
´´´
### Estrutura do Repositório

├── historia_financas_with_eufrasia_seunome.py    # Aplicação sobre Eufrásia Teixeira Leite (Linha do Tempo)
├── financas_aportes_bankb3_seunome.py            # Simulador simples de depósitos e saques
├── financas_dashboard_bankb3_seunome.py         # Dashboard financeiro em abas (Padrão B3)
├── app_clima_vocacao_seunome.py                  # App de consulta de clima com OpenWeatherMap e Faker
└── README.md                                     # Documentação do projeto



