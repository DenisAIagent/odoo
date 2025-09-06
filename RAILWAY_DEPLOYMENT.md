# Déploiement MDMC CRM sur Railway

## Variables d'environnement à configurer sur Railway

Allez dans votre projet Railway > Variables et ajoutez ces variables :

### Base de données PostgreSQL
```
DATABASE_HOST=<host_postgresql_railway>
DATABASE_PORT=5432
DATABASE_USER=<user_postgresql_railway>
DATABASE_PASSWORD=<password_postgresql_railway>
DATABASE_NAME=<database_name_railway>
```

### Configuration Odoo
```
ODOO_ADMIN_PASSWORD=mdmc_admin_secure_2025
PORT=8069
```

### APIs (optionnel pour MVP)
```
# Google Ads API
GOOGLE_ADS_CLIENT_ID=your_google_ads_client_id
GOOGLE_ADS_CLIENT_SECRET=your_google_ads_client_secret
GOOGLE_ADS_REFRESH_TOKEN=your_google_ads_refresh_token

# Meta Ads API
META_APP_ID=your_meta_app_id
META_APP_SECRET=your_meta_app_secret
META_ACCESS_TOKEN=your_meta_access_token

# TikTok Ads API
TIKTOK_APP_ID=your_tiktok_app_id
TIKTOK_SECRET=your_tiktok_secret
TIKTOK_ACCESS_TOKEN=your_tiktok_access_token

# Google Analytics 4
GA4_MEASUREMENT_ID=G-XXXXXXXXXX
GA4_API_SECRET=your_ga4_api_secret
```

## Étapes de déploiement

1. **Connecter Railway à GitHub**
   - Allez sur railway.app
   - Connectez votre repo GitHub `DenisAIagent/odoo`

2. **Ajouter un service PostgreSQL**
   - Ajoutez un service PostgreSQL à votre projet
   - Notez les variables de connexion

3. **Configurer les variables d'environnement**
   - Utilisez les variables PostgreSQL générées par Railway
   - Ajoutez les autres variables listées ci-dessus

4. **Déployer**
   - Railway détectera automatiquement le Dockerfile
   - Le déploiement se fera automatiquement

## Post-déploiement

1. **Initialiser la base de données**
   - Accédez à votre URL Railway
   - Créez la base de données via l'interface Odoo
   - Utilisez l'email admin et le mot de passe défini dans ODOO_ADMIN_PASSWORD

2. **Installer les modules MDMC**
   - Allez dans Apps
   - Installez les modules mdmc_* dans l'ordre :
     1. mdmc_base
     2. mdmc_crm  
     3. mdmc_sales
     4. mdmc_campaigns
     5. mdmc_helpdesk
     6. mdmc_reporting
     7. mdmc_gdpr
     8. mdmc_portal

## Domaine personnalisé

Pour utiliser www.mdmcmusicads.com :
1. Allez dans Settings > Domains
2. Ajoutez votre domaine personnalisé
3. Configurez les DNS selon les instructions Railway

## Monitoring

- Railway fournit des métriques automatiques
- Logs disponibles dans l'onglet Logs
- Alertes configurables dans Settings

## Support

En cas de problème :
1. Vérifiez les logs de déploiement
2. Validez les variables d'environnement
3. Assurez-vous que PostgreSQL est bien connecté