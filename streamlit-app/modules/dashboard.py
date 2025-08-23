"""
Module Dashboard Principal - Observatoire TDAH
Vue d'ensemble des données et KPIs principaux
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time

def show_dashboard():
    """Affichage du dashboard principal avec KPIs et visualisations"""
    
    st.markdown("# 🏠 Dashboard Principal")
    st.markdown("Vue d'ensemble de l'Observatoire TDAH France")
    
    # KPIs principaux en haut de page
    create_main_kpis()
    
    # Layout en colonnes pour les graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        show_epidemiology_overview()
        show_regional_distribution()
    
    with col2:
        show_prescription_trends()
        show_quality_indicators()
    
    # Section détaillée
    st.markdown("---")
    show_detailed_analysis()

def create_main_kpis():
    """Créer les KPIs principaux"""
    
    st.markdown("## 📊 Indicateurs Clés")
    
    # Simulation de données réalistes (à remplacer par vraies données)
    kpis_data = {
        'prevalence_national': 5.9,  # %
        'cas_estimes': 642000,  # personnes
        'regions_couvertes': 13,  # sur 13 régions
        'derniere_maj': '2024-08-23',
        'prescriptions_annuelles': 89000,
        'specialistes_actifs': 1240
    }
    
    # Affichage des KPIs en 4 colonnes
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📈 Prévalence Nationale",
            value=f"{kpis_data['prevalence_national']}%",
            delta="0.2% vs 2023"
        )
        
    with col2:
        st.metric(
            label="👥 Cas Estimés",
            value=f"{kpis_data['cas_estimes']:,}".replace(',', ' '),
            delta="+12,000 vs 2023"
        )
        
    with col3:
        st.metric(
            label="🗺️ Couverture",
            value=f"{kpis_data['regions_couvertes']}/13 régions",
            delta="100% couverture"
        )
        
    with col4:
        st.metric(
            label="💊 Prescriptions/an",
            value=f"{kpis_data['prescriptions_annuelles']:,}".replace(',', ' '),
            delta="+5.2% vs 2023"
        )

def show_epidemiology_overview():
    """Aperçu épidémiologique"""
    
    st.markdown("### 📈 Évolution Épidémiologique")
    
    # Données simulées d'évolution
    years = list(range(2018, 2025))
    prevalence = [4.8, 5.1, 5.3, 5.6, 5.9, 6.1, 6.0]
    diagnostic_rate = [42, 45, 48, 52, 55, 58, 61]
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=['Prévalence (%)', 'Taux de Diagnostic (%)'],
        specs=[[{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Graphique prévalence
    fig.add_trace(
        go.Scatter(x=years, y=prevalence, mode='lines+markers',
                  name='Prévalence', line=dict(color='#667eea', width=3)),
        row=1, col=1
    )
    
    # Graphique taux diagnostic
    fig.add_trace(
        go.Scatter(x=years, y=diagnostic_rate, mode='lines+markers',
                  name='Taux Diagnostic', line=dict(color='#764ba2', width=3)),
        row=1, col=2
    )
    
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

def show_regional_distribution():
    """Distribution régionale"""
    
    st.markdown("### 🗺️ Répartition Régionale")
    
    # Données simulées par région
    regions_data = pd.DataFrame({
        'Region': ['Île-de-France', 'Auvergne-Rhône-Alpes', 'Hauts-de-France', 
                  'Nouvelle-Aquitaine', 'Occitanie', 'Grand Est', 'PACA'],
        'Prevalence': [6.2, 5.8, 6.5, 5.4, 5.9, 6.1, 5.7],
        'Cases': [125000, 89000, 78000, 67000, 72000, 58000, 69000]
    })
    
    # Graphique en barres
    fig = px.bar(regions_data, x='Region', y='Prevalence', 
                 title='Prévalence TDAH par Région (%)',
                 color='Prevalence', color_continuous_scale='Viridis')
    
    fig.update_layout(height=350, xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

def show_prescription_trends():
    """Tendances des prescriptions"""
    
    st.markdown("### 💊 Tendances Prescriptions")
    
    # Données temporelles simulées
    months = pd.date_range('2023-01', periods=20, freq='M')
    methylphenidate = np.random.normal(7500, 500, 20)
    atomoxetine = np.random.normal(1200, 150, 20)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=months, y=methylphenidate,
        mode='lines+markers',
        name='Méthylphénidate',
        line=dict(color='#ff6b6b', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=months, y=atomoxetine,
        mode='lines+markers', 
        name='Atomoxétine',
        line=dict(color='#4ecdc4', width=2)
    ))
    
    fig.update_layout(
        height=350,
        title='Évolution Mensuelle des Prescriptions',
        xaxis_title='Période',
        yaxis_title='Nombre de Prescriptions'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_quality_indicators():
    """Indicateurs qualité des données"""
    
    st.markdown("### 🔍 Qualité des Données")
    
    # Indicateurs de qualité simulés
    quality_metrics = {
        'Complétude': 94.2,
        'Exactitude': 96.8,
        'Cohérence': 91.5,
        'Actualité': 98.1
    }
    
    # Graphique radar
    categories = list(quality_metrics.keys())
    values = list(quality_metrics.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Qualité Données',
        line_color='#667eea'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        height=350,
        title="Score Qualité des Données (%)"
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_detailed_analysis():
    """Section d'analyse détaillée"""
    
    st.markdown("## 🔬 Analyses Détaillées")
    
    # Tabs pour différentes analyses
    tab1, tab2, tab3 = st.tabs(["📊 Démographie", "🏥 Système de Soins", "💰 Économie"])
    
    with tab1:
        show_demographic_analysis()
    
    with tab2:
        show_healthcare_analysis()
        
    with tab3:
        show_economic_analysis()

def show_demographic_analysis():
    """Analyse démographique"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution par âge
        age_groups = ['6-11 ans', '12-17 ans', '18-25 ans', '26-35 ans', '36+ ans']
        percentages = [35, 28, 18, 12, 7]
        
        fig = px.pie(values=percentages, names=age_groups, 
                     title='Répartition par Groupe d\'Âge')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Ratio garçons/filles
        gender_data = pd.DataFrame({
            'Age_Group': ['6-11 ans', '12-17 ans', '18+ ans'],
            'Garcons': [3.2, 2.8, 1.9],
            'Filles': [1.0, 1.0, 1.0]
        })
        
        fig = go.Figure(data=[
            go.Bar(name='Ratio Garçons', x=gender_data['Age_Group'], y=gender_data['Garcons']),
            go.Bar(name='Ratio Filles', x=gender_data['Age_Group'], y=gender_data['Filles'])
        ])
        
        fig.update_layout(barmode='group', title='Ratio Garçons/Filles par Âge')
        st.plotly_chart(fig, use_container_width=True)

def show_healthcare_analysis():
    """Analyse du système de soins"""
    
    st.markdown("#### 🏥 Accessibilité aux Soins")
    
    # Densité de spécialistes par région
    specialists_data = pd.DataFrame({
        'Region': ['IDF', 'AURA', 'HdF', 'NA', 'OCC', 'GE', 'PACA'],
        'Pedopsychiatres': [0.85, 0.62, 0.45, 0.58, 0.67, 0.71, 0.76],
        'Neurologues': [1.2, 0.8, 0.6, 0.7, 0.9, 0.8, 1.1]
    })
    
    fig = px.bar(specialists_data, x='Region', 
                 y=['Pedopsychiatres', 'Neurologues'],
                 title='Densité Spécialistes (pour 100k habitants)',
                 barmode='group')
    
    st.plotly_chart(fig, use_container_width=True)

def show_economic_analysis():
    """Analyse économique"""
    
    st.markdown("#### 💰 Impact Économique")
    
    # Coûts par catégorie
    costs_data = pd.DataFrame({
        'Categorie': ['Médicaments', 'Consultations', 'Hospitalisations', 'Rééducation'],
        'Cout_Annuel': [450000000, 280000000, 120000000, 95000000]
    })
    
    fig = px.treemap(costs_data, path=['Categorie'], values='Cout_Annuel',
                     title='Répartition des Coûts Annuels (€)')
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Métriques économiques
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Coût Total/an", "945M€", delta="+3.2%")
    with col2:
        st.metric("Coût/patient/an", "1,472€", delta="+1.8%")
    with col3:
        st.metric("Part Sécu", "76.4%", delta="-0.5%")