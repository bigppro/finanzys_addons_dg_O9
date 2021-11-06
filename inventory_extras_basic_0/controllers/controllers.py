# -*- coding: utf-8 -*-
from openerp import http

# class InventoryExtrasBasic0(http.Controller):
#     @http.route('/inventory_extras_basic_0/inventory_extras_basic_0/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inventory_extras_basic_0/inventory_extras_basic_0/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inventory_extras_basic_0.listing', {
#             'root': '/inventory_extras_basic_0/inventory_extras_basic_0',
#             'objects': http.request.env['inventory_extras_basic_0.inventory_extras_basic_0'].search([]),
#         })

#     @http.route('/inventory_extras_basic_0/inventory_extras_basic_0/objects/<model("inventory_extras_basic_0.inventory_extras_basic_0"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inventory_extras_basic_0.object', {
#             'object': obj
#         })