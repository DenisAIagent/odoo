{
    'name': 'MDMC Sales',
    'version': '17.0.1.0.0',
    'summary': 'Gestion des ventes pour MDMC Music Ads',
    'description': """
        Module de ventes pour MDMC Music Ads :
        - Produits honoraires d'agence (200€ HT/mois/plateforme)
        - Facturation immédiate à la confirmation
        - Abonnements récurrents mensuels (OCA contract)
        - Intégration paiements en ligne
        - Distinction honoraires vs budget média (non facturé)
        - Templates de devis/factures personnalisés
    """,
    'author': 'MDMC Music Ads',
    'category': 'Sales',
    'depends': [
        'sale_management',
        'account',
        'payment',
        'mdmc_base',
        'mdmc_crm',
        'contract',  # OCA contract
        'contract_sale',  # OCA contract
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/record_rules.xml',
        'data/product_data.xml',
        'data/mail_template_data.xml',
        'data/payment_data.xml',
        'views/product_template_views.xml',
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
        'views/contract_views.xml',
        'views/mdmc_sales_menus.xml',
        'report/sale_order_report.xml',
        'report/account_invoice_report.xml',
    ],
    'demo': [
        'data/demo_data.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}