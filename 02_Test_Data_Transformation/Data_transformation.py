import os
import zipfile
import pdfplumber
import pandas as pd

# Diretório de trabalho (onde o código está localizado)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminho do arquivo PDF (buscando na pasta do exercício 1)
PDF_FILE = os.path.join(BASE_DIR, "..", "01_Test_Web_Scraping", "anexo_unico.pdf")
CSV_FILE = os.path.join(BASE_DIR, "dados_extraidos.csv")
ZIP_FILE = os.path.join(BASE_DIR, "Teste_Jonathan_Goncalves_da_Silva.zip")

# Mapeamento de abreviações para descrições completas
ABREVIACOES = {
    "OD": "Consulta Odontológica",
    "AMB": "Procedimento Ambulatorial"
}

def extrair_tabela_do_pdf(pdf_path):
    dados_extraidos = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    # Limpeza de espaços extras e caracteres invisíveis
                    row_limpa = [str(cell).strip().replace("\n", " ") if cell else "" for cell in row]
                    if any(row_limpa):  # Evita linhas vazias
                        dados_extraidos.append(row_limpa)
    
    return dados_extraidos

def salvar_como_csv(dados, csv_path):
    if not dados:
        print("Erro: Nenhum dado extraído do PDF!")
        return
    
    df = pd.DataFrame(dados)

    # Verifica se há pelo menos 4 colunas antes de renomear
    if len(df.columns) >= 4:
        df.rename(columns={0: "Código", 1: "Descrição", 2: "OD", 3: "AMB"}, inplace=True)

        # Substituir abreviações SOMENTE nas colunas OD e AMB
        if "OD" in df.columns:
            df["OD"] = df["OD"].replace(ABREVIACOES)
        if "AMB" in df.columns:
            df["AMB"] = df["AMB"].replace(ABREVIACOES)
    
    # Salvar o CSV com encoding UTF-8 e sem índice
    df.to_csv(csv_path, index=False, encoding='utf-8')
    print(f"Dados salvos em {csv_path}")

def compactar_csv(csv_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(csv_path, os.path.basename(csv_path))
    print(f"Arquivo ZIP criado em {zip_path}")

def main():
    if not os.path.exists(PDF_FILE):
        print("Erro: O arquivo PDF não foi encontrado!")
        return
    
    dados = extrair_tabela_do_pdf(PDF_FILE)
    if not dados:
        print("Nenhuma tabela encontrada no PDF.")
        return
    
    salvar_como_csv(dados, CSV_FILE)
    compactar_csv(CSV_FILE, ZIP_FILE)

if __name__ == "__main__":
    main()
