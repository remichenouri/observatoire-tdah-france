import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import missingno as msno
import yaml
from pathlib import Path
import chardet
import warnings
warnings.filterwarnings('ignore')
from config import DATA_SOURCE_PATH, MISSING_RATE_MAX, OUTLIER_ZSCORE



class DataInspector:
    """Classe pour l'inspection complète des datasets"""
    
    def __init__(self, config_path="config/cleaning_config.yml"):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        self.inspection_results = {}
    
    def detect_encoding(self, file_path):
        """Détecte l'encodage d'un fichier"""
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
        return result['encoding']
    
    def inspect_file_structure(self, file_path):
        """Inspection détaillée de la structure du fichier"""
        print(f"\n{'='*50}")
        print(f"INSPECTION DE: {file_path}")
        print(f"{'='*50}")
        
        # Détection encodage
        encoding = self.detect_encoding(file_path)
        print(f"Encodage détecté: {encoding}")
        
        # Lecture avec différents séparateurs
        for sep in [',', ';', '\t', '|']:
            try:
                df_test = pd.read_csv(file_path, sep=sep, encoding=encoding, nrows=5)
                if len(df_test.columns) > 1:
                    print(f"Séparateur optimal: '{sep}'")
                    print(f"Nombre de colonnes: {len(df_test.columns)}")
                    break
            except:
                continue
        
        # Chargement complet
        df = pd.read_csv(file_path, sep=sep, encoding=encoding)
        
        return df, encoding, sep
    
    def profiling_statistique(self, df, dataset_name):
        """Profilage statistique complet"""
        results = {
            'dataset_name': dataset_name,
            'shape': df.shape,
            'memory_usage': df.memory_usage(deep=True).sum() / 1024**2,  # MB
            'dtypes': df.dtypes.to_dict(),
            'missing_summary': df.isnull().sum().to_dict(),
            'numeric_summary': {},
            'categorical_summary': {}
        }
        
        # Analyse variables numériques
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            results['numeric_summary'][col] = {
                'mean': df[col].mean(),
                'std': df[col].std(),
                'min': df[col].min(),
                'max': df[col].max(),
                'q25': df[col].quantile(0.25),
                'q50': df[col].quantile(0.50),
                'q75': df[col].quantile(0.75),
                'outliers_count': len(df[col][(np.abs(df[col] - df[col].mean()) > 2*df[col].std())])
            }
        
        # Analyse variables catégorielles
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            results['categorical_summary'][col] = {
                'unique_count': df[col].nunique(),
                'top_values': df[col].value_counts().head().to_dict(),
                'missing_rate': df[col].isnull().mean()
            }
        
        self.inspection_results[dataset_name] = results
        return results
    
    def create_quality_dashboard(self, df, dataset_name):
        """Création du tableau de bord qualité"""
        
        # 1. Graphique des valeurs manquantes
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Valeurs Manquantes par Variable', 'Distribution des Variables Numériques',
                          'Corrélation des Variables Numériques', 'Cardinalité des Variables Catégorielles'),
            specs=[[{"type": "bar"}, {"type": "histogram"}],
                   [{"type": "heatmap"}, {"type": "bar"}]]
        )
        
        # Valeurs manquantes
        missing_data = df.isnull().sum().sort_values(ascending=True)
        missing_pct = (missing_data / len(df) * 100).round(2)
        
        fig.add_trace(
            go.Bar(x=missing_pct.values, y=missing_pct.index, orientation='h',
                   name='% Manquant', marker_color='red'),
            row=1, col=1
        )
        
        # Distribution variables numériques (exemple première variable)
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            fig.add_trace(
                go.Histogram(x=df[numeric_cols[0]], name=f'Distribution {numeric_cols[0]}',
                           marker_color='blue'),
                row=1, col=2
            )
        
        # Heatmap corrélation
        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()
            fig.add_trace(
                go.Heatmap(z=corr_matrix.values, x=corr_matrix.columns, y=corr_matrix.index,
                          colorscale='RdYlBu', name='Corrélation'),
                row=2, col=1
            )
        
        # Cardinalité variables catégorielles
        categorical_cols = df.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            cardinality = [df[col].nunique() for col in categorical_cols[:10]]  # Top 10
            fig.add_trace(
                go.Bar(x=categorical_cols[:10], y=cardinality, name='Cardinalité',
                       marker_color='green'),
                row=2, col=2
            )
        
        fig.update_layout(height=800, showlegend=False, 
                         title_text=f"Tableau de Bord Qualité - {dataset_name}")
        
        # Sauvegarde
        fig.write_html(f"reports/figures/quality_dashboard_{dataset_name}.html")
        return fig

# Usage dans le notebook
def run_initial_inspection_custom(fichiers_donnees):
    """Version adaptée pour les données TDAH réelles"""
    inspector = DataInspector()
    datasets = {}
    
    for nom, chemin in fichiers_donnees.items():
        print(f"\n🔍 Inspection de {nom}...")
        
        # Détection automatique du séparateur (DREES utilise souvent ';')
        df, encoding, sep = inspector.inspect_file_structure(chemin)
        
        # Adaptation spécifique par source
        if 'drees' in nom.lower():
            # Les données DREES ont souvent des en-têtes complexes
            df = clean_drees_headers(df)
        elif 'insee' in nom.lower():
            # INSEE a ses propres codes
            df = standardize_insee_codes(df)
        
        datasets[nom] = df
        results = inspector.profiling_statistique(df, nom)
        inspector.create_quality_dashboard(df, nom)
    
    return datasets, inspector.inspection_results

    # Inspection de chaque fichier
    for name, path in inspector.config['data_sources'].items():
        print(f"\n🔍 Inspection de {name}...")
        df, encoding, sep = inspector.inspect_file_structure(path)
        datasets[name] = df
        
        # Profilage
        results = inspector.profiling_statistique(df, name)
        
        # Dashboard qualité
        inspector.create_quality_dashboard(df, name)
        
        print(f"✅ Dataset {name} inspecté: {df.shape[0]} lignes, {df.shape[1]} colonnes")
    
    return datasets, inspector.inspection_results
