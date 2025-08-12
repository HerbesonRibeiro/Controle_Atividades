# VERSÃO FINAL
import os
import shutil
import subprocess
import zipfile
import json
import sys

# ---------- CONFIG ----------
SPEC_FILE = "main.spec"            # seu .spec
DIST_DIR = "dist"
BUILD_DIR = "build"
VERSION_FILE = "version.json"      # seu arquivo de versão (pode ser vazio/missing)
APP_NAME = "controle-atividades"   # nome usado no zip e no pyupdater --name
PYUPDATER_OUTPUT = ".pyupdater/work"  # pasta onde pyupdater coloca os arquivos processados
# -----------------------------

def read_version():
    """Tenta ler version.json; se falhar pede ao usuário."""
    if os.path.exists(VERSION_FILE):
        try:
            with open(VERSION_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            v = data.get("version") or data.get("Version") or data.get("app_version")
            if v:
                return str(v)
            print(f"[WARN] '{VERSION_FILE}' existe mas não contém a chave 'version'.")
        except Exception as e:
            print(f"[WARN] Falha ao ler '{VERSION_FILE}': {e}")
    # fallback: perguntar ao usuário
    v = input("Digite a versão a usar (ex: 1.0.3): ").strip()
    if not v:
        print("Versão inválida. Abortando.")
        sys.exit(1)
    return v

def run_cmd(cmd, check=True):
    print(f"\n[CMD] {' '.join(cmd)}")
    res = subprocess.run(cmd)
    if check and res.returncode != 0:
        print(f"[ERROR] Comando falhou com código {res.returncode}: {' '.join(cmd)}")
        sys.exit(res.returncode)

def clean_old():
    for p in (DIST_DIR, BUILD_DIR, PYUPDATER_OUTPUT):
        if os.path.isdir(p):
            print(f"[CLEAN] removendo {p} ...")
            shutil.rmtree(p)

def build_with_pyinstaller():
    if not os.path.exists(SPEC_FILE):
        print(f"[ERROR] Spec file '{SPEC_FILE}' não encontrado.")
        sys.exit(1)
    # roda pyinstaller com o spec
    run_cmd(["pyinstaller", SPEC_FILE])

def find_dist_app_folder():
    """Detecta a pasta de app dentro de dist (p.ex. 'Controle_atividades' ou 'Controle-atividades')."""
    if not os.path.isdir(DIST_DIR):
        raise FileNotFoundError(f"'{DIST_DIR}' não existe. Build do PyInstaller falhou?")
    entries = [e for e in os.listdir(DIST_DIR) if os.path.isdir(os.path.join(DIST_DIR, e))]
    if not entries:
        # talvez o build foi onefile e criou um exe diretamente em dist
        files = [f for f in os.listdir(DIST_DIR) if os.path.isfile(os.path.join(DIST_DIR,f))]
        if files:
            # cria uma pasta temporária e copia o exe lá para zipar com estrutura
            tmpname = f"{APP_NAME}-single"
            tmpdir = os.path.join(DIST_DIR, tmpname)
            os.makedirs(tmpdir, exist_ok=True)
            for f in files:
                shutil.copy(os.path.join(DIST_DIR, f), tmpdir)
            return tmpdir
        raise FileNotFoundError(f"Nenhuma pasta encontrada em '{DIST_DIR}'.")
    # se houver múltiplas pastas, tenta escolher a que contém um exe
    for e in entries:
        full = os.path.join(DIST_DIR, e)
        has_exe = any(fn.lower().endswith(".exe") for fn in os.listdir(full))
        if has_exe:
            return full
    # se não encontrou exe, retorna a primeira
    return os.path.join(DIST_DIR, entries[0])

def make_zip(app_folder, version):
    zip_name = f"{APP_NAME}-win-{version}.zip"
    print(f"[ZIP] Criando {zip_name} a partir de {app_folder}")
    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(app_folder):
            for f in files:
                full = os.path.join(root, f)
                # arcnome relativo dentro do zip (sem a raiz da pasta do app)
                arc = os.path.relpath(full, app_folder)
                zf.write(full, arc)
    print(f"[OK] Zip gerado: {zip_name}")
    return zip_name

def pyupdater_process(zip_path, version):
    print(f"[PYUPDATER] processando {zip_path} (name={APP_NAME}, version={version})")
    run_cmd([
        "pyupdater", "pkg",
        "--name", APP_NAME,
        "--version", version,
        zip_path,
        "--process"
    ])
    print("[OK] pyupdater --process finalizado. Verifique .pyupdater/work/")

def main():
    version = read_version()
    print(f"[INFO] versão: {version}")

    clean_old()
    build_with_pyinstaller()

    try:
        app_folder = find_dist_app_folder()
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    zip_path = make_zip(app_folder, version)
    pyupdater_process(zip_path, version)
    print("\n[FINISH] Build e processamento finalizados. Suba o zip resultante no GitHub Release.")

if __name__ == "__main__":
    main()
