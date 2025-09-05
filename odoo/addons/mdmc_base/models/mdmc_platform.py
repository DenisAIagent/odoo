from odoo import fields, models


class MdmcPlatform(models.Model):
    _name = 'mdmc.platform'
    _description = 'Plateformes Publicitaires'
    _order = 'sequence, name'

    name = fields.Char('Nom', required=True)
    code = fields.Char('Code', required=True, size=20)
    sequence = fields.Integer('Séquence', default=10)
    active = fields.Boolean('Actif', default=True)
    description = fields.Text('Description')
    color = fields.Integer('Couleur', default=1)
    
    # API configuration for integrations
    api_enabled = fields.Boolean('API Activée', default=False)
    api_url = fields.Char('URL API')
    api_version = fields.Char('Version API')
    
    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Le code de plateforme doit être unique !'),
    ]