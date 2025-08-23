import json
import os

def create_notebook_structure():
    """Crée la structure JSON d'un notebook Jupyter vide"""
    return {
        "cells": [],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

def add_code_cell(notebook, code):
    """Ajoute une cellule de code au notebook"""
    cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": code.split('\n')
    }
    notebook["cells"].append(cell)
    return notebook

def add_markdown_cell(notebook, markdown):
    """Ajoute une cellule markdown au notebook"""
    cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": markdown.split('\n')
    }
    notebook["cells"].append(cell)
    return notebook

# Créer le notebook 1 : Exploration Initiale
def create_notebook_1():
    notebook = create_notebook_structure()
    
    # Cellule 1: Titre
    add_markdown_cell(notebook, "# 🔍 OBSERVATOIRE TDAH FRANCE - Exploration Initiale\n\nNotebook 1: Inspection et analyse des données sources")
    
    # Cellule 2: Imports
    imports_code = """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

print("🚀 OBSERVATOIRE TDAH FRANCE - EXPLORATION INITIALE")
print("="*60)
print("📊 Inspection des datasets de démonstration")
print("🔬 Analyse de la qualité des données")"""
    
    add_code_cell(notebook, imports_code)
    
    # Cellule 3: Génération de données de démonstration
    demo_data_code = """# Génération de données de démonstration pour l'Observatoire TDAH
import os
os.makedirs('data/raw', exist_ok=True)

# Dataset 1: Densité Pédopsychiatres par région
regions_france = [
    'Île-de-France', 'Provence-Alpes-Côte d\\'Azur', 'Auvergne-Rhône-Alpes',
    'Hauts-de-France', 'Nouvelle-Aquitaine', 'Occitanie', 'Grand Est',
    'Pays de la Loire', 'Normandie', 'Bretagne', 'Bourgogne-Franche-Comté',
    'Centre-Val de Loire', 'Corse'
]

np.random.seed(42)
densite_data = {
    'region': regions_france,
    'code_region': ['11', '93', '84', '32', '75', '76', '44', '52', '28', '53', '27', '24', '94'],
    'densite_podopsychiatres_pour_100k': np.random.uniform(1.5, 8.2, len(regions_france)),
    'population_0_17': np.random.randint(180000, 2500000, len(regions_france)),
    'annee': [2023] * len(regions_france)
}

df_densite = pd.DataFrame(densite_data)
df_densite.to_csv('data/raw/densite_podopsychiatres_drees.csv', index=False)
print("✅ Dataset densité pédopsychiatres créé")
print(df_densite.head())"""
    
    add_code_cell(notebook, demo_data_code)
    
    # Cellule 4: Dataset pauvreté
    pauvrete_code = """# Dataset 2: Pauvreté régionale
pauvrete_data = {
    'region': regions_france,
    'code_insee': ['11', '93', '84', '32', '75', '76', '44', '52', '28', '53', '27', '24', '94'],
    'taux_pauvrete_enfants': np.random.uniform(8.5, 28.3, len(regions_france)),
    'taux_pauvrete_general': np.random.uniform(6.2, 22.1, len(regions_france)),
    'annee': [2023] * len(regions_france)
}

df_pauvrete = pd.DataFrame(pauvrete_data)
df_pauvrete.to_csv('data/raw/pauvrete_regionale_2023.csv', index=False)
print("✅ Dataset pauvreté régionale créé")
print(df_pauvrete.head())"""
    
    add_code_cell(notebook, pauvrete_code)
    
    # Cellule 5: Dataset méthylphénidate
    methylphenidate_code = """# Dataset 3: Consommation méthylphénidate
methylphenidate_data = []
for region in regions_france:
    for annee in [2020, 2021, 2022, 2023]:
        methylphenidate_data.append({
            'region': region,
            'annee': annee,
            'consommation_ddd_par_1000_hab': np.random.uniform(15.2, 45.8),
            'nb_boites_remboursees': np.random.randint(5000, 85000),
            'cout_total_euros': np.random.randint(150000, 2500000)
        })

df_methylphenidate = pd.DataFrame(methylphenidate_data)
df_methylphenidate.to_csv('data/raw/methylphenidate_utilisation.csv', index=False)
print("✅ Dataset méthylphénidate créé")
print(f"Données: {len(df_methylphenidate)} lignes")
print(df_methylphenidate.head())"""
    
    add_code_cell(notebook, methylphenidate_code)
    
    # Cellule 6: Dataset population INSEE
    population_code = """# Dataset 4: Population INSEE
population_data = []
for region in regions_france:
    population_data.append({
        'region': region,
        'code_region': regions_france.index(region) + 1,
        'population_0_17': np.random.randint(180000, 2500000),
        'population_totale': np.random.randint(800000, 12500000),
        'annee': 2022
    })

df_population = pd.DataFrame(population_data)
df_population.to_csv('data/raw/insee_population_2022.csv', index=False)
print("✅ Dataset population INSEE créé")
print(df_population.head())"""
    
    add_code_cell(notebook, population_code)
    
    # Cellule 7: Analyse de qualité
    quality_code = """# Analyse de qualité des données créées
datasets = {
    'Densité Pédopsychiatres': df_densite,
    'Pauvreté Régionale': df_pauvrete,
    'Méthylphénidate': df_methylphenidate,
    'Population INSEE': df_population
}

print("📊 RÉSUMÉ QUALITÉ DES DATASETS")
print("="*50)

for name, df in datasets.items():
    print(f"\\n{name}:")
    print(f"  Taille: {df.shape[0]} lignes × {df.shape[3]} colonnes")
    print(f"  Valeurs manquantes: {df.isnull().sum().sum()}")
    print(f"  Types de données: {df.dtypes.nunique()} types différents")"""
    
    add_code_cell(notebook, quality_code)
    
    # Cellule 8: Visualisation
    viz_code = """# Visualisation rapide des données
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Observatoire TDAH France - Exploration Initiale', fontsize=16, fontweight='bold')

# 1. Densité pédopsychiatres par région
axes[0,0].bar(range(len(df_densite)), df_densite['densite_podopsychiatres_pour_100k'])
axes[0,0].set_title('Densité Pédopsychiatres par Région')
axes[0,0].set_ylabel('Pour 100k habitants')

# 2. Pauvreté enfants par région
axes[0,1].bar(range(len(df_pauvrete)), df_pauvrete['taux_pauvrete_enfants'])
axes[0,1].set_title('Taux Pauvreté Enfants par Région')
axes[0,1].set_ylabel('Pourcentage')

# 3. Évolution méthylphénidate
evolution = df_methylphenidate.groupby('annee')['consommation_ddd_par_1000_hab'].mean()
axes[1,0].plot(evolution.index, evolution.values, marker='o')
axes[1,0].set_title('Évolution Consommation Méthylphénidate')
axes[1,0].set_ylabel('DDD/1000 hab')

# 4. Population par région
axes[1,1].bar(range(len(df_population)), df_population['population_0_17'])
axes[1,1].set_title('Population 0-17 ans par Région')
axes[1,1].set_ylabel('Habitants')

plt.tight_layout()
plt.savefig('reports/figures/exploration_initiale_overview.png', dpi=300, bbox_inches='tight')
plt.show()

print("✅ Visualisations générées et sauvegardées")
print("📁 Fichier: reports/figures/exploration_initiale_overview.png")"""
    
    add_code_cell(notebook, viz_code)
    
    # Cellule finale
    add_markdown_cell(notebook, "## ✅ Exploration Initiale Terminée\n\n**Résultats:**\n- ✅ 4 datasets de démonstration créés\n- ✅ Qualité des données analysée\n- ✅ Visualisations générées\n- ✅ Prêt pour l'étape de nettoyage\n\n**Prochaine étape:** Notebook 2 - Nettoyage des données")
    
    return notebook

# Exécuter la création
notebook_1 = create_notebook_1()

# Sauvegarder
os.makedirs('notebooks/exploratory', exist_ok=True)
with open('notebooks/exploratory/01_exploration_initiale.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook_1, f, indent=2, ensure_ascii=False)

print("✅ Notebook 01_exploration_initiale.ipynb créé avec succès!")
print("📁 Emplacement: notebooks/exploratory/01_exploration_initiale.ipynb")
