from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class MdmcCampaign(models.Model):
    _name = 'mdmc.campaign'
    _description = 'Campagne MDMC'
    _order = 'create_date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Informations de base
    name = fields.Char('Nom de Campagne', required=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Client', required=True, tracking=True)
    user_id = fields.Many2one('res.users', string='Chef de Projet', default=lambda self: self.env.user, tracking=True)
    
    # Dates
    date_start = fields.Date('Date de Début', required=True, tracking=True)
    date_end = fields.Date('Date de Fin', tracking=True)
    
    # États
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('running', 'En Cours'),
        ('paused', 'En Pause'),
        ('done', 'Terminée'),
        ('cancelled', 'Annulée'),
    ], string='État', default='draft', tracking=True)
    
    # Plateformes et budgets déclaratifs
    platform_ids = fields.Many2many('mdmc.platform', string='Plateformes')
    
    # Budgets déclaratifs par plateforme
    budget_youtube = fields.Float('Budget YouTube (€)', help="Budget déclaratif YouTube")
    budget_meta = fields.Float('Budget Meta (€)', help="Budget déclaratif Facebook/Instagram")
    budget_tiktok = fields.Float('Budget TikTok (€)', help="Budget déclaratif TikTok")
    budget_spotify = fields.Float('Budget Spotify (€)', help="Budget déclaratif Spotify")
    budget_other = fields.Float('Autres Budgets (€)', help="Autres plateformes")
    
    budget_total = fields.Float('Budget Total (€)', compute='_compute_budget_total', store=True)
    
    # SmartLink
    smartlink_url = fields.Char('URL SmartLink', help="URL du SmartLink pour cette campagne")
    
    # KPIs agrégés (calculés)
    kpi_total_spend = fields.Float('Dépense Totale (€)', compute='_compute_kpi_totals')
    kpi_total_impressions = fields.Integer('Impressions Totales', compute='_compute_kpi_totals')
    kpi_total_views = fields.Integer('Vues Totales', compute='_compute_kpi_totals')
    kpi_total_clicks = fields.Integer('Clics Totaux', compute='_compute_kpi_totals')
    kpi_avg_ctr = fields.Float('CTR Moyen (%)', compute='_compute_kpi_totals', digits=(5, 2))
    kpi_avg_cpv = fields.Float('CPV Moyen (€)', compute='_compute_kpi_totals', digits=(5, 4))
    kpi_total_conversions = fields.Integer('Conversions Totales', compute='_compute_kpi_totals')
    
    # Alertes budget
    budget_alert_threshold = fields.Float('Seuil d\'Alerte Budget (%)', default=90.0)
    budget_exceeded = fields.Boolean('Budget Dépassé', compute='_compute_budget_status')
    budget_utilization = fields.Float('Utilisation Budget (%)', compute='_compute_budget_status')
    
    # Relations
    kpi_ids = fields.One2many('mdmc.campaign.kpi', 'campaign_id', string='KPIs')
    sale_order_id = fields.Many2one('sale.order', string='Commande Associée')
    
    # Référence externe pour API
    external_ref = fields.Char('Référence Externe', help="Référence utilisée par les intégrations externes")

    @api.depends('budget_youtube', 'budget_meta', 'budget_tiktok', 'budget_spotify', 'budget_other')
    def _compute_budget_total(self):
        for campaign in self:
            campaign.budget_total = (
                campaign.budget_youtube + 
                campaign.budget_meta + 
                campaign.budget_tiktok + 
                campaign.budget_spotify + 
                campaign.budget_other
            )

    @api.depends('kpi_ids.spend', 'kpi_ids.impressions', 'kpi_ids.views', 'kpi_ids.clicks')
    def _compute_kpi_totals(self):
        for campaign in self:
            kpis = campaign.kpi_ids
            
            campaign.kpi_total_spend = sum(kpis.mapped('spend'))
            campaign.kpi_total_impressions = sum(kpis.mapped('impressions'))
            campaign.kpi_total_views = sum(kpis.mapped('views'))
            campaign.kpi_total_clicks = sum(kpis.mapped('clicks'))
            campaign.kpi_total_conversions = sum(kpis.mapped('conversions'))
            
            # CTR moyen pondéré
            if campaign.kpi_total_impressions > 0:
                campaign.kpi_avg_ctr = (campaign.kpi_total_clicks / campaign.kpi_total_impressions) * 100
            else:
                campaign.kpi_avg_ctr = 0.0
            
            # CPV moyen pondéré
            if campaign.kpi_total_views > 0:
                campaign.kpi_avg_cpv = campaign.kpi_total_spend / campaign.kpi_total_views
            else:
                campaign.kpi_avg_cpv = 0.0

    @api.depends('budget_total', 'kpi_total_spend', 'budget_alert_threshold')
    def _compute_budget_status(self):
        for campaign in self:
            if campaign.budget_total > 0:
                campaign.budget_utilization = (campaign.kpi_total_spend / campaign.budget_total) * 100
                campaign.budget_exceeded = campaign.budget_utilization > campaign.budget_alert_threshold
            else:
                campaign.budget_utilization = 0.0
                campaign.budget_exceeded = False

    def action_start_campaign(self):
        """Démarrer la campagne"""
        self.state = 'running'
        self.message_post(body="Campagne démarrée")

    def action_pause_campaign(self):
        """Mettre en pause la campagne"""
        self.state = 'paused'
        self.message_post(body="Campagne mise en pause")

    def action_resume_campaign(self):
        """Reprendre la campagne"""
        self.state = 'running'
        self.message_post(body="Campagne reprise")

    def action_end_campaign(self):
        """Terminer la campagne"""
        self.state = 'done'
        self.date_end = fields.Date.today()
        self.message_post(body="Campagne terminée")

    def action_view_kpis(self):
        """Action pour voir les KPIs détaillés"""
        return {
            'name': f'KPIs - {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'mdmc.campaign.kpi',
            'view_mode': 'tree,form,graph',
            'domain': [('campaign_id', '=', self.id)],
            'context': {
                'default_campaign_id': self.id,
                'search_default_group_by_date': 1,
                'search_default_group_by_platform': 1,
            }
        }

    @api.model
    def _cron_check_budget_alerts(self):
        """Cron pour vérifier les alertes de dépassement de budget"""
        campaigns_exceeded = self.search([
            ('state', '=', 'running'),
            ('budget_exceeded', '=', True),
        ])
        
        for campaign in campaigns_exceeded:
            # Envoyer alerte par email
            template = self.env.ref('mdmc_campaigns.mail_template_budget_alert', raise_if_not_found=False)
            if template:
                template.send_mail(campaign.id)
            
            # Log
            _logger.warning(f"Budget alert for campaign {campaign.name}: {campaign.budget_utilization:.1f}% used")

    @api.model
    def find_by_external_ref(self, external_ref):
        """Trouver une campagne par sa référence externe"""
        return self.search([('external_ref', '=', external_ref)], limit=1)

    @api.model_create_multi
    def create(self, vals_list):
        """Override pour générer référence externe automatiquement"""
        campaigns = super().create(vals_list)
        
        for campaign in campaigns:
            if not campaign.external_ref:
                campaign.external_ref = f"CMP-{campaign.id:06d}"
        
        return campaigns