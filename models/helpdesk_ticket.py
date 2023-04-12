import logging
from odoo import api, fields, models
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)
                        
class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'
    
    active = fields.Boolean(default=True)
    
    @api.model
    def create(self, vals):
        partner_id = vals.get('partner_id')
        if partner_id:
            has_tickets = self.env['res.partner'].search([('id', '=', partner_id)]).has_available_tickets
            if not has_tickets:
                self.active = False
                vals['stage_id'] = 3 # En espera
            else:
                self.active = True
                vals['stage_id'] = 1 # Nuevo
                partner = self.env['res.partner'].search([('id', '=', partner_id)])
                partner.active_tickets -= 1
                
              
        return super(HelpdeskTicket, self).create(vals)
    
    def write(self, vals):
        ticket = self.env['helpdesk.ticket'].search([('id', '=', self.id)])
        partner = self.env['res.partner'].search([('id', '=', ticket.partner_id.id)])
        
        if not partner.has_available_tickets and self.stage_id.id == 3:
            vals['stage_id'] = 3 # En espera
            raise UserError('El usuario no tiene tickets disponibles')
        
        elif partner.has_available_tickets and self.stage_id.id == 3:
            partner.active_tickets -= 1
        
        return super().write(vals)

