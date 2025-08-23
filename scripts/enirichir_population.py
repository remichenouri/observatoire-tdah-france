import pandas as pd
import numpy as np
from pathlib import Path

def enrichir_population_insee():
    """
    Enrichit population_insee_generated.csv avec coordonnées géographiques
    et métriques calculées SANS changer le nom du fichier original
    """
    
    # 1. LECTURE du fichier original
    df_pop = pd.read_csv('raw/population_insee_generated.csv')
    print(f"✅ Fichier original lu : {len(df_pop)} lignes")
    
    # 2. ENRICHISSEMENT géographique des régions françaises
    coordonnees_regions = {
        'Auvergne-Rhône-Alpes': {'lat': 45.7640, 'lon': 4.8357, 'zone': 'Sud-Est'},
        'Bourgogne-Franche-Comté': {'lat': 47.2800, 'lon': 4.0000, 'zone': 'Centre-Est'},
        'Bretagne': {'lat': 48.2020, 'lon': -2.9326, 'zone': 'Ouest'},
        'Centre-Val de Loire': {'lat': 47.7516, 'lon': 1.6751, 'zone': 'Centre'},
        'Corse': {'lat': 42.0396, 'lon': 9.0129, 'zone': 'Sud'},
        'Grand Est': {'lat': 48.6999, 'lon': 6.1878, 'zone': 'Nord-Est'},
        'Hauts-de-France': {'lat': 50.4801, 'lon': 2.7937, 'zone': 'Nord'},
        'Île-de-France': {'lat': 48.8566, 'lon': 2.3522, 'zone': 'Centre'},
        'Normandie': {'lat': 49.1829, 'lon': -0.3707, 'zone': 'Nord-Ouest'},
        'Nouvelle-Aquitaine': {'lat': 45.8336, 'lon': -0.5792, 'zone': 'Sud-Ouest'},
        'Occitanie': {'lat': 43.6047, 'lon': 3.8787, 'zone': 'Sud'},
        'Pays de la Loire': {'lat': 47.4634, 'lon': -0.7842, 'zone': 'Ouest'},
        'Provence-Alpes-Côte d\'Azur': {'lat': 43.9352, 'lon': 6.0679, 'zone': 'Sud-Est'}
    }
    
    # 3. AJOUT des coordonnées (mapping flexible pour gérer différents noms)
    df_pop['latitude'] = df_pop['region'].map(lambda x: 
        next((coords['lat'] for region, coords in coordonnees_regions.items() 
              if region.lower() in str(x).lower() or str(x).lower() in region.lower()), None))
    
    df_pop['longitude'] = df_pop['region'].map(lambda x: 
        next((coords['lon'] for region, coords in coordonnees_regions.items() 
              if region.lower() in str(x).lower() or str(x).lower() in region.lower()), None))
    
    df_pop['zone_geographique'] = df_pop['region'].map(lambda x: 
        next((coords['zone'] for region, coords in coordonnees_regions.items() 
              if region.lower() in str(x).lower() or str(x).lower() in region.lower()), 'Autre'))
    
    # 4. MÉTRIQUES CALCULÉES pour Power BI
    if 'population_totale' in df_pop.columns:
        df_pop['densite_population'] = df_pop['population_totale'] / 1000  # Densité par km²
    
    if 'population_6_17_ans' in df_pop.columns:
        df_pop['ratio_pediatrique'] = (df_pop['population_6_17_ans'] / df_pop['population_totale'] * 100).round(2)
    
    # 5. ID UNIQUE pour relations Power BI
    df_pop['region_id'] = range(1, len(df_pop) + 1)
    
    # 6. SAUVEGARDE enrichie (GARDE le nom original + version enrichie)
    df_pop.to_csv('processed/population_insee_generated_enrichi.csv', index=False, encoding='utf-8-sig')
    
    # OPTIONNEL : Écrase l'original si vous voulez
    # df_pop.to_csv('raw/population_insee_generated.csv', index=False, encoding='utf-8-sig')
    
    print(f"✅ Fichier enrichi créé : population_insee_generated_enrichi.csv")
    print(f"📊 Nouvelles colonnes : latitude, longitude, zone_geographique, region_id")
    print(f"🎯 Prêt pour import Power BI !")
    
    return df_pop

def creer_dim_regions_master():
    """
    Crée la table de dimension maître à partir du fichier enrichi
    """
    df_enrichi = pd.read_csv('processed/population_insee_generated_enrichi.csv')
    
    # Sélection des colonnes essentielles pour Power BI
    dim_regions = df_enrichi[['region_id', 'region', 'latitude', 'longitude', 
                             'zone_geographique', 'population_totale', 'densite_population']].copy()
    
    dim_regions.rename(columns={'region': 'region_nom'}, inplace=True)
    dim_regions.to_csv('powerbi/dim_regions.csv', index=False, encoding='utf-8-sig')
    
    print("✅ dim_regions.csv créé pour Power BI")
    return dim_regions

# EXÉCUTION
if __name__ == "__main__":
    print("🚀 Enrichissement population_insee_generated.csv")
    
    # Créer les dossiers si nécessaire
    Path('processed').mkdir(exist_ok=True)
    Path('powerbi').mkdir(exist_ok=True)
    
    # Enrichir le fichier population
    df_enrichi = enrichir_population_insee()
    
    # Créer la dimension regions pour Power BI
    dim_regions = creer_dim_regions_master()
    
    print("\n🎯 PRÊT POUR POWER BI !")
    print("Fichiers à importer dans Power BI :")
    print("1. powerbi/dim_regions.csv")
    print("2. processed/dataset_epidemio_revolutionary_25k.csv")
    print("3. raw/methylphenidate_generated.csv")
    print("4. raw/pauvrete_regionale_generated.csv")
    print("5. raw/densite_pedopsychiatres_generated.csv")
