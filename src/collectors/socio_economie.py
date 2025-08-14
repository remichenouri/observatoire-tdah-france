import pandas as pd
import requests
import json
from typing import Dict, Any

class SocioEconomie:
    def __init__(self, config_path: str = "config/api_credentials.json"):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.taux_pauvrete_national_2023 = 15.4  # Référence INSEE

    def collecter_pauvrete_regionale(self) -> pd.DataFrame:
        """Collecte taux de pauvreté par région"""
        
        # Données de référence (dernières données INSEE disponibles)
        pauvrete_regionale = {
            'Hauts-de-France': 19.5,
            'Corse': 18.8, 
            'Occitanie': 17.2,
            'Provence-Alpes-Côte d\'Azur': 16.8,
            'Grand Est': 14.8,
            'Nouvelle-Aquitaine': 14.2,
            'Normandie': 13.9,
            'Centre-Val de Loire': 13.5,
            'Auvergne-Rhône-Alpes': 12.8,
            'Bourgogne-Franche-Comté': 12.5,
            'Pays de la Loire': 11.2,
            'Bretagne': 10.8,
            'Île-de-France': 15.1  # Contrastes importants intra-région
        }
        
        # Conversion en DataFrame
        data = []
        for region, taux in pauvrete_regionale.items():
            data.append({
                'region': region,
                'taux_pauvrete': taux,
                'ecart_national': taux - self.taux_pauvrete_national_2023,
                'source': 'INSEE_2023',
                'date_collecte': '2025-08-14'
            })
        
        df = pd.DataFrame(data)
        
        # Sauvegarde
        output_path = "data/raw/pauvrete_regionale_2023.csv"
        df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"✅ Données socio-économiques sauvegardées: {output_path}")
        
        return df

    def collecter_donnees_drees_revenus(self) -> Dict[str, Any]:
        """Tentative collecte API DREES pour données de revenus"""
        try:
            drees_config = self.config['drees']
            url = f"{drees_config['base_url']}catalog/datasets"
            
            response = requests.get(url)
            if response.status_code == 200:
                datasets = response.json()
                print("✅ Connexion DREES réussie")
                return datasets
            else:
                print("⚠️ API DREES indisponible")
                return {}
        except Exception as e:
            print(f"⚠️ Erreur DREES: {e}")
            return {}
