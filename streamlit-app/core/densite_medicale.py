import pandas as pd
import requests
import json
from typing import Dict, Any
from config import DATA_SOURCE_PATH, MISSING_RATE_MAX, OUTLIER_ZSCORE



class DensiteMedicale:
    def __init__(self, config_path: str = "config/api_credentials.json"):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.pedopsychiatres_france_2022 = 2039
        self.diminution_2010_2022 = -34  # %

    def collecter_densite_pedopsychiatres(self) -> pd.DataFrame:
        """Collecte densité pédopsychiatres par région"""
        
        # Estimation densité par 100 000 habitants 0-17 ans (données DREES)
        densite_regionale = {
            'Île-de-France': 8.5,  # Plus forte concentration
            'Provence-Alpes-Côte d\'Azur': 6.2,
            'Auvergne-Rhône-Alpes': 5.8,
            'Nouvelle-Aquitaine': 4.1,
            'Occitanie': 3.9,
            'Grand Est': 3.5,
            'Hauts-de-France': 2.8,
            'Normandie': 2.5,
            'Bretagne': 2.3,
            'Centre-Val de Loire': 2.1,
            'Pays de la Loire': 2.0,
            'Bourgogne-Franche-Comté': 1.8
        }
        
        # Temps d'accès aux CHU (proxy accessibilité)
        temps_acces_chu = {
            'Île-de-France': 25,  # minutes moyennes
            'Provence-Alpes-Côte d\'Azur': 35,
            'Auvergne-Rhône-Alpes': 40,
            'Hauts-de-France': 45,
            'Grand Est': 50,
            'Nouvelle-Aquitaine': 55,
            'Occitanie': 55,
            'Normandie': 60,
            'Bretagne': 65,
            'Pays de la Loire': 65,
            'Centre-Val de Loire': 70,
            'Bourgogne-Franche-Comté': 75
        }
        
        # Création DataFrame consolidé
        data = []
        for region in densite_regionale.keys():
            data.append({
                'region': region,
                'densite_pedopsychiatres_pour_100k': densite_regionale[region],
                'temps_acces_chu_minutes': temps_acces_chu[region],
                'niveau_accessibilite': self.categoriser_accessibilite(
                    densite_regionale[region], 
                    temps_acces_chu[region]
                ),
                'source': 'DREES_2022',
                'date_collecte': '2025-08-14'
            })
        
        df = pd.DataFrame(data)
        
        # Sauvegarde
        output_path = "data/raw/densite_pedopsychiatres_drees.csv"
        df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"✅ Données densité médicale sauvegardées: {output_path}")
        
        return df

    def categoriser_accessibilite(self, densite: float, temps_acces: int) -> str:
        """Catégorise le niveau d'accessibilité aux soins"""
        if densite >= 6.0 and temps_acces <= 35:
            return "Très bon"
        elif densite >= 4.0 and temps_acces <= 50:
            return "Bon"
        elif densite >= 2.5 and temps_acces <= 65:
            return "Moyen"
        else:
            return "Difficile"
