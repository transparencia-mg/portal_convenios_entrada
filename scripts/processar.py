from pathlib import Path
import pandas as pd

# ============================================================
# CAMINHOS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "upload"
ARQUIVO_LINKS = BASE_DIR / "link_convenios.xlsx"

# ============================================================
# COLUNAS A REMOVER
# ============================================================

COLUNAS_EXCLUIR = [
    "Inteiro teor do Instrumento - TransfereGov",
    "Inteiro teor do Instrumento - Sigcon",
    "Doc_autorizativo",
    "nome_pdf",
    "id.y",
    "drive_resource",
    "TA 1",
    "TA 2",
    "TA 3",
    "TA 4",
    "TA 5",
    "TA 6",
    "TA 7",
    "TA 8",
    "TA 9",
    "TA 10",
    "TA 11",
    "TA 12",
    "TA 13",
    "TA 16",
    "TA 17",
    "TA 20",
    "TA 21",
    "TA 22",
]

# ============================================================
# LOCALIZA O ARQUIVO SIGCON
# ============================================================

arquivos = sorted(
    UPLOAD_DIR.glob("Consultas SIGCON - Instrumentos de 2021 até 2026*.xlsx")
)

print(f"Diretório do projeto : {BASE_DIR}")
print(f"Pasta upload         : {UPLOAD_DIR}")

if not arquivos:
    print("\nArquivos encontrados na pasta upload:")
    for arq in sorted(UPLOAD_DIR.glob("*")):
        print(f" - {arq.name}")

    raise FileNotFoundError(
        "Arquivo 'Consultas SIGCON - Instrumentos de 2021 até 2026*.xlsx' não encontrado."
    )

arquivo_sigcon = arquivos[0]

print("\nArquivo encontrado:")
print(arquivo_sigcon.name)

# ============================================================
# LEITURA DOS ARQUIVOS
# ============================================================

print("\nLendo arquivo SIGCON...")
df = pd.read_excel(arquivo_sigcon)

print("Lendo link_convenios.xlsx...")
links = pd.read_excel(ARQUIVO_LINKS)

# ============================================================
# REMOVE COLUNAS ANTIGAS
# ============================================================

cols_existentes = [c for c in COLUNAS_EXCLUIR if c in df.columns]

if cols_existentes:
    print(f"Removendo {len(cols_existentes)} colunas antigas...")
    df = df.drop(columns=cols_existentes)

# ============================================================
# VALIDAÇÕES
# ============================================================

if "Código SIAFI" not in df.columns:
    raise Exception(
        "Coluna 'Código SIAFI' não encontrada no arquivo principal."
    )

if "Código SIAFI" not in links.columns:
    raise Exception(
        "Coluna 'Código SIAFI' não encontrada em link_convenios.xlsx."
    )

if "Inteiro Teor" not in links.columns:
    raise Exception(
        "Coluna 'Inteiro Teor' não encontrada em link_convenios.xlsx."
    )

# ============================================================
# RELACIONAMENTO
# ============================================================

print("Criando relacionamento...")

mapa = dict(
    zip(
        links["Código SIAFI"].astype(str).str.strip(),
        links["Inteiro Teor"]
    )
)

nova_coluna = (
    df["Código SIAFI"]
      .astype(str)
      .str.strip()
      .map(mapa)
)

# ============================================================
# INSERE A COLUNA
# ============================================================

posicao_w = min(22, len(df.columns))

df.insert(
    posicao_w,
    "Inteiro_Teor",
    nova_coluna
)

# ============================================================
# SALVA O RESULTADO
# ============================================================

arquivo_saida = UPLOAD_DIR / "convenios.xlsx"

print("Salvando convenios.xlsx...")

df.to_excel(
    arquivo_saida,
    index=False
)

# ============================================================
# REMOVE O ARQUIVO ORIGINAL
# ============================================================

try:
    arquivo_sigcon.unlink()
    print("Arquivo original removido.")
except Exception as e:
    print(f"Não foi possível remover o arquivo original: {e}")

# ============================================================
# FINALIZAÇÃO
# ============================================================

print()
print("=" * 60)
print("PROCESSAMENTO CONCLUÍDO")
print("=" * 60)
print(f"Arquivo gerado: {arquivo_saida}")