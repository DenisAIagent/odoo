from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)


class ContractContract(models.Model):
    _inherit = 'contract.contract'

    # Champs MDMC
    mdmc_total_monthly = fields.Monetary('Total Mensuel', compute='_compute_mdmc_monthly_total')
    mdmc_client_type = fields.Selection(related='partner_id.is_company', readonly=True)
    mdmc_platforms = fields.Many2many('mdmc.platform', compute='_compute_mdmc_platforms')
    
    # Commande d'origine
    sale_order_id = fields.Many2one('sale.order', string='Commande d\'Origine')

    @api.depends('contract_line_ids.price_subtotal')
    def _compute_mdmc_monthly_total(self):
        for contract in self:
            contract.mdmc_total_monthly = sum(contract.contract_line_ids.mapped('price_subtotal'))

    @api.depends('contract_line_ids.product_id.mdmc_platform_id')
    def _compute_mdmc_platforms(self):
        for contract in self:
            platforms = contract.contract_line_ids.mapped('product_id.mdmc_platform_id')
            contract.mdmc_platforms = [(6, 0, platforms.ids)]

    def action_contract_send(self):
        """Envoyer le contrat par email"""
        template = self.env.ref('mdmc_sales.mail_template_contract_recurring', raise_if_not_found=False)
        if template:
            return template.send_mail(self.id, force_send=True)
        return super().action_contract_send()


class ContractLine(models.Model):
    _inherit = 'contract.line'

    mdmc_platform_id = fields.Many2one('mdmc.platform', related='product_id.mdmc_platform_id', readonly=True)
    mdmc_is_agency_fee = fields.Boolean('Honoraires Agence', related='product_id.is_agency_fee', readonly=True)