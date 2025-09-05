{
    'name': 'MDMC Helpdesk',
    'version': '17.0.1.0.0',
    'summary': 'Support client pour MDMC Music Ads',
    'description': """
        Module de support client pour MDMC Music Ads :
        - Tickets par email/portail
        - SLA simples et routage par catégories
        - Intégration OCA helpdesk_mgmt
        - Catégories : facturation/technique/campagne
        - Portail client pour suivi tickets
    """,
    'author': 'MDMC Music Ads',
    'category': 'Services/Helpdesk',
    'depends': [
        'helpdesk_mgmt',  # OCA helpdesk
        'mdmc_base',
        'mdmc_portal',
    ],
    'data': [
        'data/helpdesk_data.xml',
        'views/helpdesk_views.xml',
        'views/mdmc_helpdesk_menus.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}