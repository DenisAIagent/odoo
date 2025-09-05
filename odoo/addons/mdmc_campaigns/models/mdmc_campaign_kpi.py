from odoo import fields, models, api
from odoo.exceptions import ValidationError


class MdmcCampaignKpi(models.Model):
    _name = 'mdmc.campaign.kpi'
    _description = 'KPI Campagne MDMC'
    _order = 'date desc, platform'

    # Relations
    campaign_id = fields.Many2one('mdmc.campaign', string='Campagne', required=True, ondelete='cascade')
    partner_id = fields.Many2one('res.partner', related='campaign_id.partner_id', readonly=True, store=True)
    
    # Identifiants
    date = fields.Date('Date', required=True)
    platform = fields.Selection([
        ('youtube', 'YouTube'),
        ('meta', 'Meta (Facebook/Instagram)'),
        ('tiktok', 'TikTok'),
        ('spotify', 'Spotify'),
        ('twitter', 'X (Twitter)'),
        ('other', 'Autre'),
    ], string='Plateforme', required=True)
    
    # Métriques principales
    impressions = fields.Integer('Impressions', default=0)
    views = fields.Integer('Vues', default=0)
    clicks = fields.Integer('Clics', default=0)
    
    # Coûts
    spend = fields.Float('Dépense (€)', digits=(12, 2), default=0.0)
    cpc = fields.Float('CPC (€)', digits=(5, 4), default=0.0, help="Coût par clic")
    cpv = fields.Float('CPV (€)', digits=(5, 4), default=0.0, help="Coût par vue")
    cpm = fields.Float('CPM (€)', digits=(5, 2), default=0.0, help="Coût pour mille impressions")
    
    # Taux de performance
    ctr = fields.Float('CTR (%)', digits=(5, 2), default=0.0, help="Taux de clics")
    view_rate = fields.Float('Taux de Vue (%)', digits=(5, 2), default=0.0)
    
    # Conversions
    conversions = fields.Integer('Conversions', default=0)
    conversion_rate = fields.Float('Taux de Conversion (%)', digits=(5, 2), default=0.0)
    cost_per_conversion = fields.Float('Coût par Conversion (€)', digits=(5, 2), default=0.0)
    
    # Métriques spécifiques streaming/musique
    streams = fields.Integer('Streams', default=0, help="Streams générés (Spotify, etc.)")
    video_views_25 = fields.Integer('Vues 25%', default=0, help="Vues à 25% de la vidéo")
    video_views_50 = fields.Integer('Vues 50%', default=0, help="Vues à 50% de la vidéo")
    video_views_75 = fields.Integer('Vues 75%', default=0, help="Vues à 75% de la vidéo")
    video_views_100 = fields.Integer('Vues 100%', default=0, help="Vues complètes de la vidéo")
    
    # Engagement social
    likes = fields.Integer('Likes', default=0)
    shares = fields.Integer('Partages', default=0)
    comments = fields.Integer('Commentaires', default=0)
    saves = fields.Integer('Sauvegardes', default=0)
    
    # Métadonnées
    create_date = fields.Datetime('Créé le', readonly=True)
    create_uid = fields.Many2one('res.users', 'Créé par', readonly=True)
    
    _sql_constraints = [
        ('unique_campaign_date_platform', 
         'unique(campaign_id, date, platform)', 
         'Il ne peut y avoir qu\'un seul KPI par campagne, date et plateforme !'),
    ]

    @api.constrains('date', 'campaign_id')
    def _check_date_in_campaign_period(self):
        """Vérifier que la date KPI est dans la période de campagne"""
        for record in self:
            campaign = record.campaign_id
            if campaign.date_start and record.date < campaign.date_start:
                raise ValidationError(f"La date KPI ne peut pas être antérieure au début de campagne ({campaign.date_start})")
            if campaign.date_end and record.date > campaign.date_end:
                raise ValidationError(f"La date KPI ne peut pas être postérieure à la fin de campagne ({campaign.date_end})")

    def name_get(self):
        """Nom d'affichage personnalisé"""
        result = []
        for record in self:
            name = f"{record.campaign_id.name} - {record.platform.title()} - {record.date}"
            result.append((record.id, name))
        return result

    @api.model
    def upsert_kpi(self, campaign_ref, date, platform, kpi_data):
        """
        Méthode pour créer ou mettre à jour un KPI (utilisée par l'API)
        
        :param campaign_ref: Référence externe de la campagne
        :param date: Date du KPI (format YYYY-MM-DD)
        :param platform: Code de la plateforme
        :param kpi_data: Dictionnaire avec les données KPI
        """
        # Trouver la campagne
        campaign = self.env['mdmc.campaign'].find_by_external_ref(campaign_ref)
        if not campaign:
            raise ValidationError(f"Campagne non trouvée avec la référence : {campaign_ref}")
        
        # Chercher un KPI existant
        existing_kpi = self.search([
            ('campaign_id', '=', campaign.id),
            ('date', '=', date),
            ('platform', '=', platform),
        ])
        
        # Préparer les données
        vals = {
            'campaign_id': campaign.id,
            'date': date,
            'platform': platform,
            **kpi_data
        }
        
        if existing_kpi:
            # Mettre à jour
            existing_kpi.write(vals)
            return existing_kpi
        else:
            # Créer
            return self.create(vals)