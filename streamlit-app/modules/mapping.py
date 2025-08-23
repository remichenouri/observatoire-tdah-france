"""
Module Cartographie - Observatoire TDAH
Visualisations géographiques et analyses territoriales
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
import geopandas as gpd
from datetime import datetime
import json

def show_mapping():
    """Interface principale de cartographie"""
    
    st.markdown("# 🗺️ Cartographie TDAH France")
    st.markdown("Visualisations géographiques et analyses territoriales")
    
    # Navigation par onglets
    tab1, tab2, tab3, tab4 = st.tabs([
        "🇫🇷 Vue France", 
        "📍 Densité Médicale",
        "📊 Analyses Régionales", 
        "🔍 Comparaisons"
    ])
    
    with tab1:
        show_france_overview()
    
    with tab2:
        show_medical_density_map()
        
    with tab3:
        show_regional_analysis()
        
    with tab4:
        show_regional_comparisons()

def show_france_overview():
    """Vue d'ensemble de la France"""
    
    st.markdown("### 🇫🇷 Prévalence TDAH par Région")
    
    # Sélecteurs
    col1, col2, col3 = st.columns(3)
    
    with col1:
        metric = st.selectbox(
            "Métrique à afficher",
            ["Prévalence (%)", "Cas Estimés", "Taux Diagnostic (%)", "Prescriptions/1000hab"]
        )
    
    with col2:
        year = st.selectbox("Année", [2024, 2023, 2022, 2021])
        
    with col3:
        age_group = st.selectbox("Groupe d'âge", ["Tous", "6-11 ans", "12-17 ans", "18+ ans"])
    
    # Génération des données géographiques simulées
    regions_data = generate_regions_data(metric, year, age_group)
    
    # Carte interactive avec Folium
    create_france_choropleth_map(regions_data, metric)
    
    # Statistiques rapides
    show_geographic_stats(regions_data, metric)

def generate_regions_data(metric, year, age_group):
    """Génération des données géographiques simulées"""
    
    # Données des régions françaises
    regions = {
        'Île-de-France': {'lat': 48.8566, 'lon': 2.3522, 'code': '11'},
        'Centre-Val de Loire': {'lat': 47.7516, 'lon': 1.6751, 'code': '24'},
        'Bourgogne-Franche-Comté': {'lat': 47.2805, 'lon': 4.9950, 'code': '27'},
        'Normandie': {'lat': 49.1829, 'lon': -0.3707, 'code': '28'},
        'Hauts-de-France': {'lat': 49.6649, 'lon': 2.5282, 'code': '32'},
        'Grand Est': {'lat': 48.6921, 'lon': 6.1844, 'code': '44'},
        'Pays de la Loire': {'lat': 47.7633, 'lon': -0.3299, 'code': '52'},
        'Bretagne': {'lat': 48.2020, 'lon': -2.9326, 'code': '53'},
        'Nouvelle-Aquitaine': {'lat': 45.7640, 'lon': 0.8034, 'code': '75'},
        'Occitanie': {'lat': 43.8927, 'lon': 2.0435, 'code': '76'},
        'Auvergne-Rhône-Alpes': {'lat': 45.4472, 'lon': 4.3854, 'code': '84'},
        'Provence-Alpes-Côte d\'Azur': {'lat': 43.9352, 'lon': 6.0679, 'code': '93'},
        'Corse': {'lat': 42.0396, 'lon': 9.0129, 'code': '94'}
    }
    
    # Simulation des valeurs selon la métrique
    np.random.seed(42)
    
    data = []
    for region_name, region_info in regions.items():
        
        if metric == "Prévalence (%)":
            value = np.random.normal(5.9, 1.2)  # Moyenne 5.9%, écart-type 1.2%
            value = max(3.0, min(9.0, value))  # Borner entre 3% et 9%
            
        elif metric == "Cas Estimés":
            # Basé sur la population régionale approximative
            pop_base = np.random.randint(500000, 12000000)
            value = int(pop_base * np.random.uniform(0.04, 0.08))  # 4-8% de la population
            
        elif metric == "Taux Diagnostic (%)":
            value = np.random.normal(58, 12)  # Moyenne 58%, écart-type 12%
            value = max(30, min(85, value))  # Borner entre 30% et 85%
            
        else:  # Prescriptions/1000hab
            value = np.random.normal(12.5, 3.2)  # Moyenne 12.5 pour 1000, écart-type 3.2
            value = max(5, min(25, value))  # Borner entre 5 et 25
        
        data.append({
            'Region': region_name,
            'Code': region_info['code'],
            'Latitude': region_info['lat'],
            'Longitude': region_info['lon'],
            'Value': round(value, 1),
            'Metric': metric
        })
    
    return pd.DataFrame(data)

def create_france_choropleth_map(regions_data, metric):
    """Création de la carte choroplèthe de France"""
    
    # Création de la carte Folium
    m = folium.Map(
        location=[46.6034, 1.8883],  # Centre de la France
        zoom_start=6,
        tiles='OpenStreetMap'
    )
    
    # Déterminer la palette de couleurs selon la métrique
    if "Prévalence" in metric or "Taux" in metric:
        colormap = folium.LinearColormap(
            colors=['green', 'yellow', 'orange', 'red'],
            vmin=regions_data['Value'].min(),
            vmax=regions_data['Value'].max()
        )
    else:
        colormap = folium.LinearColormap(
            colors=['lightblue', 'blue', 'darkblue'],
            vmin=regions_data['Value'].min(),
            vmax=regions_data['Value'].max()
        )
    
    # Ajouter les marqueurs pour chaque région
    for _, row in regions_data.iterrows():
        
        # Couleur selon la valeur
        color = colormap(row['Value'])
        
        # Taille du marqueur selon la valeur (normalisée)
        min_val, max_val = regions_data['Value'].min(), regions_data['Value'].max()
        normalized_size = 10 + 30 * (row['Value'] - min_val) / (max_val - min_val)
        
        # Popup avec informations détaillées
        popup_text = f"""
        <b>{row['Region']}</b><br>
        {metric}: <b>{row['Value']}</b><br>
        Code région: {row['Code']}<br>
        <small>Cliquer pour plus de détails</small>
        """
        
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=normalized_size,
            popup=folium.Popup(popup_text, max_width=200),
            color='white',
            weight=2,
            fillColor=color,
            fillOpacity=0.7
        ).add_to(m)
    
    # Ajouter la légende
    colormap.caption = f'{metric} par région'
    colormap.add_to(m)
    
    # Affichage dans Streamlit
    map_data = st_folium(m, width=700, height=500)
    
    # Affichage des détails si région sélectionnée
    if map_data['last_object_clicked']:
        show_region_details(regions_data, map_data['last_object_clicked'])

def show_region_details(regions_data, clicked_data):
    """Affichage des détails d'une région sélectionnée"""
    
    st.markdown("#### 📍 Région Sélectionnée")
    
    # Identifier la région cliquée (approximation par coordonnées)
    if 'lat' in clicked_data and 'lng' in clicked_data:
        clicked_lat, clicked_lng = clicked_data['lat'], clicked_data['lng']
        
        # Trouver la région la plus proche
        distances = regions_data.apply(
            lambda row: ((row['Latitude'] - clicked_lat)**2 + (row['Longitude'] - clicked_lng)**2)**0.5,
            axis=1
        )
        
        closest_region = regions_data.loc[distances.idxmin()]
        
        # Affichage des informations
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Région", closest_region['Region'])
            st.metric(closest_region['Metric'], f"{closest_region['Value']}")
            
        with col2:
            # Classement de la région
            rank = (regions_data['Value'] > closest_region['Value']).sum() + 1
            st.metric("Classement", f"{rank}/{len(regions_data)}")
            
            # Écart à la moyenne nationale
            national_avg = regions_data['Value'].mean()
            deviation = closest_region['Value'] - national_avg
            st.metric("Vs Moyenne Nationale", f"{deviation:+.1f}")

def show_geographic_stats(regions_data, metric):
    """Affichage des statistiques géographiques"""
    
    st.markdown("#### 📊 Statistiques Nationales")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Moyenne", f"{regions_data['Value'].mean():.1f}")
        
    with col2:
        st.metric("Médiane", f"{regions_data['Value'].median():.1f}")
        
    with col3:
        st.metric("Min", f"{regions_data['Value'].min():.1f}")
        
    with col4:
        st.metric("Max", f"{regions_data['Value'].max():.1f}")
    
    # Top et Bottom 3 régions
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 🔝 Top 3 Régions")
        top_3 = regions_data.nlargest(3, 'Value')[['Region', 'Value']]
        for _, row in top_3.iterrows():
            st.write(f"**{row['Region']}**: {row['Value']}")
    
    with col2:
        st.markdown("##### 🔻 Bottom 3 Régions")
        bottom_3 = regions_data.nsmallest(3, 'Value')[['Region', 'Value']]
        for _, row in bottom_3.iterrows():
            st.write(f"**{row['Region']}**: {row['Value']}")

def show_medical_density_map():
    """Carte de la densité médicale"""
    
    st.markdown("### 🏥 Densité des Spécialistes TDAH")
    
    # Sélecteurs
    col1, col2 = st.columns(2)
    
    with col1:
        specialist_type = st.selectbox(
            "Type de spécialiste",
            ["Pédopsychiatres", "Neurologues", "Psychiatres", "Tous"]
        )
        
    with col2:
        density_metric = st.selectbox(
            "Métrique",
            ["Nombre absolu", "Pour 100k habitants", "Pour 1000 enfants"]
        )
    
    # Génération des données de densité médicale
    medical_density_data = generate_medical_density_data(specialist_type, density_metric)
    
    # Carte spécialisée pour la densité médicale
    create_medical_density_map_viz(medical_density_data, specialist_type, density_metric)
    
    # Analyses de corrélation
    show_density_correlation_analysis(medical_density_data)

def generate_medical_density_data(specialist_type, density_metric):
    """Génération des données de densité médicale"""
    
    regions = [
        'Île-de-France', 'Centre-Val de Loire', 'Bourgogne-Franche-Comté',
        'Normandie', 'Hauts-de-France', 'Grand Est', 'Pays de la Loire',
        'Bretagne', 'Nouvelle-Aquitaine', 'Occitanie', 'Auvergne-Rhône-Alpes',
        'Provence-Alpes-Côte d\'Azur', 'Corse'
    ]
    
    np.random.seed(42)
    
    data = []
    for region in regions:
        
        # Simulation basée sur les caractéristiques régionales
        if region == 'Île-de-France':
            base_density = 1.8  # Plus forte densité en IdF
        elif region in ['Provence-Alpes-Côte d\'Azur', 'Auvergne-Rhône-Alpes']:
            base_density = 1.2  # Densité élevée dans les grandes métropoles
        elif region in ['Corse', 'Centre-Val de Loire']:
            base_density = 0.4  # Densité faible dans les régions peu peuplées
        else:
            base_density = 0.8  # Densité moyenne
        
        # Variation selon le type de spécialiste
        if specialist_type == "Pédopsychiatres":
            multiplier = 0.6
        elif specialist_type == "Neurologues":
            multiplier = 1.2
        elif specialist_type == "Psychiatres":
            multiplier = 1.8
        else:  # Tous
            multiplier = 1.0
        
        # Calcul de la valeur finale avec variation aléatoire
        value = base_density * multiplier * np.random.uniform(0.7, 1.3)
        
        # Ajustement selon la métrique
        if density_metric == "Nombre absolu":
            # Conversion en nombre absolu (approximation basée sur la population)
            pop_factor = np.random.randint(500000, 12000000) / 1000000
            value = int(value * pop_factor * 100)
            
        elif density_metric == "Pour 1000 enfants":
            value *= 2.5  # Plus de spécialistes par 1000 enfants que par 100k habitants
        
        data.append({
            'Region': region,
            'Density': round(value, 2),
            'Specialist_Type': specialist_type,
            'Metric': density_metric
        })
    
    return pd.DataFrame(data)

def create_medical_density_map_viz(data, specialist_type, density_metric):
    """Visualisation de la densité médicale"""
    
    # Graphique en barres horizontales
    fig = px.bar(
        data.sort_values('Density', ascending=True),
        x='Density',
        y='Region',
        orientation='h',
        title=f'{specialist_type} - {density_metric}',
        color='Density',
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Carte de chaleur
    st.markdown("#### 🌡️ Carte de Chaleur")
    
    # Créer une matrice pour la heatmap (simulation)
    heatmap_data = data.pivot_table(
        index='Region', 
        values='Density',
        aggfunc='mean'
    ).fillna(0)
    
    fig_heatmap = px.imshow(
        heatmap_data.values.reshape(1, -1),
        x=heatmap_data.index,
        aspect='auto',
        color_continuous_scale='RdYlBu_r',
        title="Intensité de la Densité Médicale"
    )
    
    fig_heatmap.update_layout(height=200)
    fig_heatmap.update_yaxis(showticklabels=False)
    st.plotly_chart(fig_heatmap, use_container_width=True)

def show_density_correlation_analysis(medical_data):
    """Analyse des corrélations avec la densité médicale"""
    
    st.markdown("#### 🔗 Corrélations avec Autres Indicateurs")
    
    # Simulation de données corrélées
    np.random.seed(42)
    
    correlation_data = medical_data.copy()
    
    # Ajouter des variables corrélées
    correlation_data['Prevalence_TDAH'] = (
        5.9 + (correlation_data['Density'] - correlation_data['Density'].mean()) * 0.3 +
        np.random.normal(0, 0.5, len(correlation_data))
    ).clip(3, 9)
    
    correlation_data['Taux_Diagnostic'] = (
        58 + (correlation_data['Density'] - correlation_data['Density'].mean()) * 5 +
        np.random.normal(0, 8, len(correlation_data))
    ).clip(30, 85)
    
    correlation_data['Temps_Attente_Jours'] = (
        90 - (correlation_data['Density'] - correlation_data['Density'].mean()) * 15 +
        np.random.normal(0, 20, len(correlation_data))
    ).clip(15, 180)
    
    # Graphiques de corrélation
    col1, col2 = st.columns(2)
    
    with col1:
        fig_corr1 = px.scatter(
            correlation_data,
            x='Density',
            y='Prevalence_TDAH',
            hover_name='Region',
            title='Densité vs Prévalence TDAH',
            trendline='ols'
        )
        st.plotly_chart(fig_corr1, use_container_width=True)
    
    with col2:
        fig_corr2 = px.scatter(
            correlation_data,
            x='Density',
            y='Temps_Attente_Jours',
            hover_name='Region',
            title='Densité vs Temps d\'Attente',
            trendline='ols'
        )
        st.plotly_chart(fig_corr2, use_container_width=True)
    
    # Matrice de corrélation
    corr_matrix = correlation_data[['Density', 'Prevalence_TDAH', 'Taux_Diagnostic', 'Temps_Attente_Jours']].corr()
    
    fig_matrix = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect='auto',
        color_continuous_scale='RdBu_r',
        title='Matrice de Corrélation'
    )
    
    st.plotly_chart(fig_matrix, use_container_width=True)

def show_regional_analysis():
    """Analyses détaillées par région"""
    
    st.markdown("### 📊 Analyses Régionales Détaillées")
    
    # Sélection de région pour analyse détaillée
    regions = [
        'Île-de-France', 'Auvergne-Rhône-Alpes', 'Hauts-de-France',
        'Nouvelle-Aquitaine', 'Occitanie', 'Grand Est', 'Provence-Alpes-Côte d\'Azur',
        'Pays de la Loire', 'Bretagne', 'Normandie', 'Centre-Val de Loire',
        'Bourgogne-Franche-Comté', 'Corse'
    ]
    
    selected_region = st.selectbox("Sélectionner une région", regions)
    
    # Analyses multi-dimensionnelles pour la région sélectionnée
    show_region_deep_dive(selected_region)
    
    # Comparaison avec la moyenne nationale
    show_region_vs_national(selected_region)

def show_region_deep_dive(region_name):
    """Analyse approfondie d'une région"""
    
    st.markdown(f"#### 🔍 Analyse Détaillée: {region_name}")
    
    # Génération de données complètes pour la région
    np.random.seed(hash(region_name) % 2**32)
    
    # Données simulées multi-dimensionnelles
    region_data = {
        'Population_Totale': np.random.randint(1000000, 12000000),
        'Population_6_17_ans': np.random.randint(150000, 2000000),
        'Prevalence_TDAH': round(np.random.normal(5.9, 1.2), 1),
        'Cas_Estimes': np.random.randint(20000, 400000),
        'Taux_Diagnostic': round(np.random.normal(58, 12), 1),
        'Pediatres': np.random.randint(50, 800),
        'Pedopsychiatres': np.random.randint(5, 150),
        'Neurologues': np.random.randint(20, 300),
        'Temps_Attente_Moyens': np.random.randint(30, 120),
        'Prescriptions_Annuelles': np.random.randint(5000, 80000),
        'Cout_Total_Annuel': np.random.randint(10000000, 200000000)
    }
    
    # Affichage des KPIs régionaux
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Population 6-17 ans", f"{region_data['Population_6_17_ans']:,}".replace(',', ' '))
        st.metric("Prévalence TDAH", f"{region_data['Prevalence_TDAH']}%")
        
    with col2:
        st.metric("Cas Estimés", f"{region_data['Cas_Estimes']:,}".replace(',', ' '))
        st.metric("Taux Diagnostic", f"{region_data['Taux_Diagnostic']}%")
        
    with col3:
        st.metric("Pédopsychiatres", region_data['Pedopsychiatres'])
        st.metric("Temps d'Attente", f"{region_data['Temps_Attente_Moyens']} jours")
        
    with col4:
        st.metric("Prescriptions/an", f"{region_data['Prescriptions_Annuelles']:,}".replace(',', ' '))
        st.metric("Coût Total/an", f"{region_data['Cout_Total_Annuel']/1000000:.1f}M€")
    
    # Graphiques régionaux
    col1, col2 = st.columns(2)
    
    with col1:
        # Répartition des spécialistes
        specialists_data = pd.DataFrame({
            'Specialite': ['Pédiatres', 'Pédopsychiatres', 'Neurologues'],
            'Nombre': [region_data['Pediatres'], region_data['Pedopsychiatres'], region_data['Neurologues']]
        })
        
        fig_specialists = px.pie(
            specialists_data,
            values='Nombre',
            names='Specialite',
            title='Répartition des Spécialistes'
        )
        st.plotly_chart(fig_specialists, use_container_width=True)
    
    with col2:
        # Évolution temporelle simulée
        months = pd.date_range('2023-01', periods=12, freq='M')
        evolution_data = pd.DataFrame({
            'Mois': months,
            'Nouveaux_Diagnostics': np.random.poisson(region_data['Cas_Estimes']/12, 12),
            'Prescriptions': np.random.poisson(region_data['Prescriptions_Annuelles']/12, 12)
        })
        
        fig_evolution = px.line(
            evolution_data,
            x='Mois',
            y=['Nouveaux_Diagnostics', 'Prescriptions'],
            title='Évolution Mensuelle 2023'
        )
        st.plotly_chart(fig_evolution, use_container_width=True)

def show_region_vs_national(region_name):
    """Comparaison région vs moyenne nationale"""
    
    st.markdown(f"#### ⚖️ {region_name} vs Moyenne Nationale")
    
    # Données simulées pour la comparaison
    np.random.seed(hash(region_name) % 2**32)
    
    comparison_metrics = {
        'Prévalence (%)': [np.random.normal(5.9, 1.2), 5.9],
        'Taux Diagnostic (%)': [np.random.normal(58, 12), 58],
        'Spécialistes/100k': [np.random.normal(0.8, 0.3), 0.8],
        'Temps Attente (j)': [np.random.normal(75, 25), 75],
        'Prescriptions/1000': [np.random.normal(12.5, 3), 12.5]
    }
    
    # Graphique radar de comparaison
    categories = list(comparison_metrics.keys())
    region_values = [comparison_metrics[cat][0] for cat in categories]
    national_values = [comparison_metrics[cat][1] for cat in categories]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=region_values,
        theta=categories,
        fill='toself',
        name=region_name,
        line_color='blue'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=national_values,
        theta=categories,
        fill='toself',
        name='Moyenne Nationale',
        line_color='red',
        opacity=0.6
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(max(region_values), max(national_values)) * 1.2]
            )),
        showlegend=True,
        title="Comparaison Multi-dimensionnelle"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Tableau de comparaison détaillé
    comparison_df = pd.DataFrame({
        'Métrique': categories,
        region_name: [round(val, 1) for val in region_values],
        'Moyenne Nationale': national_values,
        'Écart': [round(reg - nat, 1) for reg, nat in zip(region_values, national_values)],
        'Écart (%)': [round((reg - nat) / nat * 100, 1) for reg, nat in zip(region_values, national_values)]
    })
    
    st.dataframe(comparison_df, use_container_width=True)

def show_regional_comparisons():
    """Comparaisons entre régions"""
    
    st.markdown("### 🔍 Comparaisons Inter-Régionales")
    
    # Sélection de régions à comparer
    regions = [
        'Île-de-France', 'Auvergne-Rhône-Alpes', 'Hauts-de-France',
        'Nouvelle-Aquitaine', 'Occitanie', 'Grand Est', 'Provence-Alpes-Côte d\'Azur',
        'Pays de la Loire', 'Bretagne', 'Normandie', 'Centre-Val de Loire',
        'Bourgogne-Franche-Comté', 'Corse'
    ]
    
    selected_regions = st.multiselect(
        "Sélectionner des régions à comparer (max 5)",
        regions,
        default=['Île-de-France', 'Auvergne-Rhône-Alpes', 'Hauts-de-France'],
        max_selections=5
    )
    
    if len(selected_regions) >= 2:
        
        # Génération des données comparatives
        comparison_data = generate_comparative_data(selected_regions)
        
        # Métriques sélectionnables pour comparaison
        metrics_available = [
            'Prévalence (%)', 'Taux Diagnostic (%)', 'Densité Spécialistes',
            'Temps d\'Attente (j)', 'Prescriptions/1000hab', 'Coût/habitant (€)'
        ]
        
        selected_metric = st.selectbox("Métrique à comparer", metrics_available)
        
        # Visualisation comparative
        create_regional_comparison_viz(comparison_data, selected_metric, selected_regions)
        
        # Analyses statistiques
        show_comparison_statistics(comparison_data, selected_regions)
    
    else:
        st.info("Sélectionnez au moins 2 régions pour effectuer une comparaison")

def generate_comparative_data(regions):
    """Génération des données pour comparaisons"""
    
    comparative_data = {}
    
    for region in regions:
        np.random.seed(hash(region) % 2**32)
        
        comparative_data[region] = {
            'Prévalence (%)': round(np.random.normal(5.9, 1.2), 1),
            'Taux Diagnostic (%)': round(np.random.normal(58, 12), 1),
            'Densité Spécialistes': round(np.random.normal(0.8, 0.3), 2),
            'Temps d\'Attente (j)': round(np.random.normal(75, 25), 0),
            'Prescriptions/1000hab': round(np.random.normal(12.5, 3), 1),
            'Coût/habitant (€)': round(np.random.normal(145, 40), 0)
        }
    
    return comparative_data

def create_regional_comparison_viz(data, metric, regions):
    """Visualisations comparatives entre régions"""
    
    # Extraction des données pour la métrique sélectionnée
    metric_data = pd.DataFrame({
        'Region': regions,
        'Value': [data[region][metric] for region in regions]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Graphique en barres
        fig_bar = px.bar(
            metric_data,
            x='Region',
            y='Value',
            title=f'Comparaison - {metric}',
            color='Value',
            color_continuous_scale='Viridis'
        )
        fig_bar.update_xaxis(tickangle=45)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        # Graphique radar pour comparaison multi-métriques
        if len(regions) <= 4:  # Limiter pour la lisibilité
            
            fig_radar = go.Figure()
            
            metrics = ['Prévalence (%)', 'Taux Diagnostic (%)', 'Densité Spécialistes']
            
            for region in regions:
                values = [data[region][m] for m in metrics]
                
                fig_radar.add_trace(go.Scatterpolar(
                    r=values,
                    theta=metrics,
                    fill='toself',
                    name=region,
                    opacity=0.6
                ))
            
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True)),
                showlegend=True,
                title="Comparaison Multi-Métriques"
            )
            
            st.plotly_chart(fig_radar, use_container_width=True)
        
        else:
            # Graphique en ligne pour éviter la surcharge
            fig_line = px.line(
                metric_data,
                x='Region',
                y='Value',
                title=f'Évolution - {metric}',
                markers=True
            )
            fig_line.update_xaxis(tickangle=45)
            st.plotly_chart(fig_line, use_container_width=True)

def show_comparison_statistics(data, regions):
    """Statistiques de comparaison"""
    
    st.markdown("#### 📊 Statistiques Comparatives")
    
    # Créer un DataFrame complet pour les analyses
    full_data = pd.DataFrame(data).T
    
    # Statistiques descriptives
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 📈 Statistiques Descriptives")
        stats = full_data.describe()
        st.dataframe(stats.round(2))
    
    with col2:
        st.markdown("##### 🏆 Classements")
        
        # Classement pour chaque métrique
        rankings = {}
        for metric in full_data.columns:
            sorted_regions = full_data.sort_values(metric, ascending=False).index.tolist()
            rankings[metric] = {region: idx+1 for idx, region in enumerate(sorted_regions)}
        
        # Affichage du classement pour une métrique exemple
        ranking_df = pd.DataFrame({
            'Région': regions,
            'Rang Prévalence': [rankings['Prévalence (%)'][region] for region in regions],
            'Rang Diagnostic': [rankings['Taux Diagnostic (%)'][region] for region in regions]
        })
        
        st.dataframe(ranking_df)
    
    # Corrélations entre métriques
    st.markdown("##### 🔗 Corrélations entre Métriques")
    
    corr_matrix = full_data.corr()
    
    fig_corr = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect='auto',
        color_continuous_scale='RdBu_r',
        title='Matrice de Corrélation entre Métriques'
    )
    
    st.plotly_chart(fig_corr, use_container_width=True)