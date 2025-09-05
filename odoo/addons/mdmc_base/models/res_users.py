from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def _get_default_timezone(self):
        return 'Europe/Lisbon'

    def __init__(self, pool, cr):
        super().__init__(pool, cr)
        # Set default timezone for all users
        self._defaults['tz'] = 'Europe/Lisbon'