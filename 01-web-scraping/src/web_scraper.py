import requests
from bs4 import BeautifulSoup
import zipfile
import os

def download_pdfs():
    url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Criar diretório de output se não existir
    os.makedirs('../output', exist_ok=True)
    
    # Encontrar e baixar os anexos
    pdf_links = []
    for link in soup.find_all('a'):
        href = link.get('href', '').lower()
        if 'Anexo I' in href and href.endswith('.pdf'):
            pdf_links.append(('Anexo_I.pdf', href))
        elif 'Anexo II' in href and href.endswith('.pdf'):
            pdf_links.append(('Anexo_II.pdf', href))
    
    for filename, pdf_url in pdf_links:
        pdf_response = requests.get(pdf_url)
        with open(f'../output/{filename}', 'wb') as f:
            f.write(pdf_response.content)
    
    # Compactar os arquivos
    with zipfile.ZipFile('../output/anexos.zip', 'w') as zipf:
        for filename, _ in pdf_links:
            zipf.write(f'../output/{filename}', arcname=filename)
    
    print("Download e compactação concluídos com sucesso!")

if __name__ == "__main__":
    download_pdfs()