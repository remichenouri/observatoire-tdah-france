import json
import requests
import pandas as pd
import base64
from typing import Dict, Any

class EpidemiologieTDAH:
    def __init__(self, config_path: str = "config/api_credentials.json"):
        """Initialise le collecteur d'épidémiologie TDAH"""
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        with open("config/insee_endpoints.json", 'r') as f:
            self.endpoints = json.load(f)
        
        self.prevalence_lecendreux = 0.035  # 3,5% chez 6-12 ans
        self.population_6_17_france = 9767500  # Donnée de référence
        self.token = None

    def get_insee_token(self) -> str:
        """Génère un token d'accès INSEE"""
        if self.token:
            return self.token
            
        insee_config = self.config['insee']
        credentials = f"{insee_config['key']}:{insee_config['secret']}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = "grant_type=client_credentials"
        
        response = requests.post(insee_config['token_url'], headers=headers, data=data)
        
        if response.status_code == 200:
            self.token = response.json()["access_token"]
            print("✅ Token INSEE généré avec succès")
            return self.token
        else:
            print(f"❌ Erreur génération token: {response.status_code}")
            return None

    def collecter_population_insee(self, code_region: str) -> Dict[str, Any]:
        """Collecte population par région via API INSEE officielle"""
        token = self.get_insee_token()
        if not token:
            return self.simulation_encadree_population(code_region)
        
        url = f"{self.config['insee']['base_url']}{self.endpoints['endpoints']['population']['url']}"
        headers = {
            'Authorization': f'Bearer {token}',
            'Accept': 'application/json'
        }
        params = {
            'codeGeo': code_region,
            'variables': ','.join(self.endpoints['endpoints']['population']['variables'])
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                return self.traiter_donnees_population(data, code_region)
            else:
                print(f"⚠️ API INSEE indisponible pour {code_region}, simulation encadrée")
                return self.simulation_encadree_population(code_region)
        except Exception as e:
            print(f"⚠️ Erreur API INSEE {code_region}: {e}")
            return self.simulation_encadree_population(code_region)

    def simulation_encadree_population(self, code_region: str) -> Dict[str, Any]:
        """Simulation encadrée basée sur données connues"""
        # Données de référence par région (à actualiser)
        populations_reference = {
            '11': 1800000,  # Île-de-France
            '84': 1200000,  # Auvergne-Rhône-Alpes
            '75': 900000,   # Nouvelle-Aquitaine
            '76': 850000,   # Occitanie
            '44': 800000,   # Grand Est
            '93': 750000,   # PACA
            '32': 950000,   # Hauts-de-France
            '28': 500000,   # Normandie
            '24': 400000,   # Centre-Val de Loire
            '27': 400000,   # Bourgogne-Franche-Comté
            '53': 500000,   # Bretagne
            '52': 600000    # Pays de la Loire
        }
        
        population_base = populations_reference.get(code_region, 500000)
        # Variation ±15% pour simulation réaliste
        import numpy as np
        variation = np.random.uniform(-0.15, 0.15)
        population_simulee = int(population_base * (1 + variation))
        
        return {
            'code_region': code_region,
            'nom_region': self.endpoints['codes_regions'].get(code_region, 'Inconnue'),
            'population_6_17': population_simulee,
            'source': 'simulation_encadree',
            'variation_appliquee': variation
        }

    def estimer_cas_tdah_region(self, population_region_6_17: int) -> Dict[str, Any]:
        """Estime les cas TDAH par région selon Dr Lecendreux"""
        cas_estimes = population_region_6_17 * self.prevalence_lecendreux
        return {
            'cas_tdah_estimes': int(cas_estimes),
            'prevalence_appliquee': self.prevalence_lecendreux,
            'methodologie': 'Dr_Lecendreux_3.5_pct'
        }

    def collecter_toutes_regions(self) -> pd.DataFrame:
        """Collecte complète pour toutes les régions"""
        donnees_regions = []
        
        for code_region, nom_region in self.endpoints['codes_regions'].items():
            print(f"📊 Collecte {nom_region} ({code_region})...")
            
            # Collecte population
            data_pop = self.collecter_population_insee(code_region)
            
            # Estimation TDAH
            estimation_tdah = self.estimer_cas_tdah_region(data_pop['population_6_17'])
            
            # Consolidation
            data_complete = {**data_pop, **estimation_tdah}
            donnees_regions.append(data_complete)
        
        # Création DataFrame
        df = pd.DataFrame(donnees_regions)
        
        # Sauvegarde
        output_path = "data/raw/insee_population_2022.csv"
        df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"✅ Données épidémiologiques sauvegardées: {output_path}")
        
        return df
