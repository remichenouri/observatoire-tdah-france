# apps/modules/prescriptions.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from statsmodels.tsa.seasonal import STL

def load_prescriptions_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=['date_prescription'])
    df = df.dropna(subset=['date_prescription', 'département', 'médicament', 'nombre_doses', 'âge_patient', 'sexe_patient'])
    df['année'] = df['date_prescription'].dt.year
    df['mois'] = df['date_prescription'].dt.to_period('M').dt.to_timestamp()
    return df

def make_stl_plot(stl_result):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=stl_result.observed.index, y=stl_result.observed.values, name='Observé'))
    fig.add_trace(go.Scatter(
        x=stl_result.trend.index, y=stl_result.trend.values, name='Tendance'))
    fig.add_trace(go.Scatter(
        x=stl_result.seasonal.index, y=stl_result.seasonal.values, name='Saisonnalité'))
    fig.update_layout(
        title="Décomposition STL de la Série Temporelle",
        xaxis_title="Date", yaxis_title="Nombre de prescriptions")
    return fig

def show_prescriptions():
    st.header("💊 Suivi Avancé des Prescriptions TDAH")

    file = st.sidebar.file_uploader("Importer CSV prescriptions", type="csv")
    if not file:
        st.warning("Importez un fichier CSV pour démarrer l'analyse.")
        return

    df = load_prescriptions_data(file)
    st.session_state.current_data = df
    st.session_state.data_loaded = True

    # KPI Cards
    total_presc = len(df)
    top_med = df['médicament'].mode()[0]
    mean_age = df['âge_patient'].mean()
    hist_annual = df.groupby('année').size().reset_index(name='count')
    annual_growth = hist_annual['count'].pct_change().iloc[-1] * 100

    col1, col2, col3, col4 = st.columns(4, gap="large")
    col1.metric("Total Prescriptions", f"{total_presc:,}")
    col2.metric("Médicament N°1", top_med)
    col3.metric("Âge moyen", f"{mean_age:.1f} ans")
    col4.metric("Croissance annuelle", f"{annual_growth:.1f}%", delta_color="inverse")

    st.markdown("---")

    # 1. Évolution mensuelle & cumul annuel
    monthly = df.groupby('mois').size().rename('count').reset_index()
    yearly_cum = df.groupby('année').size().cumsum().reset_index(name='cumul')
    fig_time = go.Figure()
    fig_time.add_trace(go.Scatter(
        x=monthly['mois'], y=monthly['count'], mode='lines', name='Mensuel'))
    fig_time.add_trace(go.Bar(
        x=yearly_cum['année'].astype(str), y=yearly_cum['cumul'],
        name='Cumul Annuel', opacity=0.5))
    fig_time.update_layout(
        title="Prescriptions Mensuelles & Cumul Annuel",
        xaxis_title="Date", yaxis_title="Nombre")
    st.plotly_chart(fig_time, use_container_width=True)

    # 2. Dosage moyen & quantiles
    st.subheader("Dosage par Médicament")
    dose_stats = df.groupby('médicament')['nombre_doses'] \
                   .agg(['mean','median', lambda x: x.quantile(0.25), lambda x: x.quantile(0.75)]) \
                   .rename(columns={'<lambda_0>':'Q1','<lambda_1>':'Q3'}) \
                   .reset_index()
    st.dataframe(dose_stats.style.format({
        'mean':'{:.1f}','median':'{:.1f}','Q1':'{:.1f}','Q3':'{:.1f}'
    }))

    # 3. Segmentation démographique
    st.subheader("Profil Démographique")
    age_bins = [0,6,12,18,30,45,60,100]
    df['tranche_age'] = pd.cut(df['âge_patient'], age_bins, right=False)
    demo = df.groupby(['tranche_age','sexe_patient']).size().reset_index(name='count')
    fig_demo = px.bar(
        demo, x='tranche_age', y='count', color='sexe_patient',
        barmode='group', title="Répartition par Âge & Sexe")
    st.plotly_chart(fig_demo, use_container_width=True)

    # 4. Décomposition saisonnière (STL)
    st.subheader("Analyse Saisonnière")
    ts = monthly.set_index('mois')['count']
    stl = STL(ts, period=12, robust=True).fit()
    st.plotly_chart(make_stl_plot(stl), use_container_width=True)

    # 5. Parts de marché dynamiques
    st.subheader("Parts de Marché Dynamiques")
    pivot = df.groupby(['mois','médicament']).size().unstack(fill_value=0)
    pct = pivot.divide(pivot.sum(axis=1), axis=0).reset_index()
    fig_dyn = px.area(
        pct, x='mois', y=pivot.columns,
        title="Évolution des Parts de Marché")
    st.plotly_chart(fig_dyn, use_container_width=True)

    # 6. Carte interactive
    st.subheader("Cartographie Interactive")
    geojson_path = "data/france_departements.geojson"
    med_filter = st.multiselect(
        "Filtrer par médicament", df['médicament'].unique(),
        default=list(df['médicament'].unique()))
    period = st.slider(
        "Période",
        min_value=monthly['mois'].min(),
        max_value=monthly['mois'].max(),
        value=(monthly['mois'].min(), monthly['mois'].max()),
        format="YYYY-MM"
    )
    df_map = df[
        (df['médicament'].isin(med_filter)) &
        (df['mois'].between(*period))
    ]
    dept_counts = df_map.groupby('département').size().reset_index(name='count')
    fig_map = px.choropleth_mapbox(
        dept_counts, geojson=geojson_path, locations='département',
        featureidkey="properties.code", color='count',
        color_continuous_scale="Viridis", mapbox_style="carto-positron",
        zoom=5, center={"lat":46.6, "lon":2.5},
        title="Prescriptions par Département"
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # 7. Tableau détaillé
    st.subheader("Tableau Détaillé")
    table = df[[
        'date_prescription','département','médicament',
        'âge_patient','sexe_patient','nombre_doses'
    ]]
    st.data_editor(table, use_container_width=True)

    # 8. Documentation
    st.markdown("---")
    st.markdown("### ℹ️ Informations Médicaments")
    st.markdown("""
    - **Méthylphénidate :** stimulant du SNC, usage pédiatrique majoritaire.  
    - **Lisdexamfétamine :** pro-drogue du dextroamphétamine.  
    - **Atomoxétine :** non-stimulant, alternative sans psychostimulant.
    """)
    st.markdown("[En savoir plus](https://www.has-sante.fr)")

    # 9. Export avancé
    st.markdown("---")
    if st.download_button(
        "Télécharger Tout (CSV)",
        df.to_csv(index=False), "prescriptions_full.csv", "text/csv"
    ):
        pass
    if st.download_button(
        "Télécharger Statistiques (JSON)",
        df.describe(include='all').to_json(), "prescriptions_stats.json", "application/json"
    ):
        pass
