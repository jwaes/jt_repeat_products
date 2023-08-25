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
    'version': '0.3',

    # any module necessary for this one to work correctly
    'depends': ['base','product','stock','jt_product_repeat'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/product_attribute_views.xml',
        'views/stock_package_type_view.xml',
        'report/repeat_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
