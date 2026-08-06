import os
import glob
import math
import pandas as pd

# ============================================================
# CONFIGURAÇÕES
# ============================================================

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "upload"

LINHAS_POR_ARQUIVO = 50000

# ============================================================
# LOCALIZA ARQUIVO DE EXECUÇÃO
# ============================================================

arquivos = glob.glob(
    os.path.join(
        UPLOAD_DIR,
        "Execução Estadual - Execução*.xlsx"
    )
)

if not arquivos:
    raise FileNotFoundError(
        "Arquivo 'Execução Estadual - Execução (SIAFI)' não encontrado."
    )

arquivo_execucao = arquivos[0]

print("Arquivo encontrado:")
print(arquivo_execucao)

# ============================================================
# LEITURA
# ============================================================

print("Lendo arquivo de Execução...")
df = pd.read_excel(arquivo_execucao)

total_linhas = len(df)
n_arquivos = math.ceil(total_linhas / LINHAS_POR_ARQUIVO)

print(f"Total de linhas: {total_linhas}")
print(f"Arquivos a gerar: {n_arquivos}")

# ============================================================
# PARTICIONA E SALVA
# ============================================================

arquivos_gerados = []

for i in range(n_arquivos):
    inicio = i * LINHAS_POR_ARQUIVO
    fim = inicio + LINHAS_POR_ARQUIVO
    parte = df.iloc[inicio:fim]

    nome = "execucao.xlsx" if i == 0 else f"execucao{i}.xlsx"
    caminho_saida = os.path.join(UPLOAD_DIR, nome)

    print(f"Salvando {nome} ({len(parte)} linhas)...")
    parte.to_excel(caminho_saida, index=False)
    arquivos_gerados.append(caminho_saida)

# ============================================================
# REMOVE ARQUIVO ORIGINAL
# ============================================================

try:
    os.remove(arquivo_execucao)
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
for arq in arquivos_gerados:
    print(f"Arquivo gerado: {arq}")
