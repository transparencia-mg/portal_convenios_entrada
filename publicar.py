import os
import subprocess

# ============================================================
# CONFIGURAÇÕES
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# GIT
# ============================================================

print("Verificando alterações...")

resultado = subprocess.run(
    ["git", "status", "--porcelain"],
    cwd=BASE_DIR,
    capture_output=True,
    text=True
)

if resultado.stdout.strip():

    subprocess.run(["git", "add", "."], cwd=BASE_DIR, check=True)

    subprocess.run(
        ["git", "commit", "-m", "Atualização automática convênios de entrada"],
        cwd=BASE_DIR,
        check=True
    )

    subprocess.run(["git", "push", "origin", "main"], cwd=BASE_DIR, check=True)

    print("\nGitHub atualizado com sucesso.")

else:

    print("\nNenhuma alteração encontrada.")
