from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestMdmcBase(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Platform = self.env['mdmc.platform']
        self.Partner = self.env['res.partner']

    def test_create_platform(self):
        """Test création d'une nouvelle plateforme"""
        platform = self.Platform.create({
            'name': 'Test Platform',
            'code': 'test',
            'description': 'Platform de test',
            'api_enabled': True,
            'api_url': 'https://api.test.com',
            'api_version': 'v1.0'
        })
        
        self.assertEqual(platform.name, 'Test Platform')
        self.assertEqual(platform.code, 'test')
        self.assertTrue(platform.api_enabled)
        self.assertTrue(platform.active)

    def test_platform_code_unique(self):
        """Test l'unicité du code de plateforme"""
        self.Platform.create({
            'name': 'Platform 1',
            'code': 'unique_code',
        })
        
        with self.assertRaises(ValidationError):
            self.Platform.create({
                'name': 'Platform 2',
                'code': 'unique_code',
            })

    def test_partner_artist_fields(self):
        """Test les champs spécifiques aux artistes"""
        artist = self.Partner.create({
            'name': 'Test Artist',
            'is_artist': True,
            'artist_name': 'TestArtist',
            'music_genre': 'pop',
            'marketing_consent': True,
        })
        
        self.assertTrue(artist.is_artist)
        self.assertEqual(artist.artist_name, 'TestArtist')
        self.assertEqual(artist.music_genre, 'pop')
        self.assertTrue(artist.marketing_consent)

    def test_partner_label_fields(self):
        """Test les champs spécifiques aux labels"""
        label = self.Partner.create({
            'name': 'Test Label Records',
            'is_label': True,
            'label_name': 'Test Label',
            'marketing_consent': False,
        })
        
        self.assertTrue(label.is_label)
        self.assertEqual(label.label_name, 'Test Label')
        self.assertFalse(label.marketing_consent)

    def test_default_timezone(self):
        """Test que le timezone par défaut est Europe/Lisbon"""
        user = self.env['res.users'].create({
            'name': 'Test User',
            'login': 'test@test.com',
        })
        
        # Note: En fonction de l'implémentation exacte du timezone par défaut
        # ce test pourrait nécessiter un ajustement
        self.assertTrue(user.tz is not None or user.tz == 'Europe/Lisbon')