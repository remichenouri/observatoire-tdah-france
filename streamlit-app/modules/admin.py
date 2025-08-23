"""
Module Administration - Observatoire TDAH
Configuration, maintenance et administration du système
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os

def show_admin():
    """Interface d'administration principale"""
    
    st.markdown("# 🔧 Administration")
    st.markdown("Configuration et maintenance du système Observatoire TDAH")
    
    # Vérification des droits admin (simulation)
    if not check_admin_rights():
        st.error("🚫 Accès refusé - Droits administrateur requis")
        return
    
    # Navigation administrative
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "⚙️ Configuration",
        "👥 Utilisateurs", 
        "🔐 Sécurité",
        "📊 Monitoring",
        "🛠️ Maintenance"
    ])
    
    with tab1:
        show_system_config()
    
    with tab2:
        show_user_management()
        
    with tab3:
        show_security_settings()
        
    with tab4:
        show_system_monitoring()
        
    with tab5:
        show_maintenance_tools()

def check_admin_rights():
    """Vérification des droits administrateur (simulation)"""
    
    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False
    
    if not st.session_state.admin_authenticated:
        st.markdown("### 🔐 Authentification Administrateur")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            username = st.text_input("Nom d'utilisateur")
            password = st.text_input("Mot de passe", type="password")
            
            if st.button("🔑 Se connecter"):
                # Simulation d'authentification
                if username == "admin" and password == "tdah2024":
                    st.session_state.admin_authenticated = True
                    st.success("✅ Authentification réussie")
                    st.rerun()
                else:
                    st.error("❌ Identifiants incorrects")
        
        with col2:
            st.info("""
            **Mode Démonstration**
            
            Utilisez ces identifiants pour accéder au panel admin:
            - **Utilisateur:** admin
            - **Mot de passe:** tdah2024
            
            ⚠️ En production, utiliser un système d'authentification sécurisé
            """)
        
        return False
    
    return True

def show_system_config():
    """Configuration système"""
    
    st.markdown("### ⚙️ Configuration Système")
    
    # Configuration générale
    with st.expander("🔧 Configuration Générale", expanded=True):
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Paramètres de l'Application")
            
            app_title = st.text_input("Titre de l'application", value="Observatoire TDAH France")
            app_version = st.text_input("Version", value="2.0.0")
            debug_mode = st.checkbox("Mode debug", value=False)
            auto_refresh = st.checkbox("Actualisation automatique", value=True)
            
            if auto_refresh:
                refresh_interval = st.slider("Intervalle (secondes)", 30, 3600, 300)
        
        with col2:
            st.markdown("#### 🎨 Interface Utilisateur")
            
            theme = st.selectbox("Thème", ["Auto", "Clair", "Sombre"])
            language = st.selectbox("Langue", ["Français", "English"])
            timezone = st.selectbox("Fuseau horaire", ["Europe/Paris", "UTC"])
            items_per_page = st.number_input("Éléments par page", min_value=10, max_value=100, value=25)
    
    # Configuration des APIs
    with st.expander("🌐 Configuration des APIs"):
        
        apis_config = {
            'DREES': {
                'url': 'https://data.drees.solidarites-sante.gouv.fr/api',
                'active': True,
                'timeout': 30
            },
            'INSEE': {
                'url': 'https://api.insee.fr/donnees-locales/V0.1',
                'active': True, 
                'timeout': 45
            },
            'ANSM': {
                'url': 'https://base-donnees-publique.medicaments.gouv.fr/api',
                'active': True,
                'timeout': 60
            }
        }
        
        for api_name, config in apis_config.items():
            st.markdown(f"**{api_name}**")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.text_input(f"URL {api_name}", value=config['url'], key=f"url_{api_name}")
            
            with col2:
                st.checkbox(f"Actif {api_name}", value=config['active'], key=f"active_{api_name}")
                
            with col3:
                st.number_input(f"Timeout {api_name}", value=config['timeout'], key=f"timeout_{api_name}")
    
    # Sauvegarde de la configuration
    if st.button("💾 Enregistrer la Configuration", type="primary"):
        save_system_config()

def save_system_config():
    """Sauvegarder la configuration système"""
    
    st.success("✅ Configuration sauvegardée avec succès!")
    st.info("🔄 Redémarrage de l'application requis pour certains changements")

def show_user_management():
    """Gestion des utilisateurs"""
    
    st.markdown("### 👥 Gestion des Utilisateurs")
    
    # Statistiques utilisateurs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👤 Total Utilisateurs", "47")
        
    with col2:
        st.metric("🟢 Actifs", "41")
        
    with col3:
        st.metric("🔒 Administrateurs", "3")
        
    with col4:
        st.metric("📅 Nouveaux (30j)", "8")
    
    # Liste des utilisateurs
    st.markdown("#### 📋 Liste des Utilisateurs")
    
    users_data = pd.DataFrame({
        'ID': range(1, 11),
        'Nom': ['Dr. Martin', 'Dr. Dubois', 'Pr. Leroy', 'Dr. Bernard', 'Dr. Petit',
               'Dr. Robert', 'Pr. Richard', 'Dr. Durand', 'Dr. Moreau', 'Dr. Simon'],
        'Email': ['martin@chu-paris.fr', 'dubois@aphp.fr', 'leroy@univ-sorbonne.fr', 
                 'bernard@chru-lille.fr', 'petit@chu-lyon.fr', 'robert@chru-bordeaux.fr',
                 'richard@univ-marseille.fr', 'durand@chu-toulouse.fr', 'moreau@chru-strasbourg.fr',
                 'simon@chu-nantes.fr'],
        'Rôle': ['Médecin', 'Administrateur', 'Chercheur', 'Médecin', 'Médecin',
                'Médecin', 'Chercheur', 'Médecin', 'Médecin', 'Administrateur'],
        'Statut': ['🟢 Actif', '🟢 Actif', '🟢 Actif', '🟢 Actif', '🔴 Inactif',
                  '🟢 Actif', '🟢 Actif', '🟢 Actif', '🟡 Suspendu', '🟢 Actif'],
        'Dernière Connexion': ['2024-08-23', '2024-08-22', '2024-08-21', '2024-08-23',
                               '2024-07-15', '2024-08-20', '2024-08-23', '2024-08-19',
                               '2024-08-10', '2024-08-23']
    })
    
    # Filtres
    col1, col2, col3 = st.columns(3)
    
    with col1:
        role_filter = st.multiselect("Filtrer par rôle", ["Médecin", "Administrateur", "Chercheur"])
        
    with col2:
        status_filter = st.multiselect("Filtrer par statut", ["🟢 Actif", "🔴 Inactif", "🟡 Suspendu"])
        
    with col3:
        search_term = st.text_input("🔍 Rechercher un utilisateur")
    
    # Affichage de la table filtrée
    filtered_users = users_data
    
    if role_filter:
        filtered_users = filtered_users[filtered_users['Rôle'].isin(role_filter)]
    
    if status_filter:
        filtered_users = filtered_users[filtered_users['Statut'].isin(status_filter)]
        
    if search_term:
        filtered_users = filtered_users[
            filtered_users['Nom'].str.contains(search_term, case=False) |
            filtered_users['Email'].str.contains(search_term, case=False)
        ]
    
    st.dataframe(filtered_users, use_container_width=True)
    
    # Actions utilisateur
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ Ajouter Utilisateur"):
            show_add_user_form()
    
    with col2:
        if st.button("📧 Inviter par Email"):
            show_invite_user_form()
    
    with col3:
        if st.button("📊 Export Utilisateurs"):
            st.download_button(
                "💾 Télécharger CSV",
                users_data.to_csv(index=False),
                "utilisateurs_observatoire_tdah.csv",
                "text/csv"
            )

def show_add_user_form():
    """Formulaire d'ajout d'utilisateur"""
    
    with st.form("add_user_form"):
        st.markdown("#### ➕ Nouvel Utilisateur")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nom = st.text_input("Nom complet")
            email = st.text_input("Email")
            
        with col2:
            role = st.selectbox("Rôle", ["Médecin", "Chercheur", "Administrateur"])
            etablissement = st.text_input("Établissement")
        
        permissions = st.multiselect(
            "Permissions",
            ["Lecture", "Écriture", "Admin", "Export", "Configuration"]
        )
        
        if st.form_submit_button("👤 Créer Utilisateur"):
            st.success(f"✅ Utilisateur {nom} créé avec succès!")

def show_invite_user_form():
    """Formulaire d'invitation"""
    
    with st.form("invite_form"):
        st.markdown("#### 📧 Inviter des Utilisateurs")
        
        emails = st.text_area("Emails (un par ligne)", placeholder="email1@domain.com\nemail2@domain.com")
        message = st.text_area("Message personnalisé", 
                              value="Vous êtes invité à rejoindre l'Observatoire TDAH France.")
        role_default = st.selectbox("Rôle par défaut", ["Médecin", "Chercheur"])
        
        if st.form_submit_button("📤 Envoyer Invitations"):
            email_list = [email.strip() for email in emails.split('\n') if email.strip()]
            st.success(f"✅ {len(email_list)} invitations envoyées!")

def show_security_settings():
    """Paramètres de sécurité"""
    
    st.markdown("### 🔐 Paramètres de Sécurité")
    
    # Audit de sécurité
    with st.expander("🔍 Audit de Sécurité", expanded=True):
        
        security_metrics = {
            'Authentification forte': 85,
            'Chiffrement des données': 95,
            'Contrôle d\'accès': 90,
            'Journalisation': 88,
            'Sauvegarde': 92
        }
        
        for metric, score in security_metrics.items():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**{metric}**")
                progress = st.progress(score / 100)
                
            with col2:
                color = "🟢" if score >= 90 else "🟡" if score >= 70 else "🔴"
                st.metric("", f"{color} {score}%")
    
    # Configuration de sécurité
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔑 Authentification")
        
        enable_2fa = st.checkbox("Authentification à deux facteurs", value=True)
        session_timeout = st.slider("Expiration session (heures)", 1, 24, 8)
        password_policy = st.selectbox(
            "Politique mot de passe",
            ["Faible", "Moyenne", "Forte", "Très forte"]
        )
        
    with col2:
        st.markdown("#### 🛡️ Protection")
        
        rate_limiting = st.checkbox("Limitation du taux de requêtes", value=True)
        ip_whitelist = st.checkbox("Liste blanche d'IPs", value=False)
        ssl_enforced = st.checkbox("Forcer HTTPS", value=True)
    
    # Logs de sécurité
    st.markdown("#### 📊 Événements de Sécurité Récents")
    
    security_events = pd.DataFrame({
        'Timestamp': pd.date_range('2024-08-20', periods=10, freq='H'),
        'Type': ['Connexion réussie', 'Échec connexion', 'Changement mot de passe', 
                'Connexion réussie', 'Export données', 'Connexion réussie',
                'Échec connexion', 'Modification config', 'Connexion réussie', 'Déconnexion'],
        'Utilisateur': ['dr.martin', 'unknown', 'dr.dubois', 'dr.bernard', 'admin',
                       'dr.leroy', 'unknown', 'admin', 'dr.petit', 'dr.simon'],
        'IP': ['192.168.1.10', '203.45.67.89', '192.168.1.15', '192.168.1.22', 
               '192.168.1.5', '192.168.1.18', '45.67.89.123', '192.168.1.5',
               '192.168.1.25', '192.168.1.30'],
        'Statut': ['✅ Succès', '🔴 Échec', '✅ Succès', '✅ Succès', '⚠️ Sensible',
                  '✅ Succès', '🔴 Échec', '⚠️ Sensible', '✅ Succès', '✅ Succès']
    })
    
    st.dataframe(security_events, use_container_width=True)

def show_system_monitoring():
    """Monitoring système"""
    
    st.markdown("### 📊 Monitoring Système")
    
    # Métriques système
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💾 Utilisation CPU", "23%", delta="-5%")
        
    with col2:
        st.metric("🧠 Mémoire", "67%", delta="+12%")
        
    with col3:
        st.metric("💿 Disque", "45%", delta="+3%")
        
    with col4:
        st.metric("🌐 Réseau", "156 MB/s", delta="+23 MB/s")
    
    # Graphiques de monitoring
    col1, col2 = st.columns(2)
    
    with col1:
        # CPU Usage
        st.markdown("#### 📈 Utilisation CPU (24h)")
        
        hours = pd.date_range('2024-08-22', periods=24, freq='H')
        cpu_usage = np.random.normal(25, 10, 24).clip(5, 95)
        
        fig = px.line(x=hours, y=cpu_usage, title='CPU Usage (%)')
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Memory Usage
        st.markdown("#### 🧠 Utilisation Mémoire (24h)")
        
        memory_usage = np.random.normal(65, 15, 24).clip(20, 95)
        
        fig = px.area(x=hours, y=memory_usage, title='Memory Usage (%)')
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    # Statut des services
    st.markdown("#### 🔧 Statut des Services")
    
    services_status = pd.DataFrame({
        'Service': ['API Gateway', 'Base de Données', 'Cache Redis', 'File Storage', 
                   'Email Service', 'Backup Service', 'Monitoring'],
        'Statut': ['🟢 Running', '🟢 Running', '🟢 Running', '🟢 Running',
                  '🟢 Running', '🟡 Warning', '🟢 Running'],
        'Uptime': ['99.9%', '99.8%', '99.95%', '99.7%', '98.5%', '97.2%', '99.99%'],
        'Dernière Vérification': ['30s ago', '1m ago', '15s ago', '2m ago',
                                 '5m ago', '10m ago', '1m ago']
    })
    
    st.dataframe(services_status, use_container_width=True)

def show_maintenance_tools():
    """Outils de maintenance"""
    
    st.markdown("### 🛠️ Outils de Maintenance")
    
    # Actions de maintenance
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🧹 Nettoyage")
        
        if st.button("🗑️ Nettoyer les Logs"):
            run_maintenance_task("Nettoyage des logs", 3)
            
        if st.button("💾 Nettoyer le Cache"):
            run_maintenance_task("Nettoyage du cache", 2)
            
        if st.button("📊 Optimiser BDD"):
            run_maintenance_task("Optimisation base de données", 5)
    
    with col2:
        st.markdown("#### 💾 Sauvegardes")
        
        if st.button("📦 Sauvegarde Complète"):
            run_maintenance_task("Sauvegarde complète", 8)
            
        if st.button("⚡ Sauvegarde Incrémentale"):
            run_maintenance_task("Sauvegarde incrémentale", 3)
            
        if st.button("🔄 Restaurer Sauvegarde"):
            show_restore_interface()
    
    # Planification des tâches
    st.markdown("#### ⏰ Tâches Planifiées")
    
    scheduled_tasks = pd.DataFrame({
        'Tâche': ['Sauvegarde quotidienne', 'Nettoyage hebdomadaire', 'Rapport mensuel',
                 'Mise à jour sécurité', 'Archivage trimestriel'],
        'Fréquence': ['Quotidienne', 'Hebdomadaire', 'Mensuelle', 'Automatique', 'Trimestrielle'],
        'Prochaine Exécution': ['2024-08-24 02:00', '2024-08-25 03:00', '2024-09-01 01:00',
                               'Dès disponible', '2024-10-01 00:00'],
        'Statut': ['✅ Active', '✅ Active', '✅ Active', '⏸️ Pause', '✅ Active']
    })
    
    st.dataframe(scheduled_tasks, use_container_width=True)

def run_maintenance_task(task_name, duration):
    """Exécution d'une tâche de maintenance"""
    
    with st.spinner(f"Exécution: {task_name}..."):
        import time
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(duration):
            status_text.text(f"{task_name} en cours... ({i+1}/{duration})")
            progress_bar.progress((i + 1) / duration)
            time.sleep(0.5)
        
        st.success(f"✅ {task_name} terminée avec succès!")

def show_restore_interface():
    """Interface de restauration"""
    
    with st.expander("🔄 Restaurer une Sauvegarde", expanded=True):
        
        backup_files = [
            "backup_2024-08-23_full.sql",
            "backup_2024-08-22_incremental.sql", 
            "backup_2024-08-21_full.sql",
            "backup_2024-08-20_incremental.sql"
        ]
        
        selected_backup = st.selectbox("Choisir une sauvegarde", backup_files)
        
        st.warning("⚠️ La restauration remplacera toutes les données actuelles!")
        
        confirm_restore = st.checkbox("Je confirme vouloir restaurer cette sauvegarde")
        
        if st.button("🔄 Lancer la Restauration", disabled=not confirm_restore):
            run_maintenance_task("Restauration de sauvegarde", 6)