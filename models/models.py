from odoo import api, fields, models

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