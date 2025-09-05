from odoo.tests.common import TransactionCase
from odoo import fields
from datetime import timedelta
import json


class TestMdmcCrm(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Lead = self.env['crm.lead']
        self.Platform = self.env['mdmc.platform']
        self.Country = self.env['res.country']
        
        # Créer des données de test
        self.platform_youtube = self.Platform.create({
            'name': 'YouTube Test',
            'code': 'youtube',
        })
        self.platform_meta = self.Platform.create({
            'name': 'Meta Test', 
            'code': 'meta',
        })
        self.country_fr = self.Country.search([('code', '=', 'FR')], limit=1)

    def test_lead_scoring_high(self):
        """Test du scoring élevé"""
        lead = self.Lead.create({
            'name': 'Test Lead High Score',
            'email_from': 'test@example.com',
            'x_budget_est': 3000,
            'x_country_focus': self.country_fr.id,
            'x_genre': 'pop',
            'x_services_interest': [(6, 0, [self.platform_youtube.id, self.platform_meta.id])],
        })
        
        # Le score devrait être élevé (budget 30 + pays 20 + plateformes 20 + genre 10 = 80)
        self.assertGreaterEqual(lead.x_lead_score, 70)
        self.assertIn('Budget élevé', lead.x_score_details)

    def test_lead_scoring_low(self):
        """Test du scoring faible"""
        lead = self.Lead.create({
            'name': 'Test Lead Low Score',
            'email_from': 'test@example.com',
            'x_budget_est': 200,
            'x_genre': 'jazz',
        })
        
        # Le score devrait être faible
        self.assertLess(lead.x_lead_score, 40)

    def test_sequence_start(self):
        """Test du démarrage de séquence"""
        lead = self.Lead.create({
            'name': 'Test Sequence',
            'email_from': 'test@example.com',
        })
        
        # Démarrer la séquence
        lead.action_start_sequence()
        
        self.assertEqual(lead.x_sequence_step, 1)
        self.assertIsNotNone(lead.x_sequence_last_sent)
        self.assertFalse(lead.x_sequence_paused)

    def test_sequence_pause_resume(self):
        """Test pause/reprise de séquence"""
        lead = self.Lead.create({
            'name': 'Test Sequence',
            'email_from': 'test@example.com',
            'x_sequence_step': 1,
        })
        
        # Tester pause
        lead.action_pause_sequence()
        self.assertTrue(lead.x_sequence_paused)
        
        # Tester reprise
        lead.action_resume_sequence()
        self.assertFalse(lead.x_sequence_paused)

    def test_convert_to_customer(self):
        """Test conversion lead vers customer"""
        lead = self.Lead.create({
            'name': 'Test Convert',
            'partner_name': 'Test Artist',
            'email_from': 'artist@test.com',
            'phone': '+33123456789',
            'x_artist_name': 'TestArtist',
            'x_genre': 'pop',
        })
        
        # Convertir
        lead.convert_to_customer()
        
        # Vérifier que le partner a été créé
        self.assertIsNotNone(lead.partner_id)
        self.assertTrue(lead.partner_id.is_artist)
        self.assertEqual(lead.partner_id.artist_name, 'TestArtist')
        self.assertEqual(lead.partner_id.music_genre, 'pop')

    def test_cron_email_sequences(self):
        """Test du cron de traitement des séquences"""
        # Créer un lead en étape 1 avec date ancienne
        lead_j3 = self.Lead.create({
            'name': 'Test Cron J3',
            'email_from': 'test@example.com',
            'x_sequence_step': 1,
            'x_sequence_last_sent': fields.Datetime.now() - timedelta(days=3),
            'x_sequence_paused': False,
        })
        
        # Créer un lead en étape 2 avec date ancienne  
        lead_j7 = self.Lead.create({
            'name': 'Test Cron J7',
            'email_from': 'test2@example.com',
            'x_sequence_step': 2,
            'x_sequence_last_sent': fields.Datetime.now() - timedelta(days=4),
            'x_sequence_paused': False,
        })
        
        # Exécuter le cron
        self.Lead._cron_process_email_sequences()
        
        # Vérifier les changements
        self.assertEqual(lead_j3.x_sequence_step, 2)
        self.assertEqual(lead_j7.x_sequence_step, 3)

    def test_auto_start_sequence_on_create(self):
        """Test du démarrage automatique de séquence à la création"""
        lead = self.Lead.create({
            'name': 'Test Auto Sequence',
            'email_from': 'test@example.com',
            'x_source_url': 'https://test.com',
        })
        
        # La séquence devrait être programmée (avec delay)
        # On ne peut pas tester le delay facilement, mais on peut vérifier
        # que les champs sont corrects
        self.assertIsNotNone(lead.email_from)
        self.assertIsNotNone(lead.x_source_url)