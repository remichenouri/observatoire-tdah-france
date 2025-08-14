import os
import json
import pandas as pd
from typing import Dict, Any
import numpy as np
from collections import defaultdict

# Import des collecteurs
from collectors.epidemiologie import EpidemiologieTDAH
from collectors.socio_economie import SocioEconomie  
from collectors.densite_medicale import DensiteMedicale
from collectors.ansm_prescriptions import PrescriptionsANSM

class ObservatoireTDAHCollector:
    def __init__(self, config_path: str = "config/api_credentials.json"):
        """Collecteur principal de l'Observatoire TDAH"""
        self.config_path = config_path
        self.cache_local = {}
        self.variation_max = 0.15  # ±15% pour simulation encadrée
        
        # Initialisation des collecteurs
        self.epidemio = EpidemiologieTDAH(config_path)
        self.socio_eco = SocioEconomie(config_path)
        self.densite_med = DensiteMedicale(config_path)
        self.ansm = PrescriptionsANSM(config_path)
        
        print("🚀 ObservatoireTDAHCollector initialisé")

    def verifier_structure_dossiers(self):
        """Crée la structure de dossiers si nécessaire"""
        dossiers = [
            "data/raw",
            "data/processed", 
            "data/cache",
            "config",
            "src/collectors"
        ]
        
        for dossier in dossiers:
            os.makedirs(dossier, exist_ok=True)
        
        print("✅ Structure des dossiers vérifiée")

    def collecter_toutes_donnees(self) -> Dict[str, pd.DataFrame]:
        """Collecte complète des données Phase 2"""
        print("\n📊 === DÉBUT COLLECTE PHASE 2 ===")
        
        donnees_collectees = {}
        
        try:
            # 1. Épidémiologie
            print("\n1️⃣ Collecte épidémiologie...")
            donnees_collectees['epidemiologie'] = self.epidemio.collecter_toutes_regions()
            
            # 2. Socio-économie
            print("\n2️⃣ Collecte socio-économie...")
            donnees_collectees['socio_economie'] = self.socio_eco.collecter_pauvrete_regionale()
            
            # 3. Densité médicale
            print("\n3️⃣ Collecte densité médicale...")
            donnees_collectees['densite_medicale'] = self.densite_med.collecter_densite_pedopsychiatres()
            
            # 4. Prescriptions ANSM
            print("\n4️⃣ Collecte prescriptions ANSM...")
            self.ansm.generer_csv_methylphenidate()
            donnees_collectees['prescriptions'] = self.ansm.analyser_tendances()
            
            print("\n✅ === COLLECTE PHASE 2 TERMINÉE ===")
            return donnees_collectees
            
        except Exception as e:
            print(f"❌ Erreur lors de la collecte: {e}")
            return {}

    def consolider_donnees(self, donnees: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """Consolide toutes les données en un DataFrame unifié"""
        print("\n🔄 Consolidation des données...")
        
        # Jointure des données par région
        df_final = None
        
        # Base: données épidémiologiques
        if 'epidemiologie' in donnees:
            df_final = donnees['epidemiologie'].copy()
            df_final = df_final.rename(columns={'nom_region': 'region'})
        
        # Ajout socio-économie
        if 'socio_economie' in donnees and df_final is not None:
            df_final = df_final.merge(
                donnees['socio_economie'], 
                on='region', 
                how='left'
            )
        
        # Ajout densité médicale
        if 'densite_medicale' in donnees and df_final is not None:
            df_final = df_final.merge(
                donnees['densite_medicale'], 
                on='region', 
                how='left'
            )
        
        # Calculs d'indicateurs composites
        if df_final is not None:
            df_final = self.calculer_indicateurs_composites(df_final)
            
            # Sauvegarde données consolidées
            output_path = "data/processed/donnees_consolidees_phase2.csv"
            df_final.to_csv(output_path, index=False, encoding='utf-8')
            print(f"✅ Données consolidées sauvegardées: {output_path}")
        
        return df_final

    def calculer_indicateurs_composites(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calcule des indicateurs composites pour l'analyse"""
        
        # Indicateur de vulnérabilité TDAH
        df['vulnerabilite_tdah'] = (
            df['taux_pauvrete'] * 0.4 +  # Impact pauvreté
            (100 - df['densite_pedopsychiatres_pour_100k'] * 10) * 0.3 +  # Manque spécialistes
            (df['temps_acces_chu_minutes'] / 10) * 0.3  # Accessibilité géographique
        )
        
        # Besoins non couverts estimés
        df['besoins_non_couverts'] = df['cas_tdah_estimes'] * (df['vulnerabilite_tdah'] / 100)
        
        # Classement des régions
        df['rang_vulnerabilite'] = df['vulnerabilite_tdah'].rank(ascending=False)
        
        print("✅ Indicateurs composites calculés")
        return df

    def generer_rapport_collecte(self, donnees: Dict[str, pd.DataFrame]) -> str:
        """Génère un rapport de la collecte"""
        
        rapport = []
        rapport.append("# RAPPORT COLLECTE PHASE 2 - OBSERVATOIRE TDAH")
        rapport.append(f"Date: 2025-08-14")
        rapport.append(f"Heure: {pd.Timestamp.now().strftime('%H:%M:%S')}")
        rapport.append("")
        
        for nom_dataset, df in donnees.items():
            rapport.append(f"## {nom_dataset.upper()}")
            rapport.append(f"- Nombre de lignes: {len(df)}")
            rapport.append(f"- Nombre de colonnes: {len(df.columns)}")
            rapport.append(f"- Colonnes: {', '.join(df.columns)}")
            rapport.append("")
        
        # Sauvegarde rapport
        rapport_path = "data/processed/rapport_collecte_phase2.md"
        with open(rapport_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(rapport))
        
        print(f"✅ Rapport généré: {rapport_path}")
        return rapport_path

    def executer_collecte_complete(self):
        """Exécution complète de la collecte Phase 2"""
        print("🚀 LANCEMENT COLLECTE COMPLETE PHASE 2")
        
        # Vérifications préalables
        self.verifier_structure_dossiers()
        
        # Collecte
        donnees = self.collecter_toutes_donnees()
        
        if donnees:
            # Consolidation
            df_consolide = self.consolider_donnees(donnees)
            
            # Rapport
            self.generer_rapport_collecte(donnees)
            
            print(f"\n🎉 COLLECTE TERMINÉE AVEC SUCCÈS!")
            print(f"📁 Fichiers générés dans data/raw/ et data/processed/")
            
            return df_consolide
        else:
            print("❌ Échec de la collecte")
            return None
