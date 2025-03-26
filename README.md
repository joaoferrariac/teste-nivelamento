# Testes de Nivelamento - ANS

- Autor: João Victor Ferrari de Melo 

## 📌 Visão Geral
Repositório contendo a solução para os 4 testes técnicos:

- **Teste 1:** Web Scraping e download de anexos
- **Teste 2:** Transformação de PDF para CSV
- **Teste 3:** Banco de dados e análise de operadoras
- **Teste 4:** API e Interface Web

## 🤖 Tecnologias Utilizadas

**Linguagem:**
- Python 3.8+

**Bibliotecas:**
- `requests`, `BeautifulSoup`, `tabula-py`, `pandas`, `sqlalchemy`

**Bancos de Dados:**
- MySQL 8.0+ ou PostgreSQL 12+

## 💃💪 Estrutura do Projeto

```
teste-nivelamento/
├── 01-web-scraping/
│   ├── src/
│   │   └── web_scraper.py
│   └── output/
├── 02-transformacao-dados/
│   ├── src/
│   │   └── pdf_to_csv.py
│   └── output/
├── 03-banco-dados/
│   ├── data/
│   ├── scripts/
│   └── download_dados.py
└── 04-api/
    ├── backend/
    │   ├── app.py
    │   ├── requirements.txt
    │   └── data/
    └── frontend/
        ├── src/
        │   ├── App.vue
        │   └── main.js
        └── package.json
```

---

## 🔮 Teste 1: Web Scraping

### 🎯 Objetivo
Baixar anexos I e II do rol de procedimentos da ANS e compactá-los.

### 🛠️ Como executar:
```bash
cd 01-web-scraping/src
pip install requests beautifulsoup4
python web_scraper.py
```

### 📄 Saída esperada:
- Arquivos `anexo_i.pdf` e `anexo_ii.pdf` na pasta `output/`
- Arquivo compactado `anexos.zip` contendo ambos

---

## 🔮 Teste 2: Transformação de Dados

### 🎯 Objetivo
Converter tabelas do PDF (Anexo I) para CSV formatado.

### 🔧 Pré-requisitos:
- Java Runtime Environment (JRE)
- Arquivo `anexo_i.pdf` na pasta `input/`

### 🛠️ Como executar:
```bash
cd 02-transformacao-dados/src
pip install tabula-py pandas
python pdf_to_csv.py
```

### 📄 Saída esperada:
- Arquivo `rol_procedimentos.csv` na pasta `output/`
- Arquivo `Teste_[NOME].zip` com o CSV compactado

---

## 🔮 Teste 3: Banco de Dados

### 🎯 Objetivo
Analisar despesas de operadoras de saúde.

### 🛠️ Como executar:
#### 1. Baixar os dados
```bash
cd 03-banco-dados
pip install pandas sqlalchemy
python download_dados.py
```

#### 2. Importar para o banco (2 métodos):

**Método MySQL:**
```bash
mysql -u root -p < scripts/01_setup.sql
mysql -u root -p ans_db < scripts/02_create_tables.sql
mysql -u root -p ans_db < scripts/03_import_data.sql
```

**Método Python (alternativo):**
```bash
python import_to_db.py
```

#### 3. Executar consultas
```bash
mysql -u root -p ans_db < scripts/04_queries.sql
```

### 📈 Consultas principais:
- Top 10 operadoras com maiores despesas (trimestre)
- Top 10 operadoras com maiores despesas (ano)

### ⚠️ Dificuldades Encontradas:
- **Erro "secure-file-priv" no MySQL**: Algumas versões do MySQL restringem a importação de arquivos CSV.
- **Problemas de encoding nos dados**: O CSV original pode estar em Latin1, exigindo conversão para UTF-8 para evitar erros de exibição.
- **Tempo de processamento**: Algumas consultas podem ser lentas, dependendo do volume de dados.

---

## 🔮 Teste 4: API e Interface Web

### 🎯 Objetivo
Desenvolver uma aplicação web completa para consulta de operadoras de saúde, com:

- **Backend:** API REST em Python (Flask)
- **Frontend:** Interface moderna com Vue.js 3
- **Integração:** Comunicação eficiente entre frontend e backend

### 📄 Arquitetura do Projeto
```
04-api/
├── backend/              # Servidor API
│   ├── app.py            # Endpoints da API
│   ├── requirements.txt  # Dependências Python
│   └── data/             # Dados das operadoras (CSV)
└── frontend/             # Aplicação Vue
    ├── src/
    │   ├── App.vue       # Componente principal
    │   └── main.js       # Inicialização do Vue
    └── package.json      # Dependências JavaScript
```

### 🎯 Funcionalidades Implementadas

#### Backend (Flask)
- **Rota de busca:**
  - `GET /api/operadoras?q={termo}`
  - Filtra operadoras por razão social ou nome fantasia
  - Retorna JSON com até 20 resultados
- **Tratamento de dados:**
  - Carrega dados do CSV da ANS
  - Normaliza buscas (case insensitive)
  - Filtra resultados com pelo menos 3 caracteres

#### Frontend (Vue.js 3)
- **Interface de busca:**
  - Campo de input com busca em tempo real
  - Debounce para otimizar requisições
- **Visualização:**
  - Cards com informações das operadoras
  - Feedback visual durante carregamento
  - Tratamento de erros
- **Design responsivo:**
  - Layout adaptável para diferentes telas
  - Estilos CSS organizados

### 🛠️ Como Executar

#### Backend
```bash
pip install -r requirements.txt
python app.py
```

#### Frontend
```bash
npm install
npm run dev
```

### 📈 Acesso
- **API:** http://localhost:5000
- **Interface Web:** http://localhost:5173

### 💪 Destaques Técnicos
- **Segurança:** Configuração CORS adequada
- **Performance:**
  - Paginação de resultados no backend
  - Cache de requisições no frontend
- **UX:**
  - Feedback visual durante buscas
  - Mensagens de erro claras

---

## 📝 Licença
- Dados abertos disponibilizados pela ANS.
- Código para fins educacionais.

