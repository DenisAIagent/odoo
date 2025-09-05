{
    'name': 'MDMC Base',
    'version': '17.0.1.0.0',
    'summary': 'Configuration de base pour MDMC Music Ads',
    'description': """
        Module de base pour MDMC Music Ads contenant :
        - Configuration des rôles et groupes d'utilisateurs
        - Données communes (pays, plateformes publicitaires)
        - Configuration des emails et templates de base
        - Timezone Europe/Lisbon par défaut
    """,
    'author': 'MDMC Music Ads',
    'category': 'Base',
    'depends': [
        'base',
        'mail',
        'contacts',
        'web',
        'server_environment',  # OCA server-tools
        'auditlog',  # OCA server-tools
    ],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'data/res_country_data.xml',
        'data/platforms_data.xml',
        'data/mail_template_data.xml',
        'data/server_environment_data.xml',
    ],
    'demo': [
        'data/demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}