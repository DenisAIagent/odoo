import json
import logging
from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError, AccessError

_logger = logging.getLogger(__name__)


class MdmcKpiApi(http.Controller):

    def _check_api_auth(self):
        """Vérifier l'authentification API via token"""
        api_key = request.httprequest.headers.get('X-API-KEY')
        if not api_key:
            return False
        
        # Récupérer le token depuis la configuration système
        expected_token = request.env['ir.config_parameter'].sudo().get_param('mdmc.api.kpi_token')
        if not expected_token:
            _logger.error("MDMC API token not configured in system parameters")
            return False
        
        return api_key == expected_token

    @http.route('/api/mdmc/v1/kpis/ingest', type='http', auth='none', methods=['POST'], csrf=False, cors='*')
    def ingest_kpis(self, **kwargs):
        """
        API endpoint pour ingérer les KPIs depuis n8n
        
        Expected JSON payload:
        {
            "campaign_ref": "CMP-000001",
            "date": "2025-09-05",
            "platform": "youtube",
            "impressions": 123456,
            "views": 34567,
            "clicks": 789,
            "spend": 123.45,
            "ctr": 0.64,
            "cpv": 0.0036,
            "cpc": 0.157,
            "conversions": 42,
            "streams": 1250
        }
        """
        try:
            # Vérifier l'authentification
            if not self._check_api_auth():
                return request.make_response(
                    json.dumps({'error': 'Unauthorized - Invalid API key'}),
                    headers=[('Content-Type', 'application/json')],
                    status=401
                )
            
            # Parser les données JSON
            if hasattr(request, 'jsonrequest') and request.jsonrequest:
                data = request.jsonrequest
            else:
                data = json.loads(request.httprequest.get_data(as_text=True))
            
            # Validation des champs obligatoires
            required_fields = ['campaign_ref', 'date', 'platform']
            for field in required_fields:
                if not data.get(field):
                    return request.make_response(
                        json.dumps({'error': f'Missing required field: {field}'}),
                        headers=[('Content-Type', 'application/json')],
                        status=400
                    )
            
            # Extraire les données KPI
            kpi_data = {}
            kpi_fields = [
                'impressions', 'views', 'clicks', 'spend', 'ctr', 'cpv', 'cpc', 'cpm',
                'conversions', 'conversion_rate', 'cost_per_conversion',
                'streams', 'video_views_25', 'video_views_50', 'video_views_75', 'video_views_100',
                'likes', 'shares', 'comments', 'saves', 'view_rate'
            ]
            
            for field in kpi_fields:
                if field in data:
                    try:
                        if field in ['impressions', 'views', 'clicks', 'conversions', 'streams', 
                                   'video_views_25', 'video_views_50', 'video_views_75', 'video_views_100',
                                   'likes', 'shares', 'comments', 'saves']:
                            kpi_data[field] = int(data[field])
                        else:
                            kpi_data[field] = float(data[field])
                    except (ValueError, TypeError):
                        return request.make_response(
                            json.dumps({'error': f'Invalid value for field {field}: {data[field]}'}),
                            headers=[('Content-Type', 'application/json')],
                            status=400
                        )
            
            # Upsert KPI
            kpi_model = request.env['mdmc.campaign.kpi'].sudo()
            kpi = kpi_model.upsert_kpi(
                campaign_ref=data['campaign_ref'],
                date=data['date'],
                platform=data['platform'],
                kpi_data=kpi_data
            )
            
            _logger.info(f"KPI ingested successfully - Campaign: {data['campaign_ref']}, "
                        f"Platform: {data['platform']}, Date: {data['date']}, ID: {kpi.id}")
            
            # Réponse de succès
            response_data = {
                'success': True,
                'kpi_id': kpi.id,
                'campaign_ref': data['campaign_ref'],
                'date': data['date'],
                'platform': data['platform'],
                'message': 'KPI ingested successfully'
            }
            
            return request.make_response(
                json.dumps(response_data),
                headers=[('Content-Type', 'application/json')],
                status=200
            )
            
        except ValidationError as e:
            _logger.error(f"Validation error in KPI ingestion: {str(e)}")
            return request.make_response(
                json.dumps({'error': f'Validation error: {str(e)}'}),
                headers=[('Content-Type', 'application/json')],
                status=400
            )
            
        except json.JSONDecodeError:
            _logger.error("KPI API: Invalid JSON payload")
            return request.make_response(
                json.dumps({'error': 'Invalid JSON payload'}),
                headers=[('Content-Type', 'application/json')],
                status=400
            )
            
        except Exception as e:
            _logger.error(f"Erreur KPI API: {str(e)}")
            return request.make_response(
                json.dumps({'error': 'Internal server error'}),
                headers=[('Content-Type', 'application/json')],
                status=500
            )

    @http.route('/api/mdmc/v1/kpis/bulk', type='http', auth='none', methods=['POST'], csrf=False, cors='*')
    def ingest_bulk_kpis(self, **kwargs):
        """
        API endpoint pour ingérer plusieurs KPIs en une fois
        
        Expected JSON payload:
        {
            "kpis": [
                {
                    "campaign_ref": "CMP-000001",
                    "date": "2025-09-05",
                    "platform": "youtube",
                    "impressions": 123456,
                    ...
                },
                {
                    "campaign_ref": "CMP-000001", 
                    "date": "2025-09-05",
                    "platform": "meta",
                    ...
                }
            ]
        }
        """
        try:
            # Vérifier l'authentification
            if not self._check_api_auth():
                return request.make_response(
                    json.dumps({'error': 'Unauthorized - Invalid API key'}),
                    headers=[('Content-Type', 'application/json')],
                    status=401
                )
            
            # Parser les données JSON
            if hasattr(request, 'jsonrequest') and request.jsonrequest:
                data = request.jsonrequest
            else:
                data = json.loads(request.httprequest.get_data(as_text=True))
            
            if 'kpis' not in data or not isinstance(data['kpis'], list):
                return request.make_response(
                    json.dumps({'error': 'Missing or invalid kpis array'}),
                    headers=[('Content-Type', 'application/json')],
                    status=400
                )
            
            results = []
            errors = []
            
            # Traiter chaque KPI
            for i, kpi_data in enumerate(data['kpis']):
                try:
                    # Validation des champs obligatoires
                    required_fields = ['campaign_ref', 'date', 'platform']
                    for field in required_fields:
                        if not kpi_data.get(field):
                            errors.append(f"KPI {i}: Missing required field: {field}")
                            continue
                    
                    if errors:
                        continue
                    
                    # Extraire et processer comme dans l'endpoint simple
                    kpi_fields_data = {}
                    kpi_fields = [
                        'impressions', 'views', 'clicks', 'spend', 'ctr', 'cpv', 'cpc', 'cpm',
                        'conversions', 'conversion_rate', 'cost_per_conversion',
                        'streams', 'video_views_25', 'video_views_50', 'video_views_75', 'video_views_100',
                        'likes', 'shares', 'comments', 'saves', 'view_rate'
                    ]
                    
                    for field in kpi_fields:
                        if field in kpi_data:
                            if field in ['impressions', 'views', 'clicks', 'conversions', 'streams',
                                       'video_views_25', 'video_views_50', 'video_views_75', 'video_views_100',
                                       'likes', 'shares', 'comments', 'saves']:
                                kpi_fields_data[field] = int(kpi_data[field])
                            else:
                                kpi_fields_data[field] = float(kpi_data[field])
                    
                    # Upsert KPI
                    kpi_model = request.env['mdmc.campaign.kpi'].sudo()
                    kpi = kpi_model.upsert_kpi(
                        campaign_ref=kpi_data['campaign_ref'],
                        date=kpi_data['date'],
                        platform=kpi_data['platform'],
                        kpi_data=kpi_fields_data
                    )
                    
                    results.append({
                        'index': i,
                        'kpi_id': kpi.id,
                        'campaign_ref': kpi_data['campaign_ref'],
                        'date': kpi_data['date'],
                        'platform': kpi_data['platform'],
                        'status': 'success'
                    })
                    
                except Exception as e:
                    errors.append(f"KPI {i}: {str(e)}")
            
            _logger.info(f"Bulk KPI ingestion: {len(results)} success, {len(errors)} errors")
            
            # Réponse
            response_data = {
                'success': len(errors) == 0,
                'processed': len(results),
                'errors': len(errors),
                'results': results,
                'error_details': errors if errors else None
            }
            
            status_code = 200 if len(errors) == 0 else 207  # 207 Multi-Status
            
            return request.make_response(
                json.dumps(response_data),
                headers=[('Content-Type', 'application/json')],
                status=status_code
            )
            
        except Exception as e:
            _logger.error(f"Erreur bulk KPI API: {str(e)}")
            return request.make_response(
                json.dumps({'error': 'Internal server error'}),
                headers=[('Content-Type', 'application/json')],
                status=500
            )

    @http.route('/api/mdmc/v1/kpis/test', type='json', auth='none', methods=['GET'], csrf=False)
    def test_kpi_api(self):
        """Endpoint de test pour vérifier que l'API KPI est fonctionnelle"""
        return {
            'status': 'ok',
            'message': 'MDMC KPI API is working',
            'version': '1.0',
            'endpoints': {
                'ingest_single': '/api/mdmc/v1/kpis/ingest (POST)',
                'ingest_bulk': '/api/mdmc/v1/kpis/bulk (POST)',
                'test': '/api/mdmc/v1/kpis/test (GET)'
            },
            'auth': 'Header: X-API-KEY'
        }