import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class ProductPackaging(models.Model):
    _inherit = "product.packaging"

    weight = fields.Float(compute='_compute_weight', string='Weight')
    total_height = fields.Float(compute='_compute_total_height', string='Total Height')
    height_factor = fields.Float('Height factor', default='1.0')
    
    @api.depends('qty', 'product_id', 'product_id.thickness', 'package_type_id', 'package_type_id.height')
    def _compute_total_height(self):
        for pp in self:
            th = pp.qty * pp.product_id.thickness * pp.height_factor
            if pp.package_type_id:
                th += pp.package_type_id.height
            pp.total_height = th            
    
    @api.depends('qty', 'package_type_id', 'package_type_id.tarra_weight')
    def _compute_weight(self):
        for pp in self:
            w = pp.qty * pp.product_id.weight
            if pp.package_type_id:
                w += pp.package_type_id.tarra_weight
            pp.weight = w

   