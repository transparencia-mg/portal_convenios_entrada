import subprocess
import sys

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "upload"
ARQUIVO_LINKS = BASE_DIR / "link_convenios.xlsx"

SCRIPTS = [
    "scripts/processar.py",
    "scripts/particionar_execucao.py",
    "scripts/publicar.py",
]

for script in SCRIPTS:
    print(f"\n{'=' * 60}\nExecutando {script}\n{'=' * 60}")
    resultado = subprocess.run(["python", script])
    if resultado.returncode != 0:
        print(f"\nERRO: {script} falhou (código {resultado.returncode}). Pipeline interrompido.")
        sys.exit(resultado.returncode)

print("\nPipeline concluído com sucesso.")
