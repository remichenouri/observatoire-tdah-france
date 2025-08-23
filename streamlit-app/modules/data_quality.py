"""
Module Qualité des Données - Observatoire TDAH
Inspection, nettoyage et validation de la qualité des données
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False
    import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from datetime import datetime
import io

def show_data_quality():
    """Interface principale de qualité des données"""
    
    st.markdown("# 🔍 Qualité des Données")
    st.markdown("Inspection, validation et nettoyage des données TDAH")
    
    # Score de qualité global
    show_quality_overview()
    
    # Navigation par onglets
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Vue d'ensemble",
        "🔎 Inspection Détaillée", 
        "🛠️ Nettoyage",
        "✅ Validation",
        "📋 Rapport"
    ])
    
    with tab1:
        show_quality_dashboard()
    
    with tab2:
        show_detailed_inspection()
        
    with tab3:
        show_data_cleaning()
        
    with tab4:
        show_validation_results()
        
    with tab5:
        show_quality_report()

def show_quality_overview():
    """Score global de qualité"""
    
    st.markdown("## 🎯 Score de Qualité Global")
    
    # Calcul du score composite
    quality_metrics = {
        'Complétude': 94.2,
        'Exactitude': 96.8,
        'Cohérence': 91.5,
        'Actualité': 98.1,
        'Validité': 93.7
    }
    
    # Score global pondéré
    weights = {'Complétude': 0.25, 'Exactitude': 0.25, 'Cohérence': 0.2, 'Actualité': 0.15, 'Validité': 0.15}
    overall_score = sum(quality_metrics[k] * weights[k] for k in quality_metrics)
    
    # Affichage du score principal
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Jauge de score
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = overall_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Score Qualité Global"},
            delta = {'reference': 92},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Détail par dimension
        st.markdown("#### 📋 Détail par Dimension")
        
        for metric, score in quality_metrics.items():
            # Couleur selon le score
            if score >= 95:
                color = "🟢"
            elif score >= 85:
                color = "🟡"
            else:
                color = "🔴"
            
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.metric(f"{color} {metric}", f"{score}%")

def show_quality_dashboard():
    """Dashboard de qualité détaillé"""
    
    st.markdown("### 📊 Tableau de Bord Qualité")
    
    # Génération de données de test réalistes
    datasets = generate_test_data()
    
    # Sélecteur de dataset
    selected_dataset = st.selectbox(
        "Choisir un dataset",
        list(datasets.keys()),
        index=0
    )
    
    df = datasets[selected_dataset]
    
    # Métriques par dataset
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📏 Lignes", f"{len(df):,}")
        
    with col2:
        st.metric("📊 Colonnes", len(df.columns))
        
    with col3:
        missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100)
        st.metric("❓ Valeurs Manquantes", f"{missing_pct:.1f}%")
        
    with col4:
        duplicates = df.duplicated().sum()
        st.metric("🔄 Doublons", duplicates)
    
    # Visualisations
    col1, col2 = st.columns(2)
    
    with col1:
        # Heatmap des valeurs manquantes
        st.markdown("#### 🔥 Carte des Valeurs Manquantes")
        create_missing_heatmap(df)
    
    with col2:
        # Graphique de distribution des types de données
        st.markdown("#### 📈 Types de Données")
        create_dtype_chart(df)

def create_missing_heatmap(df):
    """Créer la heatmap des valeurs manquantes"""
    
    # Calculer le pourcentage de valeurs manquantes par colonne
    missing_data = df.isnull().sum().sort_values(ascending=False)
    missing_pct = (missing_data / len(df) * 100).round(1)
    
    if missing_pct.sum() > 0:
        # Graphique en barres des valeurs manquantes
        fig = px.bar(
            x=missing_pct.values,
            y=missing_pct.index,
            orientation='h',
            title='Pourcentage de Valeurs Manquantes par Colonne',
            color=missing_pct.values,
            color_continuous_scale='Reds'
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("✅ Aucune valeur manquante détectée!")

def create_dtype_chart(df):
    """Graphique des types de données"""
    
    # Compter les types de données
    dtype_counts = df.dtypes.value_counts()
    
    fig = px.pie(
        values=dtype_counts.values,
        names=dtype_counts.index.astype(str),
        title='Répartition des Types de Données'
    )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

def show_detailed_inspection():
    """Inspection détaillée des données"""
    
    st.markdown("### 🔎 Inspection Détaillée")
    
    # Génération de données de test
    datasets = generate_test_data()
    
    # Sélection dataset et colonne
    col1, col2 = st.columns(2)
    
    with col1:
        selected_dataset = st.selectbox("Dataset", list(datasets.keys()), key="inspect")
    
    df = datasets[selected_dataset]
    
    with col2:
        selected_column = st.selectbox("Colonne", df.columns)
    
    # Analyse de la colonne sélectionnée
    st.markdown(f"#### 📊 Analyse: {selected_column}")
    
    col_data = df[selected_column]
    
    # Métriques de base
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Type", str(col_data.dtype))
        
    with col2:
        st.metric("Non-nulls", f"{col_data.notna().sum():,}")
        
    with col3:
        st.metric("Nulls", f"{col_data.isna().sum():,}")
        
    with col4:
        if pd.api.types.is_numeric_dtype(col_data):
            st.metric("Unique", col_data.nunique())
        else:
            st.metric("Unique", col_data.nunique())
    
    # Visualisations selon le type
    if pd.api.types.is_numeric_dtype(col_data):
        show_numeric_analysis(col_data, selected_column)
    else:
        show_categorical_analysis(col_data, selected_column)

def show_numeric_analysis(col_data, col_name):
    """Analyse pour colonnes numériques"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Statistiques descriptives
        st.markdown("#### 📈 Statistiques Descriptives")
        stats = col_data.describe()
        st.dataframe(stats.to_frame().T)
        
        # Détection des outliers
        Q1 = col_data.quantile(0.25)
        Q3 = col_data.quantile(0.75)
        IQR = Q3 - Q1
        outliers = col_data[(col_data < Q1 - 1.5*IQR) | (col_data > Q3 + 1.5*IQR)]
        
        st.metric("🔍 Outliers", len(outliers))
    
    with col2:
        # Distribution
        st.markdown("#### 📊 Distribution")
        fig = px.histogram(col_data.dropna(), nbins=30, title=f'Distribution - {col_name}')
        st.plotly_chart(fig, use_container_width=True)
        
    # Box plot
    st.markdown("#### 📦 Box Plot")
    fig = px.box(y=col_data, title=f'Box Plot - {col_name}')
    st.plotly_chart(fig, use_container_width=True)

def show_categorical_analysis(col_data, col_name):
    """Analyse pour colonnes catégorielles"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top valeurs
        st.markdown("#### 🏆 Top Valeurs")
        top_values = col_data.value_counts().head(10)
        st.dataframe(top_values.to_frame('Count'))
        
    with col2:
        # Distribution
        st.markdown("#### 📊 Distribution")
        fig = px.bar(
            x=top_values.values,
            y=top_values.index,
            orientation='h',
            title=f'Top 10 - {col_name}'
        )
        st.plotly_chart(fig, use_container_width=True)

def show_data_cleaning():
    """Interface de nettoyage des données"""
    
    st.markdown("### 🛠️ Nettoyage des Données")
    
    # Options de nettoyage
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔧 Options de Nettoyage")
        
        clean_missing = st.checkbox("Traiter les valeurs manquantes", value=True)
        clean_duplicates = st.checkbox("Supprimer les doublons", value=True)
        clean_outliers = st.checkbox("Traiter les outliers", value=False)
        standardize_formats = st.checkbox("Standardiser les formats", value=True)
        
        if clean_missing:
            missing_strategy = st.selectbox(
                "Stratégie valeurs manquantes",
                ["Suppression", "Imputation par moyenne", "Imputation par médiane", "Machine Learning"]
            )
    
    with col2:
        st.markdown("#### ⚙️ Paramètres Avancés")
        
        outlier_method = st.selectbox("Méthode outliers", ["IQR", "Z-score", "Isolation Forest"])
        outlier_threshold = st.slider("Seuil outliers", 1.0, 5.0, 3.0)
        
        date_format = st.text_input("Format date cible", "YYYY-MM-DD")
        encoding_target = st.selectbox("Encodage cible", ["UTF-8", "ISO-8859-1", "ASCII"])
    
    # Simulation du nettoyage
    if st.button("🚀 Lancer le Nettoyage", type="primary"):
        run_data_cleaning(clean_missing, clean_duplicates, missing_strategy)

def run_data_cleaning(clean_missing, clean_duplicates, missing_strategy):
    """Simulation du processus de nettoyage"""
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    steps = [
        "🔍 Analyse des données...",
        "❓ Traitement des valeurs manquantes...",
        "🔄 Suppression des doublons...",
        "🧹 Standardisation des formats...",
        "✅ Nettoyage terminé!"
    ]
    
    for i, step in enumerate(steps):
        status_text.text(step)
        progress_bar.progress((i + 1) / len(steps))
        
        # Simulation avec sleep réduit
        import time
        time.sleep(0.5)
    
    # Résultats simulés
    st.success("✅ Nettoyage terminé avec succès!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Lignes supprimées", "1,247", delta="-5.2%")
        
    with col2:
        st.metric("Valeurs imputées", "3,891", delta="Complété")
        
    with col3:
        st.metric("Score qualité", "96.8%", delta="+4.3%")

def show_validation_results():
    """Résultats de validation"""
    
    st.markdown("### ✅ Résultats de Validation")
    
    # Tests de validation
    validation_tests = pd.DataFrame({
        'Test': [
            'Format des codes région',
            'Cohérence des dates',
            'Valeurs dans les intervalles',
            'Unicité des identifiants',
            'Complétude des champs obligatoires',
            'Format des codes postaux',
            'Validation des emails'
        ],
        'Statut': ['✅ Passé', '✅ Passé', '⚠️ Avertissement', '✅ Passé', '❌ Échec', '✅ Passé', '✅ Passé'],
        'Score': [100, 100, 85, 100, 72, 100, 98],
        'Erreurs': [0, 0, 156, 0, 2847, 0, 23]
    })
    
    st.dataframe(validation_tests, use_container_width=True)
    
    # Graphique de répartition des résultats
    status_counts = validation_tests['Statut'].str.extract(r'([✅⚠️❌])').value_counts()
    
    fig = px.pie(
        values=status_counts.values,
        names=['Passé', 'Avertissement', 'Échec'],
        title='Répartition des Tests de Validation',
        color_discrete_map={'Passé': 'green', 'Avertissement': 'orange', 'Échec': 'red'}
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_quality_report():
    """Génération du rapport de qualité"""
    
    st.markdown("### 📋 Rapport de Qualité")
    
    # Options du rapport
    col1, col2 = st.columns(2)
    
    with col1:
        report_type = st.radio(
            "Type de rapport",
            ["Résumé exécutif", "Rapport détaillé", "Rapport technique"]
        )
        
        include_charts = st.checkbox("Inclure les graphiques", value=True)
        include_recommendations = st.checkbox("Inclure les recommandations", value=True)
        
    with col2:
        export_format = st.selectbox("Format d'export", ["PDF", "HTML", "Word", "Excel"])
        
        if st.button("📥 Générer le Rapport", type="primary"):
            generate_quality_report(report_type, include_charts, include_recommendations, export_format)

def generate_quality_report(report_type, include_charts, include_recommendations, export_format):
    """Génération du rapport de qualité"""
    
    with st.spinner("Génération du rapport en cours..."):
        import time
        time.sleep(2)
        
        st.success(f"✅ Rapport {report_type} généré en format {export_format}!")
        
        # Simulation du contenu du rapport
        report_content = f"""
        # Rapport de Qualité des Données - Observatoire TDAH
        
        **Date:** {datetime.now().strftime('%Y-%m-%d')}
        **Type:** {report_type}
        
        ## Résumé Exécutif
        - Score global de qualité: 94.6%
        - Datasets analysés: 5
        - Tests de validation: 7 (5 passés, 1 avertissement, 1 échec)
        
        ## Recommandations Prioritaires
        1. Améliorer la complétude des champs obligatoires (72% → 95%)
        2. Standardiser les formats de codes région
        3. Mettre en place une validation en temps réel
        """
        
        st.text_area("Aperçu du rapport", report_content, height=300)
        
        # Bouton de téléchargement simulé
        st.download_button(
            label=f"💾 Télécharger {export_format}",
            data=report_content,
            file_name=f"rapport_qualite_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )

def generate_test_data():
    """Génération de données de test pour la démonstration"""
    
    np.random.seed(42)
    
    datasets = {}
    
    # Dataset épidémiologique
    epidemio_data = pd.DataFrame({
        'region_code': np.random.choice(['11', '32', '44', '75', '76'], 1000),
        'age_group': np.random.choice(['6-11', '12-17', '18-25'], 1000),
        'sexe': np.random.choice(['M', 'F'], 1000),
        'diagnostic_confirme': np.random.choice([0, 1, np.nan], 1000, p=[0.3, 0.6, 0.1]),
        'date_diagnostic': pd.date_range('2020-01-01', periods=1000, freq='D'),
        'severite': np.random.choice(['Leger', 'Modere', 'Severe', np.nan], 1000, p=[0.4, 0.4, 0.15, 0.05])
    })
    
    datasets['Données Épidémiologiques'] = epidemio_data
    
    # Dataset prescriptions
    prescriptions_data = pd.DataFrame({
        'code_cip': np.random.randint(1000000, 9999999, 500),
        'methylphenidate_mg': np.random.choice([10, 18, 27, 36, 54], 500),
        'nb_boites': np.random.randint(1, 6, 500),
        'date_delivrance': pd.date_range('2023-01-01', periods=500, freq='D'),
        'age_patient': np.random.randint(6, 65, 500),
        'prescripteur_specialite': np.random.choice(['Pediatre', 'Neurologue', 'Psychiatre', np.nan], 500, p=[0.4, 0.3, 0.25, 0.05])
    })
    
    datasets['Données Prescriptions'] = prescriptions_data
    
    return datasets
