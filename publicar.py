import os
import subprocess
import sys
import time

# ============================================================
# CONFIGURAÇÕES
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BRANCH = "main"
MAX_TENTATIVAS = 3
ESPERA_ENTRE_TENTATIVAS = 5  # segundos


def git(*args, check=True):
    """Executa um comando git dentro de BASE_DIR e retorna o resultado."""
    return subprocess.run(
        ["git", *args],
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
        check=check,
    )


# ============================================================
# GIT
# ============================================================

print("Verificando alterações...")

resultado = git("status", "--porcelain")

if not resultado.stdout.strip():
    print("\nNenhuma alteração encontrada.")
    sys.exit(0)

git("add", ".")

commit = git(
    "commit", "-m", "Atualização automática convênios de entrada", check=False
)
if commit.returncode != 0:
    # Nada para commitar (ex: git add não gerou diff real) -> não é erro fatal
    if "nothing to commit" in (commit.stdout + commit.stderr).lower():
        print("\nNenhuma alteração encontrada após o add.")
        sys.exit(0)
    print(commit.stdout)
    print(commit.stderr, file=sys.stderr)
    print("ERRO: falha ao criar o commit.")
    sys.exit(1)

print(commit.stdout.strip())

# ------------------------------------------------------------
# Sincroniza com o remoto antes de publicar, com retries.
# Os arquivos gerados (.xlsx) são sempre recriados do zero a cada
# execução, então em caso de divergência com o remoto a versão
# local (recém-gerada) é a que deve prevalecer.
# ------------------------------------------------------------

sucesso = False

for tentativa in range(1, MAX_TENTATIVAS + 1):
    print(f"\nTentativa {tentativa}/{MAX_TENTATIVAS} de publicação...")

    git("fetch", "origin", check=False)

    pull = git(
        "pull",
        "--no-rebase",
        "-X", "ours",
        "origin", BRANCH,
        check=False,
    )
    if pull.returncode != 0:
        print(pull.stdout)
        print(pull.stderr, file=sys.stderr)
        print("Aviso: git pull falhou, tentando novamente...")
        time.sleep(ESPERA_ENTRE_TENTATIVAS)
        continue

    push = git("push", "origin", BRANCH, check=False)
    if push.returncode == 0:
        sucesso = True
        break

    print(push.stdout)
    print(push.stderr, file=sys.stderr)
    print("Aviso: git push falhou (provável corrida com outro push), tentando novamente...")
    time.sleep(ESPERA_ENTRE_TENTATIVAS)

if not sucesso:
    print("\nERRO: não foi possível publicar no GitHub após várias tentativas.")
    sys.exit(1)

print("\nGitHub atualizado com sucesso.")
