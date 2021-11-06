# -*- coding: utf-8 -*-
{
    'name': "Inventory Extras (P0)",

    'summary': """
        Various customizations of inventory module and its 
        associates""",

    'description': """
        This module contains various customizations of both views and 
        fields, calculated or simple for the inventory module and its 
        associates: (products, product templates, movements / transfers 
        ... etc.)
    """,

    'author': "Finanzas y Contabilidad AA / Pedro MBE",
    'website': "http://www.finanzasycontabilidadaa.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'product',
    'account', 'mail',],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #'views/views.xml',
        #'views/templates.xml',
        'reports/conduce_external_layout.xml',
        'reports/stock_picking.xml',
        'views/stock_move_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    'installable': True,
}