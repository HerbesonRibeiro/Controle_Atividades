import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from GitHubUpdater import GitHubUpdater
import pytest


# Teste básico (que já passou)
def test_check_for_updates():
    updater = GitHubUpdater(
        repo_owner="HerbesonRibeiro",
        repo_name="Controle_Atividades",
        current_version="1.0.0"
    )
    result = updater.check_for_updates()
    assert isinstance(result, dict)
    assert 'available' in result


# Teste com mock para simular uma nova versão
def test_update_available(mocker):
    # Configura uma resposta fake da API
    fake_response = {
        "tag_name": "v1.1.0",
        "body": "Correção de bugs",
        "assets": []
    }
    mocker.patch('requests.get', return_value=mocker.Mock(json=lambda: fake_response, raise_for_status=lambda: None))

    updater = GitHubUpdater("fake_owner", "fake_repo", "1.0.0")
    result = updater.check_for_updates()

    assert result['available'] is True
    assert result['version'] == "1.1.0"


# Teste para quando não há atualização
def test_no_update_available(mocker):
    fake_response = {
        "tag_name": "v1.0.0",
        "body": "",
        "assets": []
    }
    mocker.patch('requests.get', return_value=mocker.Mock(json=lambda: fake_response, raise_for_status=lambda: None))

    updater = GitHubUpdater("fake_owner", "fake_repo", "1.0.0")
    result = updater.check_for_updates()

    assert result['available'] is False


# Teste para erro de conexão
def test_connection_error(mocker):
    # Configura o mock para simular erro de conexão
    mocker.patch('requests.get', side_effect=Exception("Erro de conexão"))

    updater = GitHubUpdater("fake_owner", "fake_repo", "1.0.0")
    result = updater.check_for_updates()

    # Verifica se o resultado contém as chaves esperadas
    assert result['available'] is False
    assert 'error' in result
    assert result['error'] == "Erro de conexão"

def test_invalid_release_format(mocker):
    """Testa se o sistema lida com releases sem tag_name"""
    mocker.patch('requests.get', return_value=mocker.Mock(json=lambda: {"body": ""}, raise_for_status=lambda: None))
    updater = GitHubUpdater("fake", "repo", "1.0.0")
    result = updater.check_for_updates()
    assert result['available'] is False
    assert 'error' in result