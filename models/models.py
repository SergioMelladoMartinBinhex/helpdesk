import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    ticket_ratio = fields.Float(compute='_compute_ticket_ratio')
    has_available_tickets = fields.Boolean(compute='_compute_has_available_tickets')

    @api.depends('helpdesk_ticket_count')
    def _compute_ticket_ratio(self):
        for record in self:
            if record.helpdesk_ticket_count:
                record.ticket_ratio = (100 - (record.helpdesk_ticket_active_count / record.helpdesk_ticket_count) * 100)
            else:
                record.ticket_ratio = 0

    @api.model
    def _compute_has_available_tickets(self):
        for record in self:
            record.has_available_tickets = bool(record.helpdesk_ticket_active_count)
                        
class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'
    
    @api.model
    def create(self, vals):
        partner_id = vals.get('partner_id')
        if partner_id:
            has_tickets = self.env['res.partner'].browse(partner_id).has_available_tickets
            if not has_tickets:
                vals['stage_id'] = 3
                logging.info('DEBBUG : %s', vals)
        return super(HelpdeskTicket, self).create(vals)