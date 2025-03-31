import os
import zipfile
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfMerger

# URL of the page containing the PDFs
URL = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

# Directory to save the PDFs and output files
BASE_FOLDER = "C:/Users/praq3/Documents/Projetos/FrontEnd - Challengers/Frontend_Challenger/Frontend_Challenger/docs/Leveling_Test_IntuitiveCare/01_Test_Web_Scraping"

# Diretório de download e pasta para salvar os arquivos
DOWNLOAD_FOLDER = os.path.join(BASE_FOLDER, "downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_pdf(pdf_url, folder):
    filename = os.path.join(folder, pdf_url.split("/")[-1])
    response = requests.get(pdf_url, stream=True)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Download completed: {filename}")
        return filename
    print(f"Error downloading {pdf_url}: {response.status_code}")
    return None

def get_pdf_links():
    response = requests.get(URL)
    if response.status_code != 200:
        print(f"Error accessing the page: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    return [link["href"] for link in soup.find_all("a", href=True)
            if "Anexo" in link.text and link["href"].endswith(".pdf")]

def download_pdfs(links):
    return [download_pdf(link, DOWNLOAD_FOLDER) for link in links if link.startswith("http")]

def merge_pdfs(pdf_files, output_pdf):
    merger = PdfMerger()
    for pdf in pdf_files:
        merger.append(pdf)
    merger.write(output_pdf)
    merger.close()
    print(f"PDFs merged into {output_pdf}")
    return output_pdf

def zip_file(file_path, zip_name):
    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(file_path, os.path.basename(file_path))
    print(f"File compressed into {zip_name}")

def main():
    pdf_links = get_pdf_links()
    if not pdf_links:
        print("No PDFs found on the page.")
        return
    
    pdf_files = download_pdfs(pdf_links)
    if not pdf_files:
        print("Failed to download the PDFs.")
        return

    # Define paths for merged PDF and ZIP file inside 01_Test_Web_Scraping
    merged_pdf = os.path.join(BASE_FOLDER, "anexo_unico.pdf")
    merge_pdfs(pdf_files, merged_pdf)

    zip_name = os.path.join(BASE_FOLDER, "anexos.zip")
    zip_file(merged_pdf, zip_name)

# Script execution
if __name__ == "__main__":
    main()
