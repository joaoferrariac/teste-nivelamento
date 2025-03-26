import os
import sys
import tabula
import pandas as pd
import zipfile

def setup_environment():
    """Configura o ambiente e verifica os requisitos"""
    # Verifica se o arquivo PDF existe
    pdf_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../input/anexo_i.pdf'))
    if not os.path.exists(pdf_path):
        print(f"Erro: Arquivo PDF não encontrado em {pdf_path}")
        print("Por favor, coloque o arquivo 'anexo_i.pdf' na pasta '../input/'")
        sys.exit(1)

    # Verifica o Java
    java_home = os.getenv('JAVA_HOME')
    if not java_home:
        print("Erro: Variável JAVA_HOME não está configurada!")
        print("Siga estas etapas para corrigir:")
        print("1. Instale o JDK 11+ do site adoptium.net")
        print("2. Configure a variável JAVA_HOME apontando para a pasta do JDK")
        print("3. Adicione %JAVA_HOME%\\bin ao PATH do sistema")
        sys.exit(1)

    print(f"Java configurado corretamente (JAVA_HOME={java_home})")
    return pdf_path

def extract_pdf_tables(pdf_path):
    """Extrai tabelas do PDF"""
    try:
        print("Extraindo tabelas do PDF...")
        dfs = tabula.read_pdf(
            pdf_path,
            pages='all',
            multiple_tables=True,
            lattice=True,
            pandas_options={'header': None},
            java_options=["-Djava.awt.headless=true"]  # Opção para evitar problemas gráficos
        )
        
        if not dfs:
            print("Nenhuma tabela encontrada no PDF!")
            return None
            
        print(f"Encontradas {len(dfs)} tabelas")
        return pd.concat(dfs, ignore_index=True)
    except Exception as e:
        print(f"Erro ao extrair tabelas: {str(e)}")
        return None

def process_data(df):
    """Processa os dados extraídos"""
    if df is None:
        return None
        
    # Substitui abreviações
    df.replace({
        'OD': 'Odontológico',
        'AMB': 'Ambulatorial'
    }, inplace=True)
    
    return df

def save_results(df):
    """Salva os resultados em CSV e ZIP"""
    if df is None:
        return False
        
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../output'))
    os.makedirs(output_dir, exist_ok=True)
    
    # Salva CSV
    csv_path = os.path.join(output_dir, 'rol_procedimentos.csv')
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"CSV salvo em: {csv_path}")
    
    # Cria ZIP
    zip_path = os.path.join(output_dir, 'Teste_Joao_Ferrari.zip')
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(csv_path, arcname='rol_procedimentos.csv')
    
    print(f"Arquivo ZIP criado em: {zip_path}")
    return True

if __name__ == "__main__":
    print("=== Iniciando processamento ===")
    pdf_path = setup_environment()
    df = extract_pdf_tables(pdf_path)
    processed_df = process_data(df)
    if save_results(processed_df):
        print("=== Processamento concluído com sucesso! ===")
    else:
        print("=== Processamento falhou ===")
        
        sys.exit(1)