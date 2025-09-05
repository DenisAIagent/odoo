from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Totaux MDMC
    mdmc_total_agency_fees = fields.Monetary('Total Honoraires Agence', compute='_compute_mdmc_totals', store=True)
    mdmc_total_media_budget = fields.Monetary('Total Budget Média (Déclaratif)', compute='_compute_mdmc_totals', store=True)
    
    # Abonnement
    mdmc_is_subscription = fields.Boolean('Commande d\'Abonnement', default=False)
    mdmc_contract_id = fields.Many2one('contract.contract', string='Contrat Associé', readonly=True)
    
    # Paiement
    mdmc_payment_mode = fields.Selection([
        ('immediate', 'Paiement Immédiat (100%)'),
        ('subscription', 'Abonnement Mensuel'),
    ], string='Mode de Paiement', default='immediate')

    @api.depends('order_line.product_id.mdmc_product_type', 'order_line.price_subtotal')
    def _compute_mdmc_totals(self):
        for order in self:
            agency_total = 0.0
            media_total = 0.0
            
            for line in order.order_line:
                if line.product_id.mdmc_product_type == 'agency_fee':
                    agency_total += line.price_subtotal
                elif line.product_id.mdmc_product_type == 'media_budget':
                    media_total += line.price_subtotal
            
            order.mdmc_total_agency_fees = agency_total
            order.mdmc_total_media_budget = media_total

    def action_confirm(self):
        """Override pour facturation immédiate des honoraires"""
        result = super().action_confirm()
        
        for order in self:
            if order.mdmc_payment_mode == 'immediate' and order.mdmc_total_agency_fees > 0:
                # Facturer immédiatement les honoraires d'agence
                order._create_immediate_invoice()
            elif order.mdmc_payment_mode == 'subscription':
                # Créer le contrat d'abonnement
                order._create_subscription_contract()
        
        return result

    def _create_immediate_invoice(self):
        """Créer une facture immédiate pour les honoraires d'agence"""
        # Filtrer les lignes honoraires uniquement
        agency_lines = self.order_line.filtered(lambda l: l.product_id.mdmc_product_type == 'agency_fee')
        
        if not agency_lines:
            return
        
        # Créer la facture
        invoice_vals = self._prepare_invoice()
        invoice = self.env['account.move'].create(invoice_vals)
        
        # Créer les lignes de facture pour les honoraires uniquement
        for line in agency_lines:
            line_vals = line._prepare_invoice_line(sequence=10)
            line_vals['move_id'] = invoice.id
            self.env['account.move.line'].create(line_vals)
        
        # Calculer les totaux et confirmer
        invoice._onchange_invoice_line_ids()
        
        # Envoyer par email
        template = self.env.ref('mdmc_sales.mail_template_invoice_agency_fees', raise_if_not_found=False)
        if template:
            template.send_mail(invoice.id, force_send=True)
        
        _logger.info(f"Facture immédiate créée pour commande {self.name} - Montant: {invoice.amount_total}€")

    def _create_subscription_contract(self):
        """Créer un contrat d'abonnement OCA"""
        # Filtrer les lignes récurrentes
        recurring_lines = self.order_line.filtered(lambda l: l.product_id.mdmc_recurring)
        
        if not recurring_lines:
            return
        
        # Préparer les valeurs du contrat
        contract_vals = {
            'name': f"Abonnement MDMC - {self.partner_id.name}",
            'partner_id': self.partner_id.id,
            'company_id': self.company_id.id,
            'currency_id': self.currency_id.id,
            'contract_type': 'sale',
            'recurring_rule_type': 'monthly',
            'recurring_interval': 1,
            'date_start': fields.Date.today(),
            'sale_order_id': self.id,
        }
        
        contract = self.env['contract.contract'].create(contract_vals)
        
        # Créer les lignes du contrat
        for line in recurring_lines:
            line_vals = {
                'contract_id': contract.id,
                'product_id': line.product_id.id,
                'name': line.name,
                'quantity': line.product_uom_qty,
                'uom_id': line.product_uom.id,
                'price_unit': line.price_unit,
                'discount': line.discount,
            }
            self.env['contract.line'].create(line_vals)
        
        # Lier le contrat à la commande
        self.mdmc_contract_id = contract.id
        self.mdmc_is_subscription = True
        
        _logger.info(f"Contrat d'abonnement créé pour commande {self.name} - ID: {contract.id}")

    def action_create_media_budget_lines(self):
        """Action pour ajouter des lignes de budget média déclaratives"""
        return {
            'name': 'Ajouter Budget Média',
            'type': 'ir.actions.act_window',
            'res_model': 'mdmc.sales.media.budget.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_sale_order_id': self.id,
            }
        }


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    mdmc_is_agency_fee = fields.Boolean('Honoraires Agence', 
                                        related='product_id.is_agency_fee', readonly=True)
    mdmc_is_media_budget = fields.Boolean('Budget Média', 
                                          related='product_id.is_media_budget', readonly=True)
    mdmc_platform_id = fields.Many2one('mdmc.platform', 
                                       related='product_id.mdmc_platform_id', readonly=True)

    @api.onchange('product_id')
    def _onchange_product_id_mdmc(self):
        """Personnaliser la description selon le type MDMC"""
        if self.product_id and self.product_id.mdmc_product_type == 'media_budget':
            self.name = f"[DÉCLARATIF] {self.product_id.name} - Budget payé directement aux plateformes"