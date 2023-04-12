import logging
from odoo import api, fields, models

logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    active_tickets = fields.Integer()
    has_available_tickets = fields.Boolean(compute='_compute_has_available_tickets')
    
    def _compute_has_available_tickets(self):
        for record in self:
            if self.active_tickets > 0:
                self.has_available_tickets = True
            else:
                self.has_available_tickets = False