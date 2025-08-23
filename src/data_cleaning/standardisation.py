import pandas as pd
import numpy as np
import re
from datetime import datetime
import yaml
from typing import Dict, List, Optional

class DataStandardizer:
    """Classe pour la standardisation des données"""
    
    def __init__(self, config_path="config/cleaning_config.yml"):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        self.transformations_log = []
    
    def standardize_regional_codes(self, df: pd.DataFrame, 
                                 column_name: str) -> pd.DataFrame:
        """Standardisation des codes région/département"""
        
        original_values = df[column_name].value_counts()
        print(f"📍 Standardisation codes régionaux: {column_name}")
        
        # Dictionnaire de correspondance (exemple pour la France)
        region_mapping = {
            # Codes numériques vers codes INSEE
            '01': '01', '02': '02', '03': '03', '04': '04', '05': '05',
            # Noms vers codes
            'île-de-france': '11', 'ile-de-france': '11', 'idf': '11',
            'provence-alpes-côte d\'azur': '93', 'paca': '93',
            'auvergne-rhône-alpes': '84', 'auvergne-rhone-alpes': '84',
            'hauts-de-france': '32', 'nord-pas-de-calais': '32',
            'nouvelle-aquitaine': '75', 'aquitaine': '75',
            'occitanie': '76', 'languedoc-roussillon': '76',
            'grand est': '44', 'alsace': '44', 'lorraine': '44',
            'pays de la loire': '52', 'loire': '52',
            'bretagne': '53', 'normandie': '28',
            'centre-val de loire': '24', 'centre': '24',
            'bourgogne-franche-comté': '27', 'bourgogne': '27',
            'corse': '94', 'corsica': '94'
        }
        
        # Application du mapping
        df[f'{column_name}_standardized'] = df[column_name].astype(str).str.lower()
        df[f'{column_name}_standardized'] = df[f'{column_name}_standardized'].map(
            region_mapping).fillna(df[column_name])
        
        # Log des transformations
        self.transformations_log.append({
            'operation': 'regional_code_standardization',
            'column': column_name,
            'before_unique_count': len(original_values),
            'after_unique_count': df[f'{column_name}_standardized'].nunique(),
            'transformation_rate': (len(original_values) - df[f'{column_name}_standardized'].nunique()) / len(original_values)
        })
        
        return df
    
    def standardize_dates(self, df: pd.DataFrame, 
                         date_columns: List[str]) -> pd.DataFrame:
        """Standardisation des formats de dates"""
        
        for col in date_columns:
            if col in df.columns:
                print(f"📅 Standardisation dates: {col}")
                
                # Tentative de conversion avec différents formats
                original_format = df[col].dtype
                
                # Essai des formats de configuration
                for date_format in self.config['date_formats']:
                    try:
                        df[f'{col}_standardized'] = pd.to_datetime(
                            df[col], format=date_format, errors='coerce')
                        break
                    except:
                        continue
                
                # Si échec, utilisation de pd.to_datetime automatique
                if f'{col}_standardized' not in df.columns:
                    df[f'{col}_standardized'] = pd.to_datetime(
                        df[col], errors='coerce', dayfirst=True)
                
                # Ajout d'informations temporelles dérivées
                df[f'{col}_year'] = df[f'{col}_standardized'].dt.year
                df[f'{col}_month'] = df[f'{col}_standardized'].dt.month
                df[f'{col}_quarter'] = df[f'{col}_standardized'].dt.quarter
                
                # Log
                success_rate = df[f'{col}_standardized'].notna().mean()
                self.transformations_log.append({
                    'operation': 'date_standardization',
                    'column': col,
                    'original_format': str(original_format),
                    'success_rate': success_rate,
                    'null_created': df[f'{col}_standardized'].isna().sum()
                })
        
        return df
    
    def standardize_categorical_variables(self, df: pd.DataFrame,
                                       categorical_mappings: Dict) -> pd.DataFrame:
        """Standardisation des variables catégorielles"""
        
        for col, mapping in categorical_mappings.items():
            if col in df.columns:
                print(f"🏷️ Standardisation catégorie: {col}")
                
                original_values = df[col].value_counts()
                
                # Nettoyage préalable
                df[col] = df[col].astype(str).str.strip().str.lower()
                
                # Application du mapping
                df[f'{col}_standardized'] = df[col].map(mapping).fillna(df[col])
                
                # Log
                self.transformations_log.append({
                    'operation': 'categorical_standardization',
                    'column': col,
                    'before_categories': list(original_values.index),
                    'after_categories': df[f'{col}_standardized'].unique().tolist(),
                    'mapping_coverage': df[col].isin(mapping.keys()).mean()
                })
        
        return df
    
    def standardize_units(self, df: pd.DataFrame, 
                         unit_conversions: Dict) -> pd.DataFrame:
        """Standardisation des unités de mesure"""
        
        for col, conversion in unit_conversions.items():
            if col in df.columns:
                print(f"📏 Standardisation unités: {col}")
                
                original_values = df[col].describe()
                
                # Application de la conversion
                df[f'{col}_standardized'] = df[col] * conversion['factor']
                
                # Ajout métadonnées
                df.attrs[f'{col}_unit'] = conversion['target_unit']
                
                # Log
                self.transformations_log.append({
                    'operation': 'unit_standardization',
                    'column': col,
                    'conversion_factor': conversion['factor'],
                    'target_unit': conversion['target_unit'],
                    'value_range_before': [original_values['min'], original_values['max']],
                    'value_range_after': [df[f'{col}_standardized'].min(), 
                                        df[f'{col}_standardized'].max()]
                })
        
        return df
    
    def create_standardization_report(self) -> pd.DataFrame:
        """Génération du rapport de standardisation"""
        return pd.DataFrame(self.transformations_log)

# Configuration des standardisations spécifiques TDAH
TDAH_STANDARDIZATIONS = {
    'categorical_mappings': {
        'diagnostic_tdah': {
            'oui': 'confirmed',
            'non': 'negative', 
            'o': 'confirmed',
            'n': 'negative',
            '1': 'confirmed',
            '0': 'negative',
            'positif': 'confirmed',
            'négatif': 'negative',
            'confirmé': 'confirmed'
        },
        'sexe': {
            'homme': 'M',
            'femme': 'F',
            'h': 'M',
            'f': 'F',
            'masculin': 'M',
            'féminin': 'F',
            'm': 'M'
        },
        'type_medicament': {
            'methylphenidate': 'stimulant',
            'ritaline': 'stimulant',
            'concerta': 'stimulant',
            'atomoxetine': 'non_stimulant',
            'strattera': 'non_stimulant'
        }
    },
    
    'unit_conversions': {
        'age_mois': {'factor': 1/12, 'target_unit': 'years'},
        'dose_mg': {'factor': 1, 'target_unit': 'mg'},
        'cout_euros_centimes': {'factor': 0.01, 'target_unit': 'euros'}
    }
}
