"""
Module Collecte de Données - Observatoire TDAH
Interface pour la collecte, monitoring et gestion des sources de données
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import json

def show_data_collection():
    """Interface principale de collecte de données"""
    
    st.markdown("# 📊 Collecte de Données")
    st.markdown("Interface de gestion des sources et collecte automatisée")
    
    # Barre d'état en temps réel
    show_collection_status()
    
    # Navigation par onglets
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔄 Collecte Active", 
        "🎯 Sources de Données", 
        "⚙️ Configuration", 
        "📋 Historique"
    ])
    
    with tab1:
        show_active_collection()
    
    with tab2:
        show_data_sources()
        
    with tab3:
        show_collection_config()
        
    with tab4:
        show_collection_history()

def show_collection_status():
    """Affichage du statut de collecte en temps réel"""
    
    st.markdown("## 📈 Statut en Temps Réel")
    
    # Métriques de statut
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("📡 APIs Actives", "4/4", delta="100%")
    
    with col2:
        st.metric("⏱️ Dernière Collecte", "2h 15min", delta="Normal")
    
    with col3:
        st.metric("💾 Données Aujourd'hui", "2.3 GB", delta="+125 MB")
        
    with col4:
        st.metric("✅ Succès Rate", "98.5%", delta="+0.3%")
        
    with col5:
        st.metric("🚨 Erreurs", "2", delta="-5 vs hier")

def show_active_collection():
    """Interface de collecte active"""
    
    st.markdown("### 🔄 Collecte en Cours")
    
    # Contrôles de collecte
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        if st.button("🚀 Lancer Collecte Complète", type="primary"):
            run_full_collection()
    
    with col2:
        if st.button("⏸️ Pause"):
            st.info("Collecte mise en pause")
            
    with col3:
        if st.button("🔄 Actualiser"):
            st.rerun()
    
    # Barre de progression simulée
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Sources de données avec statut
    st.markdown("#### 📋 Sources de Données")
    
    sources_status = pd.DataFrame({
        'Source': [
            'Épidémiologie DREES',
            'Socio-économie INSEE', 
            'Densité Médicale',
            'Prescriptions ANSM',
            'Population INSEE'
        ],
        'Statut': ['🟢 Active', '🟢 Active', '🟡 En cours', '🟢 Active', '🟢 Active'],
        'Dernière_MAJ': [
            '2024-08-23 08:30',
            '2024-08-23 09:15',
            '2024-08-23 10:00',
            '2024-08-23 07:45',
            '2024-08-23 06:30'
        ],
        'Taille': ['2.1 MB', '1.8 MB', '3.4 MB', '5.2 MB', '1.2 MB'],
        'Qualité': [95, 92, 88, 97, 99]
    })
    
    st.dataframe(sources_status, use_container_width=True)

def run_full_collection():
    """Simulation d'une collecte complète"""
    
    with st.spinner("Collecte en cours..."):
        
        # Simulation étapes de collecte
        steps = [
            "🔍 Vérification des APIs...",
            "📥 Collecte Épidémiologie...",
            "📊 Collecte Socio-économie...", 
            "🏥 Collecte Densité Médicale...",
            "💊 Collecte Prescriptions...",
            "🔄 Consolidation des données...",
            "✅ Collecte terminée!"
        ]
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, step in enumerate(steps):
            status_text.text(step)
            progress_bar.progress((i + 1) / len(steps))
            time.sleep(0.5)
        
        st.success("✅ Collecte complète terminée avec succès!")
        
        # Affichage du résumé
        show_collection_summary()

def show_collection_summary():
    """Résumé de la collecte"""
    
    st.markdown("#### 📊 Résumé de la Collecte")
    
    summary_data = pd.DataFrame({
        'Métrique': [
            'Enregistrements collectés',
            'Fichiers générés',
            'Taille totale',
            'Durée de collecte',
            'Taux de réussite'
        ],
        'Valeur': [
            '24,567 lignes',
            '12 fichiers',
            '15.4 MB',
            '3 min 42 sec',
            '98.5%'
        ]
    })
    
    st.table(summary_data)

def show_data_sources():
    """Configuration des sources de données"""
    
    st.markdown("### 🎯 Gestion des Sources")
    
    # Ajout de nouvelle source
    with st.expander("➕ Ajouter une Nouvelle Source"):
        add_new_source()
    
    # Liste des sources existantes
    st.markdown("#### 📋 Sources Configurées")
    
    sources_config = {
        'DREES Épidémiologie': {
            'url': 'https://data.drees.solidarites-sante.gouv.fr/api',
            'type': 'API REST',
            'frequence': 'Mensuelle',
            'format': 'JSON',
            'authentification': 'API Key'
        },
        'INSEE Population': {
            'url': 'https://api.insee.fr/donnees-locales/V0.1',
            'type': 'API REST', 
            'frequence': 'Trimestrielle',
            'format': 'JSON',
            'authentification': 'OAuth 2.0'
        },
        'ANSM Prescriptions': {
            'url': 'https://base-donnees-publique.medicaments.gouv.fr',
            'type': 'API REST',
            'frequence': 'Mensuelle', 
            'format': 'CSV',
            'authentification': 'Open Data'
        }
    }
    
    for source_name, config in sources_config.items():
        with st.container():
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.markdown(f"**{source_name}**")
                st.caption(f"Type: {config['type']} | Fréq: {config['frequence']}")
                
            with col2:
                st.code(config['url'], language='text')
                
            with col3:
                if st.button(f"⚙️ Config", key=f"config_{source_name}"):
                    configure_source(source_name, config)
                    
            st.markdown("---")

def add_new_source():
    """Formulaire d'ajout de nouvelle source"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        source_name = st.text_input("Nom de la source")
        source_url = st.text_input("URL/Endpoint")
        source_type = st.selectbox("Type", ['API REST', 'CSV', 'Excel', 'Database'])
        
    with col2:
        freq = st.selectbox("Fréquence", ['Temps réel', 'Quotidienne', 'Hebdomadaire', 'Mensuelle'])
        auth_type = st.selectbox("Authentification", ['Aucune', 'API Key', 'OAuth 2.0', 'Basic Auth'])
        format_type = st.selectbox("Format", ['JSON', 'XML', 'CSV', 'Excel'])
    
    # Test de connexion
    if st.button("🧪 Tester la Connexion"):
        with st.spinner("Test en cours..."):
            time.sleep(2)
            st.success("✅ Connexion réussie!")
    
    if st.button("💾 Sauvegarder la Source"):
        st.success(f"✅ Source '{source_name}' ajoutée avec succès!")

def configure_source(source_name, config):
    """Configuration détaillée d'une source"""
    
    st.markdown(f"### ⚙️ Configuration: {source_name}")
    
    with st.form(f"config_form_{source_name}"):
        
        # Paramètres de connexion
        st.markdown("#### 🔌 Paramètres de Connexion")
        url = st.text_input("URL", value=config['url'])
        timeout = st.slider("Timeout (sec)", 5, 60, 30)
        retry_count = st.number_input("Tentatives", min_value=1, max_value=5, value=3)
        
        # Paramètres de collecte
        st.markdown("#### 📅 Planification")
        col1, col2 = st.columns(2)
        
        with col1:
            frequency = st.selectbox("Fréquence", ['Temps réel', 'Quotidienne', 'Hebdomadaire', 'Mensuelle'])
            
        with col2:
            time_slot = st.time_input("Heure de collecte", value=datetime.now().time())
        
        # Paramètres de qualité
        st.markdown("#### ✅ Contrôle Qualité")
        enable_validation = st.checkbox("Validation automatique", value=True)
        quality_threshold = st.slider("Seuil qualité (%)", 0, 100, 85)
        
        if st.form_submit_button("💾 Enregistrer Configuration"):
            st.success("Configuration sauvegardée!")

def show_collection_config():
    """Configuration globale de collecte"""
    
    st.markdown("### ⚙️ Configuration Globale")
    
    # Paramètres généraux
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔧 Paramètres Généraux")
        
        auto_collect = st.checkbox("Collecte automatique", value=True)
        parallel_jobs = st.slider("Jobs parallèles", 1, 8, 4)
        max_retries = st.slider("Tentatives max", 1, 10, 3)
        
    with col2:
        st.markdown("#### 📁 Stockage")
        
        storage_path = st.text_input("Répertoire de stockage", value="./data")
        max_storage = st.slider("Stockage max (GB)", 1, 100, 50)
        backup_enabled = st.checkbox("Sauvegarde automatique", value=True)
    
    # Paramètres de notification
    st.markdown("#### 📧 Notifications")
    
    col3, col4 = st.columns(2)
    
    with col3:
        email_notifications = st.checkbox("Notifications email", value=True)
        if email_notifications:
            email_address = st.text_input("Adresse email", placeholder="admin@observatoire-tdah.fr")
    
    with col4:
        webhook_enabled = st.checkbox("Webhook", value=False)
        if webhook_enabled:
            webhook_url = st.text_input("URL Webhook", placeholder="https://hooks.slack.com/...")
    
    # Bouton de sauvegarde
    if st.button("💾 Enregistrer Configuration", type="primary"):
        st.success("✅ Configuration sauvegardée!")

def show_collection_history():
    """Historique des collectes"""
    
    st.markdown("### 📋 Historique des Collectes")
    
    # Filtres
    col1, col2, col3 = st.columns(3)
    
    with col1:
        date_range = st.date_input("Période", value=[datetime.now() - timedelta(days=7), datetime.now()])
        
    with col2:
        source_filter = st.multiselect("Sources", ["Toutes", "DREES", "INSEE", "ANSM"], default=["Toutes"])
        
    with col3:
        status_filter = st.selectbox("Statut", ["Tous", "Succès", "Erreur", "En cours"])
    
    # Historique des collectes
    history_data = pd.DataFrame({
        'Timestamp': pd.date_range('2024-08-16', periods=20, freq='6H'),
        'Source': np.random.choice(['DREES', 'INSEE', 'ANSM'], 20),
        'Statut': np.random.choice(['✅ Succès', '❌ Erreur', '⏳ En cours'], 20, p=[0.8, 0.15, 0.05]),
        'Enregistrements': np.random.randint(1000, 10000, 20),
        'Durée': np.random.randint(30, 300, 20),
        'Taille': np.random.uniform(1.0, 5.0, 20).round(1)
    })
    
    # Affichage de l'historique
    st.dataframe(
        history_data.style.format({
            'Timestamp': lambda x: x.strftime('%Y-%m-%d %H:%M'),
            'Durée': lambda x: f"{x}s",
            'Taille': lambda x: f"{x} MB"
        }),
        use_container_width=True
    )
    
    # Graphique des collectes dans le temps
    fig = px.line(history_data, x='Timestamp', y='Enregistrements', 
                  color='Source', title='Volume de Collecte par Source')
    st.plotly_chart(fig, use_container_width=True)