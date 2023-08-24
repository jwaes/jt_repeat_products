import logging
from odoo import fields, models, api

_logger = logging.getLogger(__name__)


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    color_type = fields.Selection([
        ('default', 'Default'),
        ('pattern', 'Image pattern'),
        ('css', 'Css'),], default='default', required=True, help="Color type") 
    
    css_style = fields.Char(string='Css style')

    pattern_image = fields.Image('Pattern Image', max_width=1024, max_height=1024)




class ProductTemplateAttributeValue(models.Model):
    _inherit = "product.template.attribute.value"

    color_type = fields.Selection(related="product_attribute_value_id.color_type", readonly=True)
    css_style = fields.Char(related="product_attribute_value_id.css_style")
    pattern_image = fields.Image(related="product_attribute_value_id.pattern_image")

    is_pattern = fields.Boolean(compute='_compute_is_pattern', string='is_pattern')
    is_css = fields.Char(compute='_compute_is_css', string='is_css')
    
    @api.depends('color_type')
    def _compute_is_css(self):
        for record in self:
            record.is_css = record.color_type == 'css'
    
    @api.depends('color_type')
    def _compute_is_pattern(self):
        for record in self:
            record.is_pattern = record.color_type == 'pattern'