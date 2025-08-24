# Observatoire TDAH - Application Streamlit
"""
Application de visualisation et d'analyse des données TDAH en France
Auteur: Développé pour l'Observatoire TDAH
Version: 2.0
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Configuration de la page
st.set_page_config(
    page_title="Observatoire TDAH France",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/observatoire-tdah',
        'Report a bug': 'https://github.com/observatoire-tdah/issues',
        'About': '''# Observatoire TDAH France
        Application d'analyse et de visualisation des données TDAH en France.
        Développée pour améliorer la compréhension et le suivi du TDAH.
        **Version:** 2.0  
        **Technologies:** Streamlit, Pandas, Plotly, Scikit-learn'''
    }
)

# Ajout du répertoire racine au PYTHONPATH
root_dir = Path(__file__).parent
sys.path.append(str(root_dir))

# CSS personnalisé pour l'interface
def load_css():
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    
    .sidebar .stSelectbox > div > div {
        background-color: #f0f2f6;
    }
    
    .status-success {
        color: #28a745;
        font-weight: bold;
    }
    
    .kpi-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        color: white;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialisation de session
def init_session_state():
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False
    if 'current_data' not in st.session_state:
        st.session_state.current_data = None
    if 'user_preferences' not in st.session_state:
        st.session_state.user_preferences = {
            'theme': 'auto',
            'auto_refresh': True,
            'notification_level': 'info'
        }

# Navigation principale
def main():
    load_css()
    init_session_state()
    
    # En-tête principal
    st.markdown("""
    <div class="main-header">
        <h1>🧠 Observatoire TDAH France</h1>
        <p>Plateforme d'analyse et de suivi du Trouble Déficit de l'Attention avec Hyperactivité</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Barre latérale pour la navigation
    with st.sidebar:
        st.image(
            "https://via.placeholder.com/200x80/667eea/white?text=TDAH+Observatory",
            caption="Observatoire TDAH France"
        )
        st.markdown("---")
    
        # Menu principal
        page = st.selectbox(
            "🧭 Navigation",
            [
                "🏠 Dashboard Principal",
                "📊 Collecte de Données",
                "🔍 Qualité des Données",
                "📈 Analyses Épidémiologiques",
                "🗺️ Cartographie",
                "💊 Prescriptions",
                "🔧 Administration"
            ]
        )
        st.markdown("---")
    
        # Statut Système
        st.markdown('<div class="status-container">', unsafe_allow_html=True)
        st.markdown('<h4>📊 Statut Système</h4>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("APIs", "4/4", delta="Actives")
        with col2:
            st.metric("Données", "Fresh", delta="2h ago")
        st.markdown('</div>', unsafe_allow_html=True)
    
        # Statistiques rapides
        if st.session_state.data_loaded:
            st.markdown("### 📈 Aperçu Rapide")
            st.success("Données chargées avec succès")
        else:
            st.info("Chargez des données pour voir les statistiques")
    
    # Routage vers les modules
    if page == "🏠 Dashboard Principal":
        from modules.dashboard import show_dashboard
        show_dashboard()
    elif page == "📊 Collecte de Données":
        from modules.data_collection import show_data_collection
        show_data_collection()
    elif page == "🔍 Qualité des Données":
        from modules.data_quality import show_data_quality
        show_data_quality()
    elif page == "📈 Analyses Épidémiologiques":
        from modules.epidemiology import show_epidemiology
        show_epidemiology()
    elif page == "🗺️ Cartographie":
        from modules.mapping import show_mapping
        show_mapping()
    elif page == "💊 Prescriptions":
        from modules.prescriptions import show_prescriptions
        show_prescriptions()
    elif page == "🔧 Administration":
        from modules.admin import show_admin
        show_admin()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.8em;'>
        Observatoire TDAH France © 2024 | Développé avec ❤️ et Streamlit
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
