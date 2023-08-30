# -*- coding: utf-8 -*-
{
    'name': "jt_repeat_products",

    'summary': "Repeat product reports",

    'description': "",

    'author': "jaco tech",
    'website': "https://jaco.tech",
    "license": "AGPL-3",


    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.8',

    # any module necessary for this one to work correctly
    'depends': ['base','product','stock','jt_product_repeat'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # "security/product_template_rule.xml",
        # "security/product_template_tag.xml",        
        'views/product_attribute_views.xml',
        'views/stock_package_type_view.xml',
        "views/product_template.xml",
        "views/product_product.xml",        
        "views/product_tag_views.xml",
        'report/repeat_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
