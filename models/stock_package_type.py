import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class PackageType(models.Model):
    _inherit = 'stock.package.type'

    tarra_weight = fields.Float('Tarra weight', help='The total weight of the packaging itself')
    description = fields.Char('Description')