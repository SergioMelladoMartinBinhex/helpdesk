import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    ticket_ratio = fields.Float(compute='_compute_ticket_ratio')

    @api.depends('helpdesk_ticket_count')
    def _compute_ticket_ratio(self):
        for record in self:
            if record.helpdesk_ticket_count:
                self.ticket_ratio = (100 - (record.helpdesk_ticket_active_count / record.helpdesk_ticket_count) * 100)
            else:
                self.ticket_ratio = 0
    
    has_available_tickets = fields.Boolean(compute='_compute_has_available_tickets')
    
    @api.model
    def _compute_has_available_tickets(self):        
        for record in self:   
            if record.helpdesk_ticket_count == 0:
                record.has_available_tickets = False
            else:
                record.has_available_tickets = True
                        
class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'
    
    @api.model
    def create(self, vals):
        partner_id = vals.get('partner_id')
        has_tickets = self.env['res.partner'].browse(partner_id).has_available_tickets
        if not has_tickets:
            logging.info("DEBBUG - ENTRE POR EL IF")
            vals['stage_id'] = 3
            logging.info("DEBBUG - VALS: %s", vals["stage_id"])
            return super(HelpdeskTicket, self).create(vals)
        else:
            logging.info("DEBBUG - ENTRE POR EL ELSE")
            logging.info("DEBBUG - VALS: %s", vals["stage_id"])
            return super(HelpdeskTicket, self).create(vals)