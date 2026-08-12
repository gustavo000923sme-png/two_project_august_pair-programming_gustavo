# 🐍 Projetos Educacionais em Python - Finanças, História e Clima

Este repositório contém uma coleção de aplicações gráficas desenvolvidas em Python utilizando Tkinter. Os projetos foram elaborados com foco didático para alunos do programa Jovem Aprendiz, integrando conceitos de programação procedural, educação financeira, história do Brasil e consumo de APIs em tempo real.

## 🎯 Objetivos Didáticos

* **Lógica Procedural:** Estruturação de código sem o uso de Orientação a Objetos (POO), facilitando a assimilação inicial de funções, parâmetros e escopo global (`global`).
* **Interface Gráfica (GUI):** Construção de telas interativas com `tkinter` e componentes modernos (`ttk.Notebook`, `tk.Canvas`, `Listbox`, `Frame`, etc.).
* **Tratamento de Exceções:** Uso de blocos `try/except` para validação de entradas numéricas e tratamento de erros de conexão de rede.
* **Consumo de Requisições HTTP e APIs:** Integração com a web (`requests`, OpenWeatherMap), manipulação de imagens (`Pillow`) e concorrência para execução assíncrona (`threading`).

## 🚀 Projetos Incluídos

### 1. 📜 Linha do Tempo: Eufrásia Teixeira Leite (`historia_financas_with_eufrasia_seunome.py`)

Uma interface interativa sobre Eufrásia Teixeira Leite (1850–1930), a primeira investidora global do Brasil.

**Destaques:**
* Download e exibição de imagem via requisição HTTP (`requests` e `Pillow`).
* Tratamento de falhas de conexão para manter a aplicação funcional mesmo offline.
* Botões interativos para exibição de fatos históricos em caixas de diálogo.

### 2. 💵 Simulador de Aportes (`financas_aportes_bankb3_seunome.py`)

Uma calculadora de fluxo de caixa simplificada para ensinar operações de depósito e saque.

**Destaques:**
* Controle de saldo em tempo real.
* Validação para impedir saques maiores do que o saldo disponível.
* Atualização dinâmica dos rótulos e campos de texto.

### 3. 📊 Dashboard Financeiro - Padrão B3 (`financas_dashboard_bankb3_seunome.py`)

Um painel completo simulando o ambiente da Bolsa de Valores brasileira (B3).

**Destaques:**
* Uso de abas interativas (`ttk.Notebook`) para navegar entre Conta Corrente, Criptoativos e Extrato.
* Simulação de compra de frações de Bitcoin (BTC).
* Histórico de transações em tempo real utilizando `tk.Listbox`.

### 4. 🌤️ App de Clima - Vocação (`app_clima_vocacao_seunome.py`)

Uma aplicação meteorológica interativa que consulta a API OpenWeatherMap em tempo real.

**Destaques:**
* Requisições assíncronas em segundo plano utilizando `threading` para evitar o congelamento da interface.
* Suporte a alternância entre Modo Claro e Modo Escuro mantendo imagem de fundo e paleta ajustada.
* Sorteio de cidades fictícias/aleatórias via biblioteca `Faker`.
* Renderização de ícones de clima transparentes sobre canvas e dados meteorológicos detalhados.

## 🛠️ Pré-requisitos e Instalação

Para executar os projetos, você precisará do Python 3.10+ instalado em sua máquina.

### 1. Instalar as dependências do projeto

Abra o terminal ou prompt de comando e execute:

```bash
pip install requests pillow faker