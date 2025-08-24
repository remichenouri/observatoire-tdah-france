Observatoire TDAH France
Application Streamlit d’Observation et d’Analyse des Données TDAH
Plateforme interactive destinée à la visualisation, l’exploration et le suivi des tendances cliniques et médicamenteuses liées au Trouble du Déficit de l’Attention avec ou sans Hyperactivité (TDAH) en France.

🚀 Fonctionnalités principales
Tableaux de bord dynamiques
Visualisation des prescriptions et des prises en charge TDAH (2018–2024)

Filtres et segmentations
Par région, par type de traitement, par période

Graphiques interactifs
Séries temporelles, répartition géographique, histogrammes

Export de données
Téléchargement CSV / Excel pour analyses complémentaires

Rapports automatisés
Génération de rapports PDF & Power BI

📂 Structure du dépôt
text
├── .vscode/                # Configuration VS Code
├── config/                 # Fichiers de configuration
├── data/                   # Jeux de données bruts et nettoyés
│   ├── prescriptions_2018_2024.csv
│   └── …
├── notebooks/              # Jupyter notebooks exploratoires
├── power bi/               # Fichiers .pbix de tableaux de bord Power BI
├── reports/                # Rapports générés (PDF, HTML)
├── scripts/                # Scripts d’ingestion et de transformation
├── src/                    # Modules Python réutilisables
├── streamlit-app/          # Application Streamlit
│   ├── main.py             # Point d’entrée
│   ├── requirements.txt    # Dépendances
│   └── assets/             # Images et ressources statiques
├── tests/                  # Tests unitaires
├── create_notebooks.py     # Génération automatique de notebooks
├── README.md               # Présentation du projet
└── requirements.txt        # Dépendances globales
⚙️ Installation et déploiement
Cloner le dépôt

bash
git clone https://github.com/remichenouri/observatoire-tdah-france.git
cd observatoire-tdah-france
Créer un environnement virtuel

bash
python3 -m venv .venv
source .venv/bin/activate
Installer les dépendances

bash
pip install -r requirements.txt
Lancer l’application

bash
streamlit run streamlit-app/main.py
🛠️ Technologies et librairies
Langage : Python 3.9+

Framework Web : Streamlit

Data science : pandas, numpy, scikit-learn

Visualisation : matplotlib, seaborn, plotly

BI : Power BI Desktop

Tests : pytest

📈 Cas d’usage
Cliniciens et centres de soins
Suivi des prescriptions pour ajuster les protocoles thérapeutiques

Chercheurs et data scientists
Exploration des tendances longitudinales et analyses prédictives

Décideurs politiques
Évaluation des disparités régionales et impact des politiques de santé

🤝 Contribution
Les contributions sont les bienvenues !

Forker ce dépôt

Créer une branche feature/votre-fonctionnalité

Committer vos changements (git commit -m "Ajout : ma nouvelle fonctionnalité")

Pusher et ouvrir une Pull Request

📄 Licence
MIT License – voir le fichier LICENSE pour plus de détails.

✉️ Contact
Rémi Chenouri
Data Analyst – RSVA Normandie

Email : remi.chenouri@example.com

LinkedIn : linkedin.com/in/remichenouri

Observatoire TDAH France – Une initiative pour une meilleure compréhension et prise en charge du TDAH en France.
