from odoo import api, fields, models
from odoo.osv import expression

class ProductProduct(models.Model):
    _inherit = "product.product"

    additional_product_tag_ids = fields.Many2many('product.tag', 'product_tag_product_product_rel', string='Variant Tags')
    all_product_tag_ids = fields.Many2many('product.tag', compute='_compute_all_product_tag_ids', search='_search_all_product_tag_ids', string="All Tags")


    @api.depends('product_tag_ids', 'additional_product_tag_ids')
    def _compute_all_product_tag_ids(self):
        for product in self:
            product.all_product_tag_ids = product.product_tag_ids | product.additional_product_tag_ids

    def _search_all_product_tag_ids(self, operator, operand):
        if operator in expression.NEGATIVE_TERM_OPERATORS:
            return [('product_tag_ids', operator, operand), ('additional_product_tag_ids', operator, operand)]
        return ['|', ('product_tag_ids', operator, operand), ('additional_product_tag_ids', operator, operand)]
