import os
import glob
import pandas as pd

# ============================================================
# CONFIGURAÇÕES
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "upload")

ARQUIVO_LINKS = os.path.join(BASE_DIR, "link_convenios.xlsx")

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
# LOCALIZA ARQUIVO SIGCON
# ============================================================

arquivos = glob.glob(
    os.path.join(
        UPLOAD_DIR,
        "Consultas SIGCON - Instrumentos de 2021 até 2026*.xlsx"
    )
)

if not arquivos:
    raise FileNotFoundError(
        "Arquivo 'Consultas SIGCON - Instrumentos de 2021 até 2026' não encontrado."
    )

arquivo_sigcon = arquivos[0]

print(f"Arquivo encontrado:")
print(arquivo_sigcon)

# ============================================================
# LEITURA DOS ARQUIVOS
# ============================================================

print("Lendo arquivo SIGCON...")
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
# RELACIONAMENTO
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

print("Criando dicionário de relacionamento...")

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
# INSERE COLUNA W
# ============================================================

posicao_w = 22  # coluna W (índice 22)

if posicao_w > len(df.columns):
    posicao_w = len(df.columns)

df.insert(
    posicao_w,
    "Inteiro_Teor",
    nova_coluna
)

# ============================================================
# SALVA
# ============================================================

arquivo_saida = os.path.join(
    UPLOAD_DIR,
    "convenios.xlsx"
)

print("Salvando convenios.xlsx...")

df.to_excel(
    arquivo_saida,
    index=False
)

# ============================================================
# REMOVE ARQUIVO ORIGINAL
# ============================================================

try:
    os.remove(arquivo_sigcon)
    print("Arquivo original removido.")
except Exception as e:
    print(f"Não foi possível remover: {e}")

# ============================================================
# (o git add/commit/push agora fica só em publicar.py,
# executado por último no pipeline, depois de TODAS as etapas)
# ============================================================

print()
print("=" * 60)
print("PROCESSAMENTO CONCLUÍDO")
print("=" * 60)
print(f"Arquivo gerado: {arquivo_saida}")