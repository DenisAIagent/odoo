{
    'name': 'MDMC GDPR',
    'version': '17.0.1.0.0',
    'summary': 'Conformité RGPD pour MDMC Music Ads',
    'description': """
        Module de conformité RGPD pour MDMC Music Ads :
        - Wizard export/anonymisation contact
        - Journal d'audit complet (OCA auditlog)
        - Purge automatique des leads inactifs (24 mois)
        - Consentements marketing horodatés
        - Procédures de suppression/anonymisation
        - Rétention de données configurée
    """,
    'author': 'MDMC Music Ads',
    'category': 'Tools',
    'depends': [
        'base',
        'mdmc_base',
        'mdmc_crm',
        'auditlog',  # OCA server-tools
    ],
    'data': [
        'wizard/gdpr_export_wizard.xml',
        'wizard/gdpr_anonymize_wizard.xml',
        'data/cron_data.xml',
        'views/mdmc_gdpr_menus.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}