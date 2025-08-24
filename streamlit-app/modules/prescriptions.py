"""
Module Prescriptions - Observatoire TDAH
Analyses des prescriptions et médicaments TDAH
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

def show_prescriptions():
    """Interface principale des prescriptions TDAH"""
    
    st.markdown("# 💊 Prescriptions TDAH France")
    st.markdown("Analyses des prescriptions et médicaments TDAH")
    
    # Placeholder content
    st.info("🚧 **Module en construction**")
    st.markdown("""
    Ce module contiendra :
    - 📈 Évolution des prescriptions TDAH 2018-2024
    - 💊 Analyses par type de médicament (Méthylphénidate, Lisdexamphétamine, etc.)
    - 🗺️ Répartition géographique des prescriptions
    - 👥 Données démographiques (âge, sexe)
    - ⚠️ Alertes sur l'augmentation des prescriptions
    """)
    
    # Generate sample data for testing
    generate_sample_prescription_data()

def generate_sample_prescription_data():
    """Génère des données d'exemple pour tester l'interface"""
    
    st.markdown("### 📊 Données d'Exemple")
    
    # Sample prescription evolution data
    years = list(range(2018, 2025))
    prescriptions = [1246934, 1380000, 1520000, 1680000, 1850000, 2040000, 2250000]
    
    # Create DataFrame
    df_prescriptions = pd.DataFrame({
        'Année': years,
        'Prescriptions': prescriptions,
        'Croissance (%)': [0] + [round((prescriptions[i] - prescriptions[i-1])/prescriptions[i-1]*100, 1) 
                                 for i in range(1, len(prescriptions))]
    })
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total 2024", 
            f"{prescriptions[-1]:,}".replace(',', ' '), 
            delta=f"+{df_prescriptions['Croissance (%)'].iloc[-1]}%"
        )
    
    with col2:
        total_growth = round((prescriptions[-1] - prescriptions[0])/prescriptions[0]*100, 1)
        st.metric("Croissance 2018-2024", f"{total_growth}%", delta="Préoccupant")
    
    with col3:
        avg_annual = round(df_prescriptions['Croissance (%)'][1:].mean(), 1)
        st.metric("Croissance Annuelle Moyenne", f"{avg_annual}%")
    
    # Chart
    fig = px.line(
        df_prescriptions, 
        x='Année', 
        y='Prescriptions',
        title="Évolution des Prescriptions TDAH en France",
        markers=True
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Data table
    st.markdown("#### 📋 Données Détaillées")
    st.dataframe(df_prescriptions, use_container_width=True)
