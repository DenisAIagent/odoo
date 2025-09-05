import json
import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class MdmcCrmWebhook(http.Controller):

    @http.route('/api/mdmc/v1/leads/webhook', type='http', auth='none', methods=['POST'], csrf=False, cors='*')
    def capture_lead_webhook(self, **kwargs):
        """
        Endpoint webhook pour capturer les leads depuis le site externe
        
        Expected JSON payload:
        {
            "name": "Nom du prospect",
            "email": "email@example.com",
            "phone": "+33123456789",
            "artist_name": "Nom d'artiste",
            "label": "Nom du label",
            "genre": "pop",
            "budget_estimated": 1500.0,
            "country_code": "FR",
            "platforms_interest": ["youtube", "meta", "tiktok"],
            "source_url": "https://mdmc.com/contact",
            "utm_campaign": "summer_2025",
            "utm_medium": "organic",
            "utm_source": "website"
        }
        """
        try:
            # Parse JSON data
            if hasattr(request, 'jsonrequest') and request.jsonrequest:
                data = request.jsonrequest
            else:
                data = json.loads(request.httprequest.get_data(as_text=True))
            
            # Validation des champs obligatoires
            if not data.get('email'):
                return request.make_response(
                    json.dumps({'error': 'Email is required'}),
                    headers=[('Content-Type', 'application/json')],
                    status=400
                )
            
            # Préparer les valeurs du lead
            lead_vals = {
                'name': data.get('name', 'Nouveau Lead Web'),
                'contact_name': data.get('name'),
                'email_from': data.get('email'),
                'phone': data.get('phone'),
                'mobile': data.get('mobile'),
                'description': data.get('description', ''),
                'type': 'lead',
                'x_artist_name': data.get('artist_name'),
                'x_label': data.get('label'),
                'x_genre': data.get('genre'),
                'x_budget_est': float(data.get('budget_estimated', 0)),
                'x_source_url': data.get('source_url'),
                'x_utm_campaign': data.get('utm_campaign'),
                'x_utm_medium': data.get('utm_medium'),
                'x_utm_source': data.get('utm_source'),
            }
            
            # Gérer le pays
            country_code = data.get('country_code')
            if country_code:
                country = request.env['res.country'].sudo().search([
                    ('code', '=', country_code.upper())
                ], limit=1)
                if country:
                    lead_vals['country_id'] = country.id
                    lead_vals['x_country_focus'] = country.id
            
            # Gérer les plateformes d'intérêt
            platforms_interest = data.get('platforms_interest', [])
            if platforms_interest:
                platforms = request.env['mdmc.platform'].sudo().search([
                    ('code', 'in', platforms_interest)
                ])
                if platforms:
                    lead_vals['x_services_interest'] = [(6, 0, platforms.ids)]
            
            # Créer le lead
            lead = request.env['crm.lead'].sudo().create(lead_vals)
            
            _logger.info(f"Lead webhook créé avec succès - ID: {lead.id}, Email: {lead.email_from}")
            
            # Réponse de succès
            response_data = {
                'success': True,
                'lead_id': lead.id,
                'message': 'Lead created successfully'
            }
            
            return request.make_response(
                json.dumps(response_data),
                headers=[('Content-Type', 'application/json')],
                status=201
            )
            
        except json.JSONDecodeError:
            _logger.error("Webhook lead: Invalid JSON payload")
            return request.make_response(
                json.dumps({'error': 'Invalid JSON payload'}),
                headers=[('Content-Type', 'application/json')],
                status=400
            )
            
        except Exception as e:
            _logger.error(f"Erreur webhook lead: {str(e)}")
            return request.make_response(
                json.dumps({'error': 'Internal server error'}),
                headers=[('Content-Type', 'application/json')],
                status=500
            )

    @http.route('/api/mdmc/v1/leads/test', type='json', auth='none', methods=['GET'], csrf=False)
    def test_webhook_endpoint(self):
        """Endpoint de test pour vérifier que l'API est fonctionnelle"""
        return {
            'status': 'ok',
            'message': 'MDMC Leads Webhook API is working',
            'version': '1.0',
            'endpoints': {
                'create_lead': '/api/mdmc/v1/leads/webhook (POST)'
            }
        }