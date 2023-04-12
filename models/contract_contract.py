from odoo import api, fields, models
import logging

logger = logging.getLogger(__name__)

class ContractContract(models.Model):
    _inherit = 'contract.contract'

    @api.model
    def create(self, vals):
        tickets = 0
        for line in vals['contract_line_fixed_ids']:
            if line[2]['name'] == "Ticket":
                tickets = line[2]['quantity']

        partner = self.env['res.partner'].search([('id', '=', vals.get('partner_id'))])
        partner.active_tickets = tickets 

        return super().create(vals)

