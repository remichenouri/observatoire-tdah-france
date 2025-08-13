import requests
import json
from datetime import datetime

def validate_apis():
    """Valide l'accès aux APIs gouvernementales françaises"""
    
    apis_to_test = [
        {
            "name": "Data.gouv.fr - Santé",
            "url": "https://www.data.gouv.fr/api/1/datasets/?q=santé",
            "expected_keys": ["data", "total"]
        },
        {
            "name": "API Géo - Régions",
            "url": "https://geo.api.gouv.fr/regions",
            "expected_keys": ["nom", "code"]
        },
        {
            "name": "Data.gouv.fr - TDAH",
            "url": "https://www.data.gouv.fr/api/1/datasets/?q=TDAH",
            "expected_keys": ["data", "total"]
        }
    ]
    
    results = {}
    
    for api in apis_to_test:
        try:
            response = requests.get(api["url"], timeout=10)
            
            # Vérification du statut HTTP
            assert response.status_code == 200, f"HTTP {response.status_code}"
            
            # Vérification du contenu JSON
            data = response.json()
            
            # Vérification des clés attendues
            if api["expected_keys"]:
                if isinstance(data, list) and len(data) > 0:
                    for key in api["expected_keys"]:
                        assert key in data[0], f"Clé manquante: {key}"
                elif isinstance(data, dict):
                    for key in api["expected_keys"]:
                        assert key in data, f"Clé manquante: {key}"
            
            results[api["name"]] = {
                "status": "✅ SUCCESS",
                "response_time": response.elapsed.total_seconds(),
                "data_size": len(str(data))
            }
            
        except Exception as e:
            results[api["name"]] = {
                "status": f"❌ ERROR: {str(e)}",
                "response_time": None,
                "data_size": None
            }
    
    return results

def generate_validation_report():
    """Génère un rapport de validation"""
    
    print("🔍 VALIDATION DE L'INFRASTRUCTURE - Observatoire TDAH France")
    print("="*60)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    results = validate_apis()
    
    for api_name, result in results.items():
        print(f"📡 {api_name}")
        print(f"   Statut: {result['status']}")
        if result['response_time']:
            print(f"   Temps de réponse: {result['response_time']:.2f}s")
            print(f"   Taille des données: {result['data_size']} caractères")
        print()
    
    # Vérification globale
    all_success = all("SUCCESS" in result['status'] for result in results.values())
    
    if all_success:
        print("🎉 TOUTES LES APIs SONT ACCESSIBLES")
        print("✅ Infrastructure validée avec succès")
    else:
        print("⚠️  CERTAINES APIs NE SONT PAS ACCESSIBLES")
        print("❌ Vérifiez votre connexion internet et réessayez")
    
    return all_success

if __name__ == "__main__":
    success = generate_validation_report()
    exit(0 if success else 1)
