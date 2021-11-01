# -*- coding: utf-8 -*-
from openerp import http

# class InventoryExtras(http.Controller):
#     @http.route('/inventory_extras/inventory_extras/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inventory_extras/inventory_extras/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inventory_extras.listing', {
#             'root': '/inventory_extras/inventory_extras',
#             'objects': http.request.env['inventory_extras.inventory_extras'].search([]),
#         })

#     @http.route('/inventory_extras/inventory_extras/objects/<model("inventory_extras.inventory_extras"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inventory_extras.object', {
#             'object': obj
#         })