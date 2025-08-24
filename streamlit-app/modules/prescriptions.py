import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime

def load_prescriptions_data(path: str) -> pd.DataFrame:
    """
    Charge et nettoie les données de prescriptions TDAH.
    Colonnes attendues : 
      - date_prescription (YYYY-MM-DD)
      - département
      - médicament (Méthylphénidate, Lisdexamfétamine, etc.)
      - âge_patient
      - sexe_patient
      - nombre_doses
    """
    df = pd.read_csv(path, parse_dates=['date_prescription'])
    df = df.dropna(subset=['date_prescription', 'département', 'médicament'])
    df['année'] = df['date_prescription'].dt.year
    df['mois'] = df['date_prescription'].dt.to_period('M')
    return df

def show_prescriptions():
    st.header("💊 Suivi des Prescriptions TDAH")
    st.markdown("""
    Ce module présente :
    - Évolution annuelle des prescriptions (2018–2024)  
    - Répartition par type de médicament  
    - Cartographie des volumes par département  
    - Profil démographique (âge, sexe)  
    - Alertes de hausse significative  
    """)

    # 1. Chargement
    data_file = st.sidebar.file_uploader("Téléverser le CSV des prescriptions", type=['csv'])
    if not data_file:
        st.warning("Veuillez importer un fichier CSV pour afficher les analyses.")
        return

    df = load_prescriptions_data(data_file)
    st.session_state.current_data = df

    # 2. KPI globaux
    col1, col2, col3 = st.columns(3)
    total_presc = len(df)
    années = sorted(df['année'].unique())
    dernières = df[df['année'] == max(années)]
    col1.metric("Prescriptions totales", f"{total_presc:,}")
    col2.metric("Années couvertes", f"{min(années)}–{max(années)}")
    col3.metric("Prescriptions {}" .format(max(années)), f"{len(dernières):,}")

    st.markdown("---")

    # 3. Évolution temporelle 2018–2024
    st.subheader("Évolution annuelle des prescriptions")
    hist = (df
            .groupby('année')
            .size()
            .reset_index(name='count')
            .sort_values('année'))
    fig1 = px.bar(hist,
                  x='année', y='count',
                  labels={'année': 'Année', 'count': 'Nombre de prescriptions'},
                  title="Prescriptions TDAH par année")
    st.plotly_chart(fig1, use_container_width=True)

    # 4. Analyse par médicament
    st.subheader("Répartition par type de médicament")
    meds = (df
            .groupby('médicament')
            .size()
            .reset_index(name='count')
            .sort_values('count', ascending=False))
    fig2 = px.pie(meds,
                  names='médicament', values='count',
                  title="Parts de marché par médicament")
    st.plotly_chart(fig2, use_container_width=True)

    # 5. Cartographie géographique
    st.subheader("Cartographie des prescriptions par département")
    dept_counts = (df
                   .groupby('département')
                   .size()
                   .reset_index(name='count'))
    # Utiliser un GeoJSON de la France disponible localement ou via URL
    geojson_path = "data/france_departements.geojson"
    try:
        fig3 = px.choropleth_mapbox(
            dept_counts, geojson=geojson_path, locations='département',
            featureidkey="properties.code", color='count',
            color_continuous_scale="Viridis", mapbox_style="carto-positron",
            zoom=4.5, center={"lat": 46.6, "lon": 2.5},
            labels={'count': 'Nb presc.'},
            title="Volume de prescriptions par département"
        )
        st.plotly_chart(fig3, use_container_width=True)
    except Exception as e:
        st.error(f"Erreur cartographie : {e}")

    # 6. Démographie
    st.subheader("Données démographiques")
    col_age, col_sex = st.columns(2)
    with col_age:
        age_dist = df['âge_patient'].dropna().astype(int)
        fig4 = px.histogram(age_dist,
                            nbins=20,
                            title="Distribution des âges")
        st.plotly_chart(fig4, use_container_width=True)
    with col_sex:
        sex_dist = (df
                    .groupby('sexe_patient')
                    .size()
                    .reset_index(name='count'))
        fig5 = px.bar(sex_dist, x='sexe_patient', y='count',
                      labels={'sexe_patient': 'Sexe', 'count': 'Nombre'},
                      title="Répartition par sexe")
        st.plotly_chart(fig5, use_container_width=True)

    # 7. Alertes d'augmentation
    st.subheader("⚠️ Alertes de hausse annuelle")
    seuil_pct = st.slider("Seuil d'augmentation (%)", 0, 100, 20)
    year_over_year = hist.copy()
    year_over_year['prev'] = year_over_year['count'].shift(1)
    year_over_year['pct_change'] = ((year_over_year['count'] - year_over_year['prev']) / year_over_year['prev']) * 100
    alerts = year_over_year[year_over_year['pct_change'] > seuil_pct]
    if alerts.empty:
        st.success("Aucune hausse supérieure à {} % détectée.".format(seuil_pct))
    else:
        for _, row in alerts.iterrows():
            st.warning(f"Entre {int(row['année']-1)} et {int(row['année'])} : +{row['pct_change']:.1f}%")

    # 8. Export des résultats
    st.markdown("---")
    if st.button("Exporter les statistiques clés"):
        stats = hist.merge(meds, how='cross')
        stats_csv = stats.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Télécharger CSV",
            data=stats_csv,
            file_name=f"stats_prescriptions_{datetime.now().date()}.csv",
            mime="text/csv"
        )
