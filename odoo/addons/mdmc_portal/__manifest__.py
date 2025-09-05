{
    'name': 'MDMC Portal',
    'version': '17.0.1.0.0',
    'summary': 'Portail client pour MDMC Music Ads',
    'description': """
        Module portail client pour MDMC Music Ads :
        - Pages : Mes infos, Mes devis/factures, Mes campagnes, Mes rapports PDF, Mes tickets
        - Upload d'assets créatifs (Drive externe ou Documents si EE)
        - Suivi commandes et abonnements
        - Accès rapports de performance
        - Interface responsive et moderne
    """,
    'author': 'MDMC Music Ads',
    'category': 'Website/Website',
    'depends': [
        'portal',
        'website',
        'mdmc_base',
        'mdmc_campaigns',
        'mdmc_sales',
    ],
    'data': [
        'views/portal_templates.xml',
        'views/mdmc_portal_menus.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'mdmc_portal/static/src/css/portal_style.css',
            'mdmc_portal/static/src/js/portal_charts.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}