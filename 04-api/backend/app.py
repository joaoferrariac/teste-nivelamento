from flask import Flask, request, jsonify
import pandas as pd
import os
import unicodedata
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

# Configurações
CSV_PATH = os.path.join(os.path.dirname(__file__), 'data', 'operadoras_ativas.csv')

def remove_accents(text):
    """Remove acentos mas mantém outros caracteres especiais"""
    if pd.isna(text):
        return ''
    text = unicodedata.normalize('NFKD', str(text))
    text = ''.join(c for c in text if not unicodedata.combining(c))
    return text.lower().strip()

def load_data():
    try:
        # Tenta ler com UTF-8, depois latin1
        try:
            df = pd.read_csv(CSV_PATH, sep=';', encoding='utf-8', dtype=str)
        except:
            df = pd.read_csv(CSV_PATH, sep=';', encoding='latin1', dtype=str)
        
        # Mapeamento de colunas
        column_mapping = {
            'razao_social': ['Razao_Social', 'Razão Social', 'razao_social'],
            'nome_fantasia': ['Nome_Fantasia', 'Nome Fantasia', 'nome_fantasia'],
            'cnpj': ['CNPJ', 'Cnpj'],
            'registro_ans': ['Registro_ANS', 'Registro ANS']
        }
        
        # Renomeia colunas
        for standard, alternatives in column_mapping.items():
            for alt in alternatives:
                if alt in df.columns:
                    df = df.rename(columns={alt: standard})
                    break
        
        # Verifica colunas obrigatórias
        required = ['razao_social', 'nome_fantasia']
        missing = [col for col in required if col not in df.columns]
        if missing:
            raise ValueError(f"Colunas faltando: {missing}")
        
        # Preenche NaN e cria colunas de busca
        for col in ['razao_social', 'nome_fantasia']:
            df[col] = df[col].fillna('')
            df[f'{col}_search'] = df[col].apply(remove_accents)
        
        return df
    
    except Exception as e:
        print(f"Erro ao carregar dados: {str(e)}")
        return pd.DataFrame(columns=['razao_social', 'nome_fantasia'])

# Carrega os dados
df = load_data()

@app.route('/api/operadoras', methods=['GET'])
def search_operadoras():
    try:
        query = remove_accents(request.args.get('q', ''))
        
        if len(query) < 3:
            return jsonify([])
            
        # Filtra os resultados
        results = df[
            df['razao_social_search'].str.contains(query, case=False, na=False) |
            df['nome_fantasia_search'].str.contains(query, case=False, na=False)
        ].head(20)
        
        # Prepara os dados para JSON
        response_data = results.replace({np.nan: None}).to_dict('records')
        return jsonify(response_data)
    
    except Exception as e:
        print(f"Erro na busca: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n=== INICIANDO SERVIDOR ===")
    app.run(host='0.0.0.0', port=5000, debug=True)