{
    'name': 'MDMC Campaigns',
    'version': '17.0.1.0.0',
    'summary': 'Gestion des campagnes publicitaires MDMC',
    'description': """
        Module de gestion des campagnes pour MDMC Music Ads :
        - Fiches campagnes avec budgets déclaratifs par plateforme
        - Ingestion KPIs via API REST (spend, vues, clics, CTR, etc.)
        - Stockage historique des performances jour par jour
        - API sécurisée pour intégration n8n
        - Alertes dépassement budget
        - Vues performance avec graphiques
    """,
    'author': 'MDMC Music Ads',
    'category': 'Project',
    'depends': [
        'project',
        'mdmc_base',
        'mdmc_sales',
        'queue_job',  # OCA server-tools
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/record_rules.xml',
        'data/campaign_data.xml',
        'data/cron_data.xml',
        'views/mdmc_campaign_views.xml',
        'views/mdmc_campaign_kpi_views.xml',
        'views/mdmc_campaigns_menus.xml',
    ],
    'demo': [
        'data/demo_data.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}