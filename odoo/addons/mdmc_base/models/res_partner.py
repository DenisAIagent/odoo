from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # RGPD consent fields
    marketing_consent = fields.Boolean('Consentement Marketing', default=False)
    marketing_consent_date = fields.Datetime('Date Consentement Marketing')
    gdpr_anonymized = fields.Boolean('Anonymisé RGPD', default=False)
    gdpr_anonymized_date = fields.Datetime('Date Anonymisation')
    
    # Artist/Label specific fields
    is_artist = fields.Boolean('Est un Artiste', default=False)
    is_label = fields.Boolean('Est un Label', default=False)
    artist_name = fields.Char('Nom d\'artiste')
    label_name = fields.Char('Nom du label')
    music_genre = fields.Selection([
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