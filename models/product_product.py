import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)

class Product(models.model):
    _inherit = 'product.product'
    
    is_a_ticket = fields.Boolean(default=False)