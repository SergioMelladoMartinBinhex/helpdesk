import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)
                        
class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'
    
    active = fields.Boolean(default=True)
    
    @api.model
    def create(self, vals):
        partner_id = vals.get('partner_id')
        if partner_id:
            has_tickets = self.env['res.partner'].browse(partner_id).has_available_tickets
            if not has_tickets:
                self.active = False
                vals['stage_id'] = 3 # En espera
            else:
                self.active = True
                vals['stage_id'] = 1 # Nuevo
                
        return super(HelpdeskTicket, self).create(vals)
    
    def write(self, vals):
        if self.active:
            vals['stage_id'] = 3
            
        return super().write(vals)
    
    
