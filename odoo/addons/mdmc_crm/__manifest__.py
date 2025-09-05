{
    'name': 'MDMC CRM',
    'version': '17.0.1.0.0',
    'summary': 'CRM adapté pour MDMC Music Ads',
    'description': """
        Extension CRM pour MDMC Music Ads :
        - Champs spécifiques artistes/labels (genre, budget, pays focus)
        - Scoring automatique des leads
        - Séquences d'emailing de prospection
        - Capture de leads via webhook
        - Kanban avec scoring et activités
    """,
    'author': 'MDMC Music Ads',
    'category': 'Sales/CRM',
    'depends': [
        'crm',
        'mail',
        'mass_mailing',
        'mdmc_base',
        'queue_job',  # OCA server-tools
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/record_rules.xml',
        'data/crm_stage_data.xml',
        'data/mail_template_data.xml',
        'data/cron_data.xml',
        'views/crm_lead_views.xml',
        'views/mdmc_crm_menus.xml',
    ],
    'demo': [
        'data/demo_data.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}