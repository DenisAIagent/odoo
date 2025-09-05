# MDMC Music Ads - CRM Odoo Complet 

## 🎵 À Propos

Ce projet livre un **CRM Odoo 17 complet** prêt pour la production, spécialement conçu pour **MDMC Music Ads** - une agence de marketing musical spécialisée dans la promotion d'artistes et labels indépendants sur les plateformes digitales.

### 🏢 Modèle Économique Unique

- **Honoraires d'agence** : 200€ HT/mois par plateforme (YouTube, Meta, TikTok)
- **Budget média** : Payé directement par le client aux plateformes (non facturé par Odoo)
- **Facturation** : 100% à la commande ou abonnement récurrent mensuel
- **Reporting transparent** : Distinction claire honoraires vs budget média

## 🚀 Fonctionnalités Principales

### 💼 CRM & Prospection
- **Capture de leads** via webhook depuis site externe
- **Scoring automatique** basé sur budget, plateformes, pays, genre musical
- **Séquences d'emailing** automatisées (J+0, J+3, J+7)
- **Conversion leads → clients** avec données spécifiques musique

### 💰 Ventes & Abonnements
- **Produits honoraires** pré-configurés par plateforme
- **Facturation immédiate** à la confirmation de commande
- **Abonnements récurrents** mensuels (OCA Contract)
- **Paiements en ligne** (Stripe/SEPA/PayPal)

### 📊 Gestion de Campagnes
- **Fiches campagnes** avec budgets déclaratifs par plateforme
- **Ingestion KPIs** automatique via API REST sécurisée
- **Métriques complètes** : spend, impressions, vues, clics, CTR, CPV, conversions
- **Alertes budget** avec seuils configurables
- **Historique jour par jour** des performances

### 🔧 Support & Helpdesk
- **Tickets** par email/portail client
- **SLA simples** et routage par catégories
- **Intégration OCA helpdesk**

### 📈 Reporting & Analytics
- **Rapports PDF** hebdomadaires/mensuels par campagne
- **Dashboard direction** : CA, MRR, churn, conversion leads→clients
- **Distinction visuelle** honoraires vs budget média
- **Envoi automatique** aux clients

### 🛡️ RGPD & Sécurité
- **Audit log complet** (OCA auditlog)
- **Export/anonymisation** contacts
- **Purge automatique** leads inactifs (24 mois)
- **Consentements marketing** horodatés
- **Rôles utilisateurs** stricts (SDR, Sales, PM, Support, Compta, Direction)

### 🌐 Portail Client
- **Pages dédiées** : infos, factures, campagnes, rapports, tickets
- **Upload d'assets** créatifs
- **Suivi temps réel** des performances
- **Interface responsive** moderne

## 🏗️ Architecture Technique

### Stack Principal
- **Odoo 17 Community Edition** + modules OCA
- **PostgreSQL 15** (base de données)
- **Redis** (queue_job OCA)
- **n8n** (intégrations APIs)
- **Traefik** (reverse proxy + SSL)
- **Docker Compose** (orchestration)

### Modules Développés
```
odoo/addons/
├── mdmc_base/          # Configuration de base, plateformes, rôles
├── mdmc_crm/          # CRM étendu, scoring, séquences email
├── mdmc_sales/        # Ventes, abonnements, produits honoraires
├── mdmc_campaigns/    # Campagnes publicitaires, ingestion KPIs
├── mdmc_helpdesk/     # Support client (OCA helpdesk)
├── mdmc_reporting/    # Rapports PDF, dashboards
├── mdmc_gdpr/         # Conformité RGPD, export/anonymisation
└── mdmc_portal/       # Portail client moderne
```

### Intégrations n8n
- **Google Ads API** → YouTube KPIs
- **Meta Marketing API** → Facebook/Instagram KPIs  
- **TikTok Business API** → TikTok Ads KPIs
- **Google Analytics 4** → Données de conversion site web

## 🚀 Installation & Déploiement

### Prérequis
- Docker & Docker Compose
- Nom de domaine configuré
- Certificats SSL (Let's Encrypt via Traefik)
- Comptes API : Google Ads, Meta, TikTok, GA4

### 1. Clonage et Configuration
```bash
git clone <votre-repo>
cd mdmc-odoo

# Copier et configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos valeurs
```

### 2. Variables Critiques (.env)
```env
# Domaines
ODOO_DOMAIN=crm.mdmcmusicads.com
N8N_DOMAIN=automation.mdmcmusicads.com

# Base de données
DB_PASSWORD=votre_mot_de_passe_db_securise

# API
MDMC_API_KPI_TOKEN=votre_token_api_securise

# SMTP Production
SMTP_SERVER=smtp.brevo.com
SMTP_USER=votre_utilisateur_smtp
SMTP_PASSWORD=votre_mot_de_passe_smtp
```

### 3. Lancement Production
```bash
# Production complète
docker-compose -f docker/docker-compose.prod.yml up -d

# Vérifier les services
docker-compose -f docker/docker-compose.prod.yml ps
```

### 4. Configuration Initiale Odoo

#### a) Première Connexion
- URL : https://crm.mdmcmusicads.com
- Base : `mdmc_odoo`
- Email admin : `admin@mdmcmusicads.com`
- Mot de passe : Configuré dans `.env`

#### b) Installation Modules
```bash
# Installer tous les modules MDMC
# Via interface : Apps → Rechercher "MDMC" → Installer tout
# Ou via commande :
docker-compose exec odoo odoo -d mdmc_odoo -i mdmc_base,mdmc_crm,mdmc_sales,mdmc_campaigns,mdmc_helpdesk,mdmc_reporting,mdmc_gdpr,mdmc_portal --stop-after-init
```

#### c) Configuration API KPI
```bash
# Configurer le token API dans Odoo
# Paramètres → Paramètres Techniques → Paramètres Système
# Créer : mdmc.api.kpi_token = votre_token_api_securise
```

### 5. Configuration n8n

#### a) Accès n8n
- URL : https://automation.mdmcmusicads.com
- User/Pass : Configurés dans `.env`

#### b) Import Workflows
```bash
# Importer les workflows depuis l'interface n8n
# Settings → Import from File
# Fichiers : n8n/workflows/*.json
```

#### c) Configuration Credentials
Dans n8n, créer les credentials :
- **Google Ads API** (OAuth2)
- **Meta Marketing API** (Access Token)  
- **TikTok Business API** (Access Token)
- **Google Analytics 4** (Service Account)

### 6. Tests de Fonctionnement

#### a) Test API KPI
```bash
curl -X POST https://crm.mdmcmusicads.com/api/mdmc/v1/kpis/test \
  -H "X-API-KEY: votre_token_api"
```

#### b) Test Webhook Leads
```bash
curl -X POST https://crm.mdmcmusicads.com/api/mdmc/v1/leads/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Artist",
    "email": "test@example.com",
    "artist_name": "TestArtist",
    "genre": "pop",
    "budget_estimated": 1500,
    "platforms_interest": ["youtube", "meta"]
  }'
```

## 📊 Utilisation Métier

### Pour les SDR (Sales Development Representatives)
1. **Leads entrants** → Tableau Kanban par score
2. **Séquences d'emailing** → Automatiques ou manuelles
3. **Qualification** → Formulaire complet avec scoring
4. **Transfert Sales** → Assignation + notification

### Pour l'Équipe Sales
1. **Création devis** → Produits honoraires par plateforme
2. **Mode paiement** → Immédiat ou abonnement mensuel
3. **Confirmation** → Facturation automatique
4. **Suivi client** → Portail + reporting

### Pour les Chefs de Projet
1. **Création campagne** → Budgets déclaratifs par plateforme
2. **Suivi KPIs** → Ingestion automatique n8n
3. **Alertes budget** → Notifications dépassement seuils
4. **Rapports clients** → PDF automatiques

### Pour la Direction
1. **Dashboard KPIs** → CA, MRR, churn, conversion leads
2. **Analyse performance** → Par plateforme, par période
3. **Reporting financier** → Distinction honoraires/budget média

## 🔧 Maintenance & Monitoring

### Sauvegarde Automatique
```bash
# Script de sauvegarde PostgreSQL (à programmer via cron)
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec -T db pg_dump -U odoo mdmc_odoo > backups/mdmc_odoo_$DATE.sql
gzip backups/mdmc_odoo_$DATE.sql

# Rotation des sauvegardes (garder 30 jours)
find backups/ -name "*.sql.gz" -mtime +30 -delete
```

### Monitoring Santé Services
```bash
# Check health status
docker-compose -f docker/docker-compose.prod.yml ps
docker-compose -f docker/docker-compose.prod.yml logs odoo --tail 50
docker-compose -f docker/docker-compose.prod.yml logs n8n --tail 50
```

### Métriques Importantes
- **Uptime services** : Odoo, PostgreSQL, n8n, Traefik
- **Performance Odoo** : Temps réponse, workers actifs
- **Volume données** : Croissance base, logs, sauvegardes
- **Intégrations n8n** : Succès/échecs workflows KPIs

## 🔒 Sécurité Production

### SSL/TLS
- **Let's Encrypt** automatique via Traefik
- **HSTS** activé
- **Redirection HTTP → HTTPS** forcée

### Base de Données  
- **Accès restreint** aux services internes uniquement
- **Mots de passe forts** (générés)
- **Sauvegardes chiffrées**

### APIs
- **Tokens authentification** pour endpoints KPIs
- **Rate limiting** Traefik
- **Logs audit** complets (OCA auditlog)

### Données Personnelles (RGPD)
- **Consentements** explicites et horodatés
- **Droit à l'oubli** : anonymisation/suppression
- **Export données** : formats JSON/CSV/ZIP
- **Purge automatique** leads inactifs

## 🧪 Tests & Qualité

### Tests Automatisés
```bash
# Lancer les tests Odoo
python odoo/odoo-bin -d test_db --test-enable --stop-after-init -i mdmc_base,mdmc_crm,mdmc_sales,mdmc_campaigns
```

### CI/CD GitHub Actions
- **Lint** : flake8, black, isort, pylint-odoo
- **Tests** : modules Odoo + couverture
- **Sécurité** : Bandit scan
- **Build** : Images Docker
- **Déploiement** : staging/production automatique

### Pre-commit Hooks
```bash
# Installation
pip install pre-commit
pre-commit install

# Les hooks vérifient automatiquement :
# - Formatting (black, isort)  
# - Linting (flake8, pylint-odoo)
# - Standards OCA
```

## 🎯 KPIs Business

### Métriques de Conversion
- **Lead → Prospect qualifié** : X%
- **Prospect → Client** : Y%
- **Taux de réponse emails** séquences
- **Temps moyen** lead → première vente

### Métriques Financières
- **MRR (Monthly Recurring Revenue)** 
- **Churn rate** abonnements
- **ARPU (Average Revenue Per User)**
- **CAC (Customer Acquisition Cost)**

### Métriques Opérationnelles
- **Nombre campagnes** actives
- **Budget média total** géré (déclaratif)
- **Performance moyenne** : CTR, CPV, conversions
- **Satisfaction client** (CSAT support)

## 📞 Support & Contact

### Support Technique
- **Documentation** : Ce README + code commenté
- **Logs** : `docker-compose logs -f [service]`
- **Debug Odoo** : Mode développeur + logs détaillés

### Formation Équipe
1. **Administrateur Odoo** : Installation, configuration, maintenance
2. **Utilisateurs métier** : Workflows CRM, campagnes, reporting  
3. **Intégrateurs** : APIs, n8n, personnalisations

### Roadmap Évolutions
- [ ] **Mobile app** React Native pour consultations terrain
- [ ] **IA recommendations** optimisation campagnes
- [ ] **Intégrations avancées** : Spotify for Artists, Apple Music
- [ ] **Multi-devises** pour expansion internationale
- [ ] **White-label** pour partenaires/revendeurs

---

## 🎵 **MDMC Music Ads - Votre Agence Marketing Musical de Référence**

*Transformez vos artistes en succès digitaux avec notre CRM professionnel !*

---

**© 2025 MDMC Music Ads - Tous droits réservés**  
*Développé avec ❤️ pour la communauté musicale indépendante*