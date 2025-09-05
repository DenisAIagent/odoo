{
    'name': 'MDMC Reporting',
    'version': '17.0.1.0.0',
    'summary': 'Rapports et PDF pour MDMC Music Ads',
    'description': """
        Module de reporting pour MDMC Music Ads :
        - Rapport hebdomadaire/mensuel PDF par campagne
        - Dashboard direction (CA, MRR, churn, leads→clients)
        - Distinction honoraires vs budget média dans les rapports
        - Templates QWeb personnalisés
        - Envoi automatique des rapports aux clients
    """,
    'author': 'MDMC Music Ads',
    'category': 'Reporting',
    'depends': [
        'base',
        'web',
        'mdmc_base',
        'mdmc_campaigns',
        'mdmc_sales',
    ],
    'data': [
        'report/campaign_report.xml',
        'report/dashboard_views.xml',
        'views/mdmc_reporting_menus.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}