# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT
from PyInstaller.utils.hooks import collect_data_files

project_path = os.path.abspath(".")

# Coleta os arquivos de dados do mysql.connector (inclui arquivos de locales)
mysql_data = collect_data_files('mysql.connector', include_py_files=True)

# Monta lista de datas padrão
datas_list = [
    ('assets/icon.ico', 'assets'),
    ('assets/logo_vermelha.png', 'assets'),
    ('.env', '.'),            # Inclui .env (você disse que usa)
    ('version.json', '.'),
    # Inclui client_config.py caso exista (PyUpdater)
]

# Se existir client_config.py no projeto, inclui no bundle (PyUpdater precisa dele)
if os.path.exists(os.path.join(project_path, 'client_config.py')):
    datas_list.append(('client_config.py', '.'))

# Inclui .pyupdater e pyu-data (se existirem) para que o executável tenha os arquivos do cliente/manifest
# Isso resolve problemas onde o exe não encontra configs do PyUpdater em tempo de execução.
pyupdater_dir = os.path.join(project_path, '.pyupdater')
pyu_data_dir = os.path.join(project_path, 'pyu-data')

def add_dir_to_datas(src_dir, dest_name):
    """Adiciona recursivamente arquivos de uma pasta ao datas_list no formato (src, dest)."""
    for root, _, files in os.walk(src_dir):
        for f in files:
            full = os.path.join(root, f)
            # calcula caminho relativo dentro da pasta de origem
            rel = os.path.relpath(full, src_dir)
            # destino será algo como '.pyupdater/<rel>'
            dest = os.path.join(dest_name, os.path.dirname(rel))
            datas_list.append((full, dest))

if os.path.isdir(pyupdater_dir):
    # adiciona todos os arquivos de .pyupdater mantendo estrutura
    add_dir_to_datas(pyupdater_dir, '.pyupdater')

if os.path.isdir(pyu_data_dir):
    # adiciona pyu-data (ex: pyu-data/deploy/version.json etc)
    add_dir_to_datas(pyu_data_dir, 'pyu-data')

a = Analysis(
    ['main.py'],
    pathex=[project_path],
    binaries=[],
    datas=datas_list + mysql_data,
    hiddenimports=[
        # mysql.connector e compatibilidade
        'mysql.connector.locales.eng.client_error',
        'mysql.connector.plugins.mysql_native_password',
        'pkg_resources.py2_warn',
        # babel (tkcalendar depende de babel)
        'babel.numbers',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

# Observações sobre name:
# - PyUpdater historicamente espera um exe temporário chamado "win" ao criar o zip/arquivo.
# - Você pode manter 'win' se seu fluxo de packaging/pyupdater já depende disso.
# - A pasta final gerada pelo COLLECT será nomeada como você indicar no `name` do COLLECT abaixo.
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='win',   # Mantive 'win' conforme seu fluxo anterior. Mude com cuidado.
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,                     # Recomendo False para evitar problemas com UPX. Mude se quiser otimizar.
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,                  # True para ver logs/erros. Troque para False para GUI-only.
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='Controle_atividades'    # nome da pasta/dist final
)
