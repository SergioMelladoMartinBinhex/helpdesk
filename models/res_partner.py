import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    has_available_tickets = fields.Boolean(compute='_compute_has_available_tickets')

    @api.depends('helpdesk_ticket_ids')
    def _compute_has_available_tickets(self):
        for record in self:
            for ticket in record.helpdesk_ticket_ids:
                if ticket.active:
                    self.has_available_tickets = True
                    break
                else:
                    continue
            self.has_available_tickets = False