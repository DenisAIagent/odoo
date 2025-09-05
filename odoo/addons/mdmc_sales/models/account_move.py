from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    # Totaux MDMC
    mdmc_total_agency_fees = fields.Monetary('Total Honoraires Agence', compute='_compute_mdmc_totals', store=True)
    mdmc_total_media_budget = fields.Monetary('Total Budget Média (Déclaratif)', compute='_compute_mdmc_totals', store=True)
    
    # Classification
    mdmc_invoice_type = fields.Selection([
        ('agency_only', 'Honoraires Agence Uniquement'),
        ('mixed', 'Honoraires + Déclaratif'),
        ('other', 'Autre'),
    ], string='Type Facture MDMC', compute='_compute_mdmc_invoice_type', store=True)

    @api.depends('invoice_line_ids.product_id.mdmc_product_type', 'invoice_line_ids.price_subtotal')
    def _compute_mdmc_totals(self):
        for move in self:
            agency_total = 0.0
            media_total = 0.0
            
            for line in move.invoice_line_ids:
                if line.product_id and line.product_id.mdmc_product_type == 'agency_fee':
                    agency_total += line.price_subtotal
                elif line.product_id and line.product_id.mdmc_product_type == 'media_budget':
                    media_total += line.price_subtotal
            
            move.mdmc_total_agency_fees = agency_total
            move.mdmc_total_media_budget = media_total

    @api.depends('mdmc_total_agency_fees', 'mdmc_total_media_budget')
    def _compute_mdmc_invoice_type(self):
        for move in self:
            if move.mdmc_total_agency_fees > 0 and move.mdmc_total_media_budget == 0:
                move.mdmc_invoice_type = 'agency_only'
            elif move.mdmc_total_agency_fees > 0 and move.mdmc_total_media_budget > 0:
                move.mdmc_invoice_type = 'mixed'
            else:
                move.mdmc_invoice_type = 'other'


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    mdmc_is_agency_fee = fields.Boolean('Honoraires Agence', 
                                        related='product_id.is_agency_fee', readonly=True)
    mdmc_is_media_budget = fields.Boolean('Budget Média', 
                                          related='product_id.is_media_budget', readonly=True)
    mdmc_platform_id = fields.Many2one('mdmc.platform', 
                                       related='product_id.mdmc_platform_id', readonly=True)