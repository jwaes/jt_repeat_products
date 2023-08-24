# -*- coding: utf-8 -*-
# from odoo import http


# class JtRepeatProducts(http.Controller):
#     @http.route('/jt_repeat_products/jt_repeat_products', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/jt_repeat_products/jt_repeat_products/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('jt_repeat_products.listing', {
#             'root': '/jt_repeat_products/jt_repeat_products',
#             'objects': http.request.env['jt_repeat_products.jt_repeat_products'].search([]),
#         })

#     @http.route('/jt_repeat_products/jt_repeat_products/objects/<model("jt_repeat_products.jt_repeat_products"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('jt_repeat_products.object', {
#             'object': obj
#         })
