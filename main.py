#!/usr/bin/env python3
"""
Point d'entrée principal pour la collecte Phase 2
Observatoire TDAH France
"""

import sys
import os

# Ajout du chemin src au PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.insert(0, src_path)

# Vérification de la structure des dossiers
def verifier_structure():
    """Vérifie que tous les dossiers nécessaires existent"""
    dossiers_requis = [
        'config',
        'data/raw',
        'data/processed',
        'data/cache',
        'src',
        'src/collectors'
    ]
    
    for dossier in dossiers_requis:
        if not os.path.exists(dossier):
            print(f"❌ Dossier manquant: {dossier}")
            os.makedirs(dossier, exist_ok=True)
            print(f"✅ Dossier créé: {dossier}")
    
    # Vérification des fichiers __init__.py
    init_files = ['src/__init__.py', 'src/collectors/__init__.py']
    for init_file in init_files:
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write("# Module Python")
            print(f"✅ Fichier créé: {init_file}")

def main():
    """Fonction principale"""
    print("🏥 === OBSERVATOIRE TDAH FRANCE - PHASE 2 ===")
    print("📊 Collecte de données validées")
    print("=" * 50)
    
    try:
        # Vérification structure
        verifier_structure()
        
        # Import après vérification structure
        try:
            from observatoire_collector import ObservatoireTDAHCollector
        except ImportError as e:
            print(f"❌ Erreur d'import: {e}")
            print("Vérifiez que tous les fichiers sont créés dans src/collectors/")
            return False
        
        # Initialisation du collecteur
        collector = ObservatoireTDAHCollector()
        
        # Exécution collecte complète
        df_resultat = collector.executer_collecte_complete()
        
        if df_resultat is not None:
            print("\n📋 RÉSUMÉ DES DONNÉES COLLECTÉES:")
            print(f"- {len(df_resultat)} régions analysées")
            print(f"- {df_resultat['cas_tdah_estimes'].sum():,} cas TDAH estimés")
            
            if 'taux_pauvrete' in df_resultat.columns:
                print(f"- Taux de pauvreté moyen: {df_resultat['taux_pauvrete'].mean():.1f}%")
            
            if 'temps_acces_chu_minutes' in df_resultat.columns:
                print(f"- Temps d'accès CHU moyen: {df_resultat['temps_acces_chu_minutes'].mean():.0f} minutes")
            
            if 'vulnerabilite_tdah' in df_resultat.columns:
                print("\n🔝 TOP 3 RÉGIONS - VULNÉRABILITÉ TDAH:")
                top_vulnerables = df_resultat.nlargest(3, 'vulnerabilite_tdah')
                for _, row in top_vulnerables.iterrows():
                    print(f"  {row['region']}: {row['vulnerabilite_tdah']:.1f} points")
            
            return True
        else:
            print("❌ Échec de la collecte")
            return False
            
    except Exception as e:
        print(f"❌ Erreur critique: {e}")
        print(f"Type d'erreur: {type(e).__name__}")
        import traceback
        print("Détails de l'erreur:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    input("Appuyez sur Entrée pour fermer...")  # Pause pour voir les résultats
    sys.exit(0 if success else 1)
