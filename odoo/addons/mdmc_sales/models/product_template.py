from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Classification MDMC
    mdmc_product_type = fields.Selection([
        ('agency_fee', 'Honoraires d\'Agence'),
        ('media_budget', 'Budget Média (Déclaratif)'),
        ('service', 'Service Ponctuel'),
        ('other', 'Autre'),
    ], string='Type Produit MDMC', default='other')
    
    mdmc_platform_id = fields.Many2one('mdmc.platform', string='Plateforme Associée')
    mdmc_recurring = fields.Boolean('Abonnement Récurrent', default=False, 
                                    help="Si coché, ce produit sera disponible pour les abonnements")
    
    # Champs pour différencier les types de produits
    is_agency_fee = fields.Boolean('Est Honoraires d\'Agence', compute='_compute_is_agency_fee', store=True)
    is_media_budget = fields.Boolean('Est Budget Média', compute='_compute_is_media_budget', store=True)
    
    def _compute_is_agency_fee(self):
        for product in self:
            product.is_agency_fee = product.mdmc_product_type == 'agency_fee'
    
    def _compute_is_media_budget(self):
        for product in self:
            product.is_media_budget = product.mdmc_product_type == 'media_budget'