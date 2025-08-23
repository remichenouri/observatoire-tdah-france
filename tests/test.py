import pytest
import requests
from src.utils.api_validator import validate_apis

def test_api_connectivity():
    """Test la connectivité des APIs"""
    results = validate_apis()
    
    for api_name, result in results.items():
        assert "SUCCESS" in result['status'], f"API {api_name} non accessible"

def test_git_repository():
    """Vérifie que le dépôt Git est correctement configuré"""
    import subprocess
    
    # Vérifier que Git est initialisé
    result = subprocess.run(['git', 'status'], 
                          capture_output=True, text=True)
    assert result.returncode == 0, "Dépôt Git non initialisé"

def test_project_structure():
    """Vérifie la structure du projet"""
    import os
    
    required_dirs = ['src', 'tests', 'docs', 'notebooks']
    required_files = ['README.md', 'requirements.txt', '.gitignore']
    
    for dir_name in required_dirs:
        assert os.path.exists(dir_name), f"Répertoire manquant: {dir_name}"
    
    for file_name in required_files:
        assert os.path.exists(file_name), f"Fichier manquant: {file_name}"

