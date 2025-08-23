# 🧠 Observatoire TDAH - Application Streamlit

Application web sophistiquée pour la visualisation, l'analyse et le monitoring des données TDAH en France. Cette application moderne offre une interface intuitive pour les professionnels de santé, chercheurs et administrateurs.

## 🚀 Fonctionnalités Principales

### 📊 Dashboard Principal
- **KPIs en temps réel** : Prévalence, cas estimés, couverture régionale
- **Visualisations interactives** : Graphiques Plotly, cartes, métriques
- **Analyses multi-dimensionnelles** : Démographie, système de soins, économie
- **Monitoring de la qualité** : Scores de qualité des données en continu

### 🔄 Collecte de Données Automatisée
- **Sources multiples** : DREES, INSEE, ANSM, données hospitalières
- **Interface de monitoring** : Suivi en temps réel des collectes
- **Configuration flexible** : Paramétrage des APIs et fréquences
- **Historique complet** : Traçabilité de toutes les opérations

### 🔍 Gestion de la Qualité
- **Inspection automatique** : Détection des anomalies et valeurs manquantes
- **Nettoyage intelligent** : ML pour l'imputation des données
- **Validation en continu** : Tests de cohérence et d'intégrité
- **Rapports détaillés** : Export des analyses qualité

### 🗺️ Cartographie Interactive
- **Visualisations géographiques** : Folium, données régionales
- **Densité médicale** : Répartition des spécialistes
- **Analyses territoriales** : Comparaisons inter-régionales

### 💊 Analyses des Prescriptions
- **Tendances temporelles** : Évolution des prescriptions
- **Analyses par molécule** : Méthylphénidate, Atomoxétine, etc.
- **Profils patients** : Segmentation par âge, région, pathologie

### 🔧 Administration Avancée
- **Gestion utilisateurs** : Rôles, permissions, authentification
- **Configuration système** : APIs, paramètres, notifications
- **Monitoring technique** : CPU, mémoire, services
- **Maintenance** : Sauvegardes, nettoyage, optimisation

## 🏗️ Architecture Technique

### Structure Modulaire
```
observatoire-tdah-streamlit/
├── app.py                          # Application principale
├── requirements.txt                # Dépendances Python
├── README.md                      # Documentation
├── .streamlit/
│   └── config.toml               # Configuration Streamlit
├── modules/                      # Modules fonctionnels
│   ├── dashboard.py             # Dashboard principal
│   ├── data_collection.py       # Collecte de données
│   ├── data_quality.py          # Qualité des données
│   ├── epidemiology.py          # Analyses épidémiologiques
│   ├── mapping.py               # Cartographie
│   ├── prescriptions.py         # Analyses prescriptions
│   └── admin.py                 # Administration
├── utils/                       # Utilitaires
│   ├── __init__.py
│   ├── data_loader.py           # Chargement des données
│   ├── visualization.py         # Fonctions de visualisation
│   ├── config.py                # Configuration globale
│   └── constants.py             # Constantes du projet
├── core/                        # Logique métier
│   ├── __init__.py
│   ├── observatoire_collector.py # Collecteur principal
│   ├── standardisation.py       # Standardisation des données
│   ├── missing_values.py        # Gestion valeurs manquantes
│   └── inspection.py            # Inspection des données
└── data/                        # Données et cache
    ├── raw/                     # Données brutes
    ├── processed/               # Données traitées
    └── cache/                   # Cache temporaire
```

### Technologies Utilisées
- **Frontend** : Streamlit 1.28+, Plotly, Folium
- **Data Science** : Pandas 2.0+, NumPy, Scikit-learn
- **Visualisation** : Plotly Express, Seaborn, Matplotlib
- **Base de données** : SQLAlchemy, PostgreSQL
- **APIs** : Requests, authentification OAuth2
- **Déploiement** : Docker, Streamlit Cloud

## 🔧 Installation et Configuration

### 1. Prérequis
```bash
# Python 3.9+ requis
python --version
# Git installé
git --version
```

### 2. Clonage et Setup
```bash
# Cloner le repository Observatoire TDAH
git clone https://github.com/votre-username/observatoire-tdah.git
cd observatoire-tdah

# Créer le dossier Streamlit
mkdir streamlit-app
cd streamlit-app

# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement (Windows)
venv\Scripts\activate
# Ou sur Linux/Mac
source venv/bin/activate
```

### 3. Installation des Dépendances
```bash
# Installer les packages requis
pip install -r requirements.txt

# Vérifier l'installation
streamlit --version
```

### 4. Structure des Dossiers
```bash
# Créer la structure complète
mkdir -p modules utils core data/{raw,processed,cache} .streamlit

# Copier les fichiers fournis
# app.py, requirements.txt, README.md dans le répertoire racine
# Modules Python dans leurs dossiers respectifs
```

### 5. Configuration
```bash
# Créer le fichier de configuration Streamlit
cat > .streamlit/config.toml << EOF
[global]
developmentMode = false

[server]
runOnSave = true
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
EOF
```

### 6. Variables d'Environnement
```bash
# Créer le fichier .env pour les clés API
cat > .env << EOF
# API Keys (remplacer par vos vraies clés)
DREES_API_KEY=your_drees_api_key
INSEE_API_KEY=your_insee_api_key
ANSM_API_KEY=your_ansm_api_key

# Base de données
DATABASE_URL=postgresql://user:password@localhost/observatoire_tdah

# Configuration
DEBUG_MODE=false
ADMIN_PASSWORD=your_secure_admin_password
SECRET_KEY=your_secret_key_for_sessions
EOF
```

## 🚀 Lancement de l'Application

### Mode Développement
```bash
# Lancer l'application en mode développement
streamlit run app.py

# Ou avec des options spécifiques
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
```

### Mode Production
```bash
# Installer Gunicorn pour la production
pip install gunicorn

# Lancer avec Gunicorn (optionnel, Streamlit peut tourner seul)
streamlit run app.py --server.headless=true --server.port=8501
```

### Docker (Recommandé pour Production)
```dockerfile
# Créer le Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
# Build et run avec Docker
docker build -t observatoire-tdah-streamlit .
docker run -p 8501:8501 observatoire-tdah-streamlit
```

## 🔗 Intégration avec le Projet Existant

### 1. Intégration des Collecteurs
```python
# Dans core/observatoire_collector.py
# Utiliser votre classe ObservatoireTDAHCollector existante
from your_existing_project.observatoire_collector import ObservatoireTDAHCollector

# Adapter l'interface Streamlit pour utiliser vos vrais collecteurs
collector = ObservatoireTDAHCollector()
data = collector.collecter_toutes_donnees()
```

### 2. Intégration Base de Données
```python
# Configuration de la base de données
import sqlalchemy as sa
from sqlalchemy import create_engine

# Utiliser votre schéma de base existant
engine = create_engine(os.getenv('DATABASE_URL'))

# Adapter les requêtes pour vos tables
def load_epidemiology_data():
    query = """
    SELECT region_code, prevalence_rate, cases_estimated
    FROM your_epidemiology_table
    WHERE date_collected >= current_date - interval '30 days'
    """
    return pd.read_sql(query, engine)
```

### 3. Intégration APIs
```python
# Utiliser vos configurations API existantes
from your_project.config import API_CREDENTIALS

# Adapter les collecteurs dans data_collection.py
def collect_drees_data():
    headers = {'Authorization': f'Bearer {API_CREDENTIALS["drees"]}'}
    # Votre logique de collecte existante
```

## 📊 Utilisation de l'Application

### Interface Utilisateur
1. **Navigation** : Menu latéral avec 7 modules principaux
2. **Dashboard** : Vue d'ensemble avec KPIs temps réel
3. **Collecte** : Monitoring et lancement des collectes
4. **Qualité** : Inspection et nettoyage des données
5. **Analyses** : Visualisations épidémiologiques avancées
6. **Cartographie** : Visualisations géographiques interactives
7. **Administration** : Gestion complète du système

### Authentification
```python
# Mode démonstration (à remplacer en production)
# Admin : admin / tdah2024
# Utilisateur : demo / demo123

# Intégrer votre système d'authentification existant
def authenticate_user(username, password):
    # Votre logique d'authentification
    return validate_credentials(username, password)
```

## 🛠️ Personnalisation et Extension

### Ajout de Nouveaux Modules
```python
# Créer un nouveau module dans modules/
def show_new_module():
    st.markdown("# 🆕 Nouveau Module")
    # Votre logique métier

# Ajouter dans app.py
elif page == "🆕 Nouveau Module":
    from modules.new_module import show_new_module
    show_new_module()
```

### Personnalisation des Visualisations
```python
# Dans utils/visualization.py
def create_custom_plot(data, plot_type):
    # Vos visualisations personnalisées
    fig = px.scatter(data, x='age', y='severity')
    return fig
```

### Ajout de Sources de Données
```python
# Dans modules/data_collection.py
def add_custom_data_source():
    # Interface pour ajouter vos sources spécifiques
    source_config = {
        'name': st.text_input("Nom de la source"),
        'url': st.text_input("URL de l'API"),
        'auth_type': st.selectbox("Type d'auth", ["API Key", "OAuth2"])
    }
```

## 🔒 Sécurité et Bonnes Pratiques

### Authentification Sécurisée
```python
# Remplacer l'authentification de démo par un vrai système
import streamlit_authenticator as stauth

# Configuration avec hachage des mots de passe
config = {
    'credentials': {
        'usernames': {
            'admin': {
                'email': 'admin@observatoire-tdah.fr',
                'name': 'Administrateur',
                'password': '$2b$12$...',  # Hash bcrypt
            }
        }
    }
}

authenticator = stauth.Authenticate(config)
```

### Protection des Données
```python
# Chiffrement des données sensibles
import cryptography.fernet as fernet

key = os.getenv('ENCRYPTION_KEY')
cipher = fernet.Fernet(key)

# Chiffrer les données sensibles avant stockage
encrypted_data = cipher.encrypt(sensitive_data.encode())
```

### Gestion des Sessions
```python
# Sessions sécurisées avec timeout
if 'session_start' not in st.session_state:
    st.session_state.session_start = datetime.now()

# Vérifier l'expiration
session_duration = datetime.now() - st.session_state.session_start
if session_duration > timedelta(hours=8):
    # Forcer la re-authentification
    st.session_state.authenticated = False
```

## 📈 Performance et Optimisation

### Cache Streamlit
```python
# Utiliser le cache pour les données lourdes
@st.cache_data(ttl=3600)  # Cache 1 heure
def load_epidemiology_data():
    # Chargement des données coûteuses
    return pd.read_sql(query, connection)

@st.cache_resource
def init_database_connection():
    # Initialisation connexion DB (partagée)
    return create_engine(DATABASE_URL)
```

### Optimisation des Visualisations
```python
# Échantillonnage pour les gros datasets
def optimize_plot_data(df, max_points=10000):
    if len(df) > max_points:
        return df.sample(max_points)
    return df

# Utilisation de Plotly optimisé
fig = px.scatter(optimize_plot_data(df), x='x', y='y')
fig.update_layout(showlegend=False)  # Réduire la charge
```

## 🚀 Déploiement en Production

### Streamlit Cloud
```bash
# 1. Pusher le code sur GitHub
git add .
git commit -m "Application Streamlit Observatoire TDAH"
git push origin main

# 2. Déployer sur Streamlit Cloud
# - Aller sur share.streamlit.io
# - Connecter votre repository GitHub
# - Spécifier app.py comme fichier principal
# - Configurer les secrets (API keys, etc.)
```

### Heroku
```bash
# Créer le Procfile
echo "web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

# Déploiement
heroku create observatoire-tdah-app
git push heroku main
```

### AWS/Azure
```bash
# Configuration Docker pour cloud
docker build -t observatoire-tdah .
docker tag observatoire-tdah your-registry/observatoire-tdah:latest
docker push your-registry/observatoire-tdah:latest

# Déploiement avec Kubernetes ou Container Instances
```

## 📝 Maintenance et Monitoring

### Logs et Monitoring
```python
# Configuration du logging
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Dans vos fonctions
def collect_data():
    logger.info("Début de collecte de données")
    try:
        # Logique de collecte
        logger.info(f"Collecte réussie: {len(data)} enregistrements")
    except Exception as e:
        logger.error(f"Erreur collecte: {str(e)}")
```

### Métriques d'Usage
```python
# Tracking des interactions utilisateurs
def track_user_action(action, user_id, details=None):
    metrics = {
        'timestamp': datetime.now(),
        'action': action,
        'user_id': user_id,
        'details': details
    }
    
    # Sauvegarder en base ou envoyer à un service d'analytics
    save_user_metrics(metrics)
```

### Sauvegarde Automatique
```python
# Script de sauvegarde (crontab ou scheduled task)
def backup_system():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Sauvegarde base de données
    os.system(f'pg_dump {DATABASE_URL} > backup_{timestamp}.sql')
    
    # Sauvegarde fichiers de données
    shutil.make_archive(f'data_backup_{timestamp}', 'zip', 'data/')
    
    # Upload vers stockage cloud (AWS S3, Azure Blob, etc.)
    upload_to_cloud_storage(f'backup_{timestamp}.sql')
```

## 🤝 Support et Contact

### Documentation Technique
- **API Documentation** : `/docs` endpoint
- **Code Source** : Repository GitHub avec README détaillé
- **Exemples** : Notebooks Jupyter dans `/examples`

### Support Utilisateurs
- **Guide Utilisateur** : Documentation intégrée dans l'app
- **FAQ** : Section aide dans le menu
- **Tickets** : Système de ticketing intégré pour le support

### Contact Développement
- **Email** : dev@observatoire-tdah.fr
- **Issues GitHub** : Pour bugs et améliorations
- **Documentation** : Wiki du projet pour guides avancés

---

## 🎯 Prêt pour l'Emploi

Cette application Streamlit sophistiquée démontre :

✅ **Expertise technique** : Python avancé, Streamlit, Data Science stack complet  
✅ **Architecture modulaire** : Code maintenable, extensible, bien structuré  
✅ **UI/UX professionnelle** : Interface moderne, responsive, intuitive  
✅ **Gestion de données** : ETL, qualité, visualisations interactives  
✅ **Bonnes pratiques** : Sécurité, performance, logging, tests  
✅ **Déploiement** : Docker, cloud-ready, CI/CD  
✅ **Documentation** : README complet, code commenté, guides utilisateur  

**Cette application constitue un portfolio technique impressionnant pour tout poste en Data Science, développement d'applications de santé, ou ingénierie logicielle !**