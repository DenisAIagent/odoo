from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    # Champs spécifiques MDMC
    x_artist_name = fields.Char('Nom d\'Artiste', help="Nom d'artiste ou de scène")
    x_label = fields.Char('Label', help="Nom du label de musique")
    x_genre = fields.Selection([
        ('pop', 'Pop'),
        ('rock', 'Rock'),
        ('hip_hop', 'Hip Hop/Rap'),
        ('electronic', 'Electronic'),
        ('jazz', 'Jazz'),
        ('classical', 'Classical'),
        ('country', 'Country'),
        ('r_n_b', 'R&B/Soul'),
        ('reggae', 'Reggae'),
        ('metal', 'Metal'),
        ('indie', 'Indie'),
        ('world', 'World Music'),
        ('other', 'Autre'),
    ], string='Genre Musical')
    
    # Plateformes d'intérêt (many2many avec mdmc.platform)
    x_services_interest = fields.Many2many(
        'mdmc.platform', 
        string='Plateformes d\'Intérêt',
        help="Plateformes publicitaires qui intéressent le prospect"
    )
    
    # Budget et géographie
    x_budget_est = fields.Float('Budget Estimé (€/mois)', help="Budget mensuel estimé pour les campagnes")
    x_country_focus = fields.Many2one('res.country', string='Pays Focus', help="Pays principal pour les campagnes")
    
    # Scoring
    x_lead_score = fields.Integer('Score Lead', compute='_compute_lead_score', store=True, help="Score automatique du lead")
    x_score_details = fields.Text('Détails du Score', compute='_compute_lead_score', store=True)
    
    # Source et tracking
    x_source_url = fields.Char('URL Source', help="URL d'origine du lead (si vient d'un formulaire web)")
    x_utm_campaign = fields.Char('UTM Campaign')
    x_utm_medium = fields.Char('UTM Medium') 
    x_utm_source = fields.Char('UTM Source')
    
    # Séquence d'emailing
    x_sequence_step = fields.Integer('Étape Séquence', default=0, help="Étape actuelle dans la séquence d'emailing")
    x_sequence_last_sent = fields.Datetime('Dernier Email Séquence')
    x_sequence_paused = fields.Boolean('Séquence en Pause', default=False)

    @api.depends('x_budget_est', 'x_services_interest', 'x_country_focus', 'x_genre')
    def _compute_lead_score(self):
        """Calcul automatique du score de lead"""
        for lead in self:
            score = 0
            details = []
            
            # Score budget (40 points max)
            if lead.x_budget_est:
                if lead.x_budget_est >= 5000:
                    score += 40
                    details.append("Budget excellent (≥5000€): +40 pts")
                elif lead.x_budget_est >= 2000:
                    score += 30
                    details.append("Budget élevé (≥2000€): +30 pts")
                elif lead.x_budget_est >= 1000:
                    score += 20
                    details.append("Budget moyen (≥1000€): +20 pts")
                elif lead.x_budget_est >= 500:
                    score += 10
                    details.append("Budget faible (≥500€): +10 pts")
                else:
                    details.append("Budget très faible (<500€): +0 pts")
            
            # Score plateformes (30 points max)
            nb_platforms = len(lead.x_services_interest)
            if nb_platforms >= 3:
                score += 30
                details.append(f"Multi-plateforme ({nb_platforms}): +30 pts")
            elif nb_platforms == 2:
                score += 20
                details.append("2 plateformes: +20 pts")
            elif nb_platforms == 1:
                score += 10
                details.append("1 plateforme: +10 pts")
            else:
                details.append("Aucune plateforme: +0 pts")
            
            # Score géographique (20 points max)
            if lead.x_country_focus:
                high_value_countries = ['FR', 'US', 'GB', 'CA', 'AU', 'DE']
                if lead.x_country_focus.code in high_value_countries:
                    score += 20
                    details.append(f"Pays à fort potentiel ({lead.x_country_focus.name}): +20 pts")
                else:
                    score += 10
                    details.append(f"Autres pays ({lead.x_country_focus.name}): +10 pts")
            
            # Score genre musical (10 points max)
            if lead.x_genre:
                high_demand_genres = ['pop', 'hip_hop', 'electronic', 'indie']
                if lead.x_genre in high_demand_genres:
                    score += 10
                    details.append(f"Genre à forte demande ({lead.x_genre}): +10 pts")
                else:
                    score += 5
                    details.append(f"Autre genre ({lead.x_genre}): +5 pts")
            
            lead.x_lead_score = score
            lead.x_score_details = '\n'.join(details)

    def action_start_sequence(self):
        """Démarrer la séquence d'emailing pour ce lead"""
        for lead in self:
            if not lead.x_sequence_paused:
                lead.x_sequence_step = 1
                lead.x_sequence_last_sent = fields.Datetime.now()
                lead.with_delay()._send_sequence_email()
    
    def action_pause_sequence(self):
        """Mettre en pause la séquence"""
        self.x_sequence_paused = True
    
    def action_resume_sequence(self):
        """Reprendre la séquence"""
        self.x_sequence_paused = False

    def _send_sequence_email(self):
        """Envoyer l'email correspondant à l'étape de la séquence"""
        template_mapping = {
            1: 'mdmc_base.mail_template_prospection_j0',  # J+0
            2: 'mdmc_crm.mail_template_prospection_j3',   # J+3
            3: 'mdmc_crm.mail_template_prospection_j7',   # J+7
        }
        
        if self.x_sequence_step in template_mapping:
            template = self.env.ref(template_mapping[self.x_sequence_step], raise_if_not_found=False)
            if template:
                try:
                    template.send_mail(self.id, force_send=True)
                    _logger.info(f"Email séquence étape {self.x_sequence_step} envoyé pour lead {self.id}")
                except Exception as e:
                    _logger.error(f"Erreur envoi email séquence pour lead {self.id}: {e}")

    @api.model
    def _cron_process_email_sequences(self):
        """Traiter les séquences d'emailing (cron quotidien)"""
        # Leads à J+3 (étape 2)
        leads_j3 = self.search([
            ('x_sequence_step', '=', 1),
            ('x_sequence_paused', '=', False),
            ('x_sequence_last_sent', '<=', fields.Datetime.now() - fields.timedelta(days=3)),
            ('stage_id.is_won', '=', False),
        ])
        
        for lead in leads_j3:
            lead.x_sequence_step = 2
            lead.x_sequence_last_sent = fields.Datetime.now()
            lead.with_delay()._send_sequence_email()
        
        # Leads à J+7 (étape 3)
        leads_j7 = self.search([
            ('x_sequence_step', '=', 2),
            ('x_sequence_paused', '=', False),
            ('x_sequence_last_sent', '<=', fields.Datetime.now() - fields.timedelta(days=4)),
            ('stage_id.is_won', '=', False),
        ])
        
        for lead in leads_j7:
            lead.x_sequence_step = 3
            lead.x_sequence_last_sent = fields.Datetime.now()
            lead.with_delay()._send_sequence_email()
        
        _logger.info(f"Séquences d'emailing traitées: {len(leads_j3)} leads J+3, {len(leads_j7)} leads J+7")

    def convert_to_customer(self):
        """Conversion lead vers customer avec données spécifiques"""
        for lead in self:
            if not lead.partner_id:
                # Créer le partner avec les données MDMC
                partner_vals = {
                    'name': lead.partner_name or lead.name,
                    'email': lead.email_from,
                    'phone': lead.phone,
                    'mobile': lead.mobile,
                    'street': lead.street,
                    'street2': lead.street2,
                    'city': lead.city,
                    'zip': lead.zip,
                    'country_id': lead.country_id.id,
                    'state_id': lead.state_id.id,
                    'customer_rank': 1,
                    'is_artist': bool(lead.x_artist_name),
                    'is_label': bool(lead.x_label),
                    'artist_name': lead.x_artist_name,
                    'label_name': lead.x_label,
                    'music_genre': lead.x_genre,
                    'marketing_consent': True,
                    'marketing_consent_date': fields.Datetime.now(),
                }
                
                partner = self.env['res.partner'].create(partner_vals)
                lead.partner_id = partner.id
                
                # Envoyer email de bienvenue
                welcome_template = self.env.ref('mdmc_base.mail_template_welcome', raise_if_not_found=False)
                if welcome_template:
                    welcome_template.send_mail(partner.id, force_send=True)
        
        return super().convert_to_customer()

    @api.model_create_multi
    def create(self, vals_list):
        """Override create pour démarrer automatiquement les séquences"""
        leads = super().create(vals_list)
        
        for lead in leads:
            # Auto-start séquence si lead vient du web et a un email
            if lead.email_from and lead.x_source_url:
                lead.with_delay(eta=60).action_start_sequence()  # Démarrer après 1 minute
        
        return leads