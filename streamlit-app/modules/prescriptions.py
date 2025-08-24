import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from statsmodels.tsa.seasonal import STL

def load_prescriptions_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=['date_prescription'])
    df = df.dropna(subset=['date_prescription', 'département', 'médicament', 'nombre_doses'])
    df['année'] = df['date_prescription'].dt.year
    df['mois'] = df['date_prescription'].dt.to_period('M').dt.to_timestamp()
    return df

def show_prescriptions():
    st.header("💊 Suivi Avancé des Prescriptions TDAH")
    st.markdown("""
    Cette section propose :
    1. Évolution mensuelle et cumul annuel  
    2. Dosage moyen et répartition (quantiles)  
    3. Segmentation par âge et sexe  
    4. Décomposition saisonnière de la série temporelle  
    5. Comparaison dynamique des médicaments  
    6. Cartographie interactive par période  
    7. Export Tableaux et Séries  
    """)

    # Téléversement
    file = st.sidebar.file_uploader("Importer CSV prescriptions", type="csv")
    if not file:
        st.warning("Importez un fichier CSV pour démarrer l'analyse.")
        return
    df = load_prescriptions_data(file)

    # KPI principaux
    st.subheader("Indicateurs clés")
    total = len(df)
    years = sorted(df['année'].unique())
    st.metric("Prescriptions Totales", f"{total:,}")
    st.metric("Années Couvertes", f"{years[0]}–{years[-1]}")
    st.metric("Dose Moyenne par Recette", f"{df['nombre_doses'].mean():.1f}")

    st.markdown("---")

    # 1. Évolution mensuelle & cumul annuel
    st.subheader("Évolution Temporelle")
    monthly = df.groupby('mois').size().rename('count').reset_index()
    yearly_cum = df.groupby(['année']).size().cumsum().reset_index(name='cumul')
    fig_time = go.Figure()
    fig_time.add_trace(go.Scatter(x=monthly['mois'], y=monthly['count'],
                                  mode='lines', name='Mensuel'))
    fig_time.add_trace(go.Bar(x=yearly_cum['année'].astype(str), y=yearly_cum['cumul'],
                              name='Cumul Annuel', opacity=0.5))
    fig_time.update_layout(title="Prescriptions Mensuelles et Cumul Annuel",
                           xaxis_title="Date", yaxis_title="Nombre")
    st.plotly_chart(fig_time, use_container_width=True)

    # 2. Dosage moyen et quantiles
    st.subheader("Dosage par Médicament")
    dose_stats = df.groupby('médicament')['nombre_doses'] \
                   .agg(['mean','median', lambda x: x.quantile(0.25), lambda x: x.quantile(0.75)]) \
                   .rename(columns={'<lambda_0>':'Q1','<lambda_1>':'Q3'}) \
                   .reset_index()
    st.dataframe(dose_stats.style.format({
        'mean': '{:.1f}', 'median': '{:.1f}', 'Q1': '{:.1f}', 'Q3': '{:.1f}'
    }))

    # 3. Segmentation âge et sexe
    st.subheader("Profil Démographique")
    age_bins = [0,6,12,18,30,45,60,100]
    df['tranche_age'] = pd.cut(df['âge_patient'], age_bins, right=False)
    demo = df.groupby(['tranche_age','sexe_patient']).size().reset_index(name='count')
    fig_demo = px.bar(demo, x='tranche_age', y='count', color='sexe_patient',
                      barmode='group', title="Répartition par Tranche d'Âge et Sexe")
    st.plotly_chart(fig_demo, use_container_width=True)

    # 4. Décomposition saisonnière
    st.subheader("Analyse Saisonnière (STL)")
    ts = monthly.set_index('mois')['count']
    stl = STL(ts, period=12, robust=True).fit()
    fig_stl = make_stl_plot(stl)
    st.plotly_chart(fig_stl, use_container_width=True)

    # 5. Comparaison dynamique des médicaments
    st.subheader("Parts de Marché Dynamiques")
    pivot = df.groupby(['mois','médicament']).size().unstack(fill_value=0)
    pct = pivot.divide(pivot.sum(axis=1), axis=0).reset_index()
    fig_dyn = px.area(pct, x='mois', y=pivot.columns,
                      title="Évolution des parts de marché par médicament")
    st.plotly_chart(fig_dyn, use_container_width=True)

    # 6. Cartographie interactive
    st.subheader("Carte Interactive")
    period = st.slider("Période", 
                       min_value=monthly['mois'].min(), 
                       max_value=monthly['mois'].max(),
                       value=(monthly['mois'].min(), monthly['mois'].max()),
                       format="YYYY-MM")
    df_map = df[(df['mois']>=period[0]) & (df['mois']<=period[1])]
    dept = df_map.groupby('département').size().reset_index(name='count')
    geo = "data/france_departements.geojson"
    map_fig = px.choropleth_mapbox(dept, geojson=geo, locations='département',
                                   featureidkey="properties.code", color='count',
                                   color_continuous_scale="Turbo",
                                   mapbox_style="carto-positron",
                                   zoom=5, center={"lat":46, "lon":2},
                                   title="Volume prescriptions par Département")
    st.plotly_chart(map_fig, use_container_width=True)

    # 7. Export avancé
    st.markdown("---")
    st.subheader("Export des Données")
    df_out = df.copy()
    if st.download_button("Télécharger Tout (CSV)", df_out.to_csv(index=False), 
                           "prescriptions_full.csv", "text/csv"):
        pass
    if st.download_button("Télécharger Statistiques (JSON)", 
                          df_out.describe(include='all').to_json(), 
                          "prescriptions_stats.json", "application/json"):
        pass

def make_stl_plot(stl_result):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stl_result.observed.index, y=stl_result.observed.values,
                             name='Observé'))
    fig.add_trace(go.Scatter(x=stl_result.trend.index, y=stl_result.trend.values,
                             name='Tendance'))
    fig.add_trace(go.Scatter(x=stl_result.seasonal.index, y=stl_result.seasonal.values,
                             name='Saisonnalité'))
    fig.update_layout(title="Décomposition STL de la Série Temporelle",
                      xaxis_title="Date", yaxis_title="Nombre de prescriptions")
    return fig
