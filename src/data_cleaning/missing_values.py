import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import missingno as msno
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')
from config import DATA_SOURCE_PATH, MISSING_RATE_MAX, OUTLIER_ZSCORE



class MissingValueHandler:
    """Gestionnaire intelligent des valeurs manquantes"""
    
    def __init__(self):
        self.imputation_strategies = {}
        self.imputation_log = []
        self.original_missing_patterns = {}
    
    def analyze_missing_patterns(self, df, dataset_name):
        """Analyse complète des patterns de données manquantes"""
        
        print(f"\n🔍 ANALYSE DES VALEURS MANQUANTES - {dataset_name}")
        print("="*60)
        
        # Statistiques générales
        missing_data = df.isnull().sum()
        missing_percent = (missing_data / len(df) * 100).round(2)
        
        missing_table = pd.DataFrame({
            'Colonnes': missing_data.index,
            'Valeurs_Manquantes': missing_data.values,
            'Pourcentage': missing_percent.values
        }).sort_values('Pourcentage', ascending=False)
        
        print("📊 Résumé des valeurs manquantes:")
        print(missing_table[missing_table['Valeurs_Manquantes'] > 0].to_string(index=False))
        
        # Patterns de co-occurrence
        self.original_missing_patterns[dataset_name] = df.isnull()
        
        return missing_table
    
    def visualize_missing_patterns(self, df, dataset_name):
        """Visualisation des patterns de valeurs manquantes"""
        
        # 1. Matrice des valeurs manquantes avec missingno
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle(f'Analyse des Valeurs Manquantes - {dataset_name}', 
                     fontsize=16, fontweight='bold')
        
        # Matrice
        msno.matrix(df, ax=axes[0,0])
        axes[0,0].set_title('Matrice des Valeurs Manquantes')
        
        # Heatmap de corrélation des nulls
        msno.heatmap(df, ax=axes[0,1])
        axes[0,1].set_title('Corrélation des Valeurs Manquantes')
        
        # Bar plot
        msno.bar(df, ax=axes[1,0])
        axes[1,0].set_title('Compte des Valeurs Manquantes')
        
        # Dendrogram
        try:
            msno.dendrogram(df, ax=axes[1,1])
            axes[1,1].set_title('Clustering des Patterns')
        except:
            axes[1,1].text(0.5, 0.5, 'Dendrogram non disponible', 
                          ha='center', va='center', transform=axes[1,1].transAxes)
        
        plt.tight_layout()
        plt.savefig(f'../reports/figures/missing_patterns_{dataset_name}.png', 
                   dpi=300, bbox_inches='tight')
        plt.show()
        
        # 2. Dashboard interactif Plotly
        missing_data = df.isnull().sum()
        missing_percent = (missing_data / len(df) * 100).round(2)
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Pourcentage de Valeurs Manquantes', 
                           'Distribution des Taux de Manquement',
                           'Heatmap des Co-occurrences', 
                           'Timeline des Valeurs Manquantes'),
            specs=[[{"type": "bar"}, {"type": "histogram"}],
                   [{"type": "heatmap"}, {"type": "scatter"}]]
        )
        
        # Bar plot des pourcentages
        non_zero_missing = missing_percent[missing_percent > 0].sort_values(ascending=True)
        fig.add_trace(
            go.Bar(y=non_zero_missing.index, x=non_zero_missing.values,
                   orientation='h', name='% Manquant',
                   marker_color='red', opacity=0.7),
            row=1, col=1
        )
        
        # Histogramme des taux
        fig.add_trace(
            go.Histogram(x=missing_percent[missing_percent > 0],
                        name='Distribution Taux', marker_color='orange'),
            row=1, col=2
        )
        
        # Heatmap de corrélation des nulls (échantillon)
        if len(df.columns) > 2:
            null_corr = df.isnull().corr()
            fig.add_trace(
                go.Heatmap(z=null_corr.values, x=null_corr.columns, y=null_corr.index,
                          colorscale='RdYlBu', name='Corrélation Nulls'),
                row=2, col=1
            )
        
        # Timeline si date disponible
        date_cols = [col for col in df.columns if 'date' in col.lower() 
                    or 'time' in col.lower() or df[col].dtype == 'datetime64[ns]']
        if date_cols:
            date_col = date_cols[0]
            missing_by_date = df.groupby(pd.to_datetime(df[date_col], errors='coerce').dt.date).apply(
                lambda x: x.isnull().sum().sum())
            fig.add_trace(
                go.Scatter(x=missing_by_date.index, y=missing_by_date.values,
                          mode='lines+markers', name='Manquant par Date',
                          line=dict(color='purple')),
                row=2, col=2
            )
        
        fig.update_layout(height=800, showlegend=False,
                         title_text=f"Dashboard Valeurs Manquantes - {dataset_name}")
        fig.write_html(f'../reports/figures/missing_dashboard_{dataset_name}.html')
        fig.show()
    
    def determine_imputation_strategy(self, df, column):
        """Détermine la meilleure stratégie d'imputation pour une colonne"""
        
        missing_rate = df[column].isnull().mean()
        col_dtype = df[column].dtype
        
        strategies = []
        
        # Critères de décision
        if missing_rate > 0.7:
            strategies.append(('drop_column', 0.1, 'Taux de manquement trop élevé'))
            
        elif missing_rate > 0.3:
            if col_dtype in ['object', 'category']:
                strategies.append(('mode_imputation', 0.6, 'Mode pour catégorielle avec beaucoup de manquant'))
                strategies.append(('create_missing_category', 0.8, 'Catégorie "Inconnu" peut être informative'))
            else:
                strategies.append(('group_median', 0.7, 'Médiane par groupe pour numérique'))
                strategies.append(('ml_imputation', 0.5, 'ML imputation risquée avec beaucoup de manquant'))
                
        else:  # missing_rate <= 0.3
            if col_dtype in ['object', 'category']:
                strategies.append(('mode_imputation', 0.8, 'Mode pour catégorielle'))
                strategies.append(('ml_imputation', 0.6, 'ML pour catégorielle'))
            else:
                strategies.append(('ml_imputation', 0.9, 'ML optimal pour numérique avec peu de manquant'))
                strategies.append(('group_median', 0.7, 'Médiane par groupe'))
                strategies.append(('median_imputation', 0.5, 'Médiane simple'))
        
        # Retour de la meilleure stratégie
        best_strategy = max(strategies, key=lambda x: x[1])
        return best_strategy, best_strategy
    
    def apply_group_imputation(self, df, column, group_columns):
        """Imputation par groupe (ex: médiane par tranche d'âge)"""
        
        original_missing = df[column].isnull().sum()
        
        # Création des groupes
        for group_col in group_columns:
            if group_col in df.columns:
                if df[column].dtype in ['int64', 'float64']:
                    # Médiane par groupe
                    group_medians = df.groupby(group_col)[column].median()
                    df[column] = df[column].fillna(df[group_col].map(group_medians))
                else:
                    # Mode par groupe
                    group_modes = df.groupby(group_col)[column].agg(lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else None)
                    df[column] = df[column].fillna(df[group_col].map(group_modes))
                break
        
        # Imputation globale pour les valeurs encore manquantes
        if df[column].isnull().sum() > 0:
            if df[column].dtype in ['int64', 'float64']:
                df[column] = df[column].fillna(df[column].median())
            else:
                df[column] = df[column].fillna(df[column].mode().iloc[0] if len(df[column].mode()) > 0 else 'Unknown')
        
        final_missing = df[column].isnull().sum()
        
        return df, original_missing, final_missing
    
    def apply_ml_imputation(self, df, column):
        """Imputation par Machine Learning"""
        
        original_missing = df[column].isnull().sum()
        
        # Préparation des données
        df_ml = df.copy()
        
        # Sélection des features pour prédiction
        feature_cols = []
        for col in df_ml.columns:
            if col != column and df_ml[col].notna().sum() > len(df_ml) * 0.5:
                if df_ml[col].dtype in ['int64', 'float64']:
                    feature_cols.append(col)
                elif df_ml[col].dtype == 'object' and df_ml[col].nunique() < 20:
                    # Encodage des variables catégorielles
                    le = LabelEncoder()
                    df_ml[f'{col}_encoded'] = le.fit_transform(df_ml[col].astype(str))
                    feature_cols.append(f'{col}_encoded')
        
        if len(feature_cols) < 2:
            print(f"⚠️ Pas assez de features pour ML imputation de {column}")
            return df, original_missing, original_missing
        
        # Séparation des données
        train_mask = df_ml[column].notna()
        test_mask = df_ml[column].isna()
        
        X_train = df_ml.loc[train_mask, feature_cols].fillna(0)
        y_train = df_ml.loc[train_mask, column]
        X_test = df_ml.loc[test_mask, feature_cols].fillna(0)
        
        # Choix du modèle
        if df[column].dtype in ['int64', 'float64']:
            model = RandomForestRegressor(n_estimators=100, random_state=42)
        else:
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            # Encodage de la variable cible si catégorielle
            le_target = LabelEncoder()
            y_train = le_target.fit_transform(y_train.astype(str))
        
        # Entraînement et prédiction
        model.fit(X_train, y_train)
        
        # Validation croisée pour évaluer la qualité
        cv_scores = cross_val_score(model, X_train, y_train, cv=5)
        print(f"📊 Score CV pour {column}: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
        
        # Prédiction des valeurs manquantes
        predictions = model.predict(X_test)
        
        if df[column].dtype not in ['int64', 'float64']:
            predictions = le_target.inverse_transform(predictions)
        
        # Application des prédictions
        df.loc[test_mask, column] = predictions
        
        final_missing = df[column].isnull().sum()
        
        return df, original_missing, final_missing
    
    def create_imputation_indicators(self, df, imputed_columns):
        """Création d'indicateurs de données imputées"""
        
        for col in imputed_columns:
            if col in self.original_missing_patterns:
                df[f'{col}_was_missing'] = self.original_missing_patterns[col]
            else:
                # Si pas d'info originale, créer basé sur pattern détecté
                df[f'{col}_was_missing'] = df[col].isnull()
        
        return df
    
    def process_missing_values(self, df, dataset_name, 
                             group_columns_context=None):
        """Processus complet de traitement des valeurs manquantes"""
        
        print(f"\n🚀 TRAITEMENT DES VALEURS MANQUANTES - {dataset_name}")
        print("="*60)
        
        # Analyse initiale
        missing_analysis = self.analyze_missing_patterns(df, dataset_name)
        self.visualize_missing_patterns(df, dataset_name)
        
        # Sauvegarde des patterns originaux
        self.original_missing_patterns[dataset_name] = df.isnull()
        
        # Traitement colonne par colonne
        processed_columns = []
        
        for col in df.columns:
            if df[col].isnull().sum() > 0:
                
                # Détermination de la stratégie
                strategy, reason = self.determine_imputation_strategy(df, col)
                print(f"\n📋 {col}: {strategy} - {reason}")
                
                original_missing = df[col].isnull().sum()
                
                if strategy == 'drop_column':
                    df = df.drop(columns=[col])
                    self.imputation_log.append({
                        'dataset': dataset_name,
                        'column': col,
                        'strategy': strategy,
                        'original_missing': original_missing,
                        'final_missing': 'column_dropped',
                        'reason': reason
                    })
                    
                elif strategy == 'group_median':
                    # Définition des colonnes de groupage contextuelles
                    if group_columns_context:
                        group_cols = group_columns_context
                    else:
                        # Colonnes de groupage par défaut pour TDAH
                        group_cols = ['age_group', 'sexe', 'region_code', 'age_category']
                        group_cols = [gc for gc in group_cols if gc in df.columns]
                    
                    df, orig_miss, final_miss = self.apply_group_imputation(df, col, group_cols)
                    processed_columns.append(col)
                    
                    self.imputation_log.append({
                        'dataset': dataset_name,
                        'column': col,
                        'strategy': strategy,
                        'original_missing': orig_miss,
                        'final_missing': final_miss,
                        'group_columns': group_cols,
                        'reason': reason
                    })
                    
                elif strategy == 'ml_imputation':
                    df, orig_miss, final_miss = self.apply_ml_imputation(df, col)
                    processed_columns.append(col)
                    
                    self.imputation_log.append({
                        'dataset': dataset_name,
                        'column': col,
                        'strategy': strategy,
                        'original_missing': orig_miss,
                        'final_missing': final_miss,
                        'reason': reason
                    })
                    
                elif strategy == 'mode_imputation':
                    mode_value = df[col].mode().iloc[0] if len(df[col].mode()) > 0 else 'Unknown'
                    df[col] = df[col].fillna(mode_value)
                    final_missing = df[col].isnull().sum()
                    processed_columns.append(col)
                    
                    self.imputation_log.append({
                        'dataset': dataset_name,
                        'column': col,
                        'strategy': strategy,
                        'original_missing': original_missing,
                        'final_missing': final_missing,
                        'imputation_value': mode_value,
                        'reason': reason
                    })
                    
                elif strategy == 'median_imputation':
                    median_value = df[col].median()
                    df[col] = df[col].fillna(median_value)
                    final_missing = df[col].isnull().sum()
                    processed_columns.append(col)
                    
                    self.imputation_log.append({
                        'dataset': dataset_name,
                        'column': col,
                        'strategy': strategy,
                        'original_missing': original_missing,
                        'final_missing': final_missing,
                        'imputation_value': median_value,
                        'reason': reason
                    })
                    
                elif strategy == 'create_missing_category':
                    df[col] = df[col].fillna('Missing_Data')
                    final_missing = df[col].isnull().sum()
                    processed_columns.append(col)
                    
                    self.imputation_log.append({
                        'dataset': dataset_name,
                        'column': col,
                        'strategy': strategy,
                        'original_missing': original_missing,
                        'final_missing': final_missing,
                        'imputation_value': 'Missing_Data',
                        'reason': reason
                    })
        
        # Création des indicateurs de données imputées
        df = self.create_imputation_indicators(df, processed_columns)
        
        print(f"\n✅ Traitement terminé pour {dataset_name}")
        print(f"📊 Colonnes traitées: {len(processed_columns)}")
        
        return df
    
    def validate_imputation_quality(self, df_original, df_imputed, dataset_name):
        """Validation de la qualité de l'imputation"""
        
        print(f"\n🔍 VALIDATION QUALITÉ IMPUTATION - {dataset_name}")
        print("="*50)
        
        validation_results = {}
        
        # Comparaison des distributions
        numeric_cols = df_original.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            if col in df_imputed.columns:
                # Test de Kolmogorov-Smirnov pour comparer distributions
                from scipy import stats
                
                original_values = df_original[col].dropna()
                imputed_values = df_imputed[col]
                
                # Statistiques descriptives
                orig_stats = original_values.describe()
                imp_stats = imputed_values.describe()
                
                # Test KS
                ks_stat, ks_pvalue = stats.ks_2samp(original_values, imputed_values)
                
                validation_results[col] = {
                    'original_mean': orig_stats['mean'],
                    'imputed_mean': imp_stats['mean'],
                    'mean_difference': abs(orig_stats['mean'] - imp_stats['mean']) / orig_stats['mean'],
                    'original_std': orig_stats['std'],
                    'imputed_std': imp_stats['std'],
                    'std_difference': abs(orig_stats['std'] - imp_stats['std']) / orig_stats['std'],
                    'ks_statistic': ks_stat,
                    'ks_pvalue': ks_pvalue,
                    'distribution_similar': ks_pvalue > 0.05
                }
        
        # Graphiques de validation
        self.create_validation_plots(df_original, df_imputed, dataset_name, validation_results)
        
        return validation_results
    
    def create_validation_plots(self, df_original, df_imputed, dataset_name, validation_results):
        """Création des graphiques de validation"""
        
        numeric_cols = list(validation_results.keys())[:6]  # Limite à 6 pour lisibilité
        
        if numeric_cols:
            fig = make_subplots(
                rows=2, cols=3,
                subplot_titles=[f'Distribution - {col}' for col in numeric_cols]
            )
            
            for i, col in enumerate(numeric_cols):
                row = (i // 3) + 1
                col_pos = (i % 3) + 1
                
                # Distribution originale
                fig.add_trace(
                    go.Histogram(x=df_original[col].dropna(), name=f'{col}_original',
                               opacity=0.7, marker_color='blue', 
                               legendgroup=col, showlegend=True),
                    row=row, col=col_pos
                )
                
                # Distribution après imputation
                fig.add_trace(
                    go.Histogram(x=df_imputed[col], name=f'{col}_imputed',
                               opacity=0.5, marker_color='red',
                               legendgroup=col, showlegend=True),
                    row=row, col=col_pos
                )
            
            fig.update_layout(height=600, 
                             title_text=f"Validation Distributions - {dataset_name}")
            fig.write_html(f'../reports/figures/imputation_validation_{dataset_name}.html')
            fig.show()
        
        # Tableau de synthèse
        validation_df = pd.DataFrame(validation_results).T
        validation_df['quality_score'] = (
            (1 - validation_df['mean_difference'].clip(0, 1)) * 0.4 +
            (1 - validation_df['std_difference'].clip(0, 1)) * 0.4 +
            validation_df['distribution_similar'].astype(float) * 0.2
        )
        
        print("📊 Scores de Qualité d'Imputation:")
        print(validation_df[['mean_difference', 'std_difference', 'distribution_similar', 'quality_score']].round(3).to_string())
        
        return validation_df
    
    def generate_imputation_report(self):
        """Génération du rapport complet d'imputation"""
        
        report_df = pd.DataFrame(self.imputation_log)
        
        if not report_df.empty:
            # Statistiques par stratégie
            strategy_stats = report_df.groupby('strategy').agg({
                'original_missing': 'sum',
                'column': 'count'
            }).rename(columns={'column': 'columns_count'})
            
            print("\n📋 RAPPORT FINAL D'IMPUTATION")
            print("="*50)
            print("Statistiques par stratégie:")
            print(strategy_stats.to_string())
            
            # Sauvegarde
            report_df.to_csv('../reports/imputation_detailed_log.csv', index=False)
            strategy_stats.to_csv('../reports/imputation_strategy_summary.csv')
        
        return report_df
