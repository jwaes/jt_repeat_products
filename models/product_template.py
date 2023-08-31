import logging
from odoo import api, fields, models
from odoo.osv import expression

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_tag_ids = fields.Many2many('product.tag', 'product_tag_product_template_rel', string='Template Tags')

    product_variant_tag_ids = fields.Many2many('product.tag', compute='_compute_product_variant_tag_ids', string='Variant Tags')

    all_product_tag_ids = fields.Many2many('product.tag', compute='_compute_all_product_tag_ids', search='_search_all_product_tag_ids',  string='All Variant Tags')

    is_public_visible = fields.Boolean(compute='_compute_is_public_visible', string='Is Publicly Visible')

    description_report = fields.Text(
            'Report Description', translate=True,
            help="A description of the Product that you want to communicate to your customers in Repeat report "
                "This description will be shown in the Repeat reports")    

    @api.depends('product_variant_ids', 'product_variant_ids.public_visible')
    def _compute_is_public_visible(self):
        for tmpl in self:
            tmpl.is_public_visible = False
            for prod in tmpl.product_variant_ids:
                if prod.public_visible:
                    tmpl.is_public_visible = True
    
    @api.depends('product_tag_ids', 'product_variant_tag_ids')
    def _compute_all_product_tag_ids(self):
        for tmpl in self:
            tmpl.all_product_tag_ids = tmpl.product_tag_ids | tmpl.product_variant_tag_ids

    @api.depends('product_variant_ids', 'product_variant_ids.additional_product_tag_ids')
    def _compute_product_variant_tag_ids(self):
        for tmpl in self:
            for prod in tmpl.product_variant_ids:
                tmpl.product_variant_tag_ids |= prod.additional_product_tag_ids

    def _search_all_product_tag_ids(self, operator, operand):
        if operator in expression.NEGATIVE_TERM_OPERATORS:
            return [('product_tag_ids', operator, operand), ('product_variant_ids.additional_product_tag_ids', operator, operand)]
        return ['|', ('product_tag_ids', operator, operand), ('product_variant_ids.additional_product_tag_ids', operator, operand)]


