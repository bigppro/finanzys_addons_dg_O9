# -*- coding: utf-8 -*-

from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class StockMove(models.Model):
    #_name = 'stock.move'
    _inherit = 'stock.move'

    quantity_available_loc_ids = fields.Many2many('stock.quant', string = "Disponibles quants", compute = '_get_available')
                                                #change_default = True, readonly = True)

    #short_name_loc_quantity = fields.Char(related = 'product_id.internal_location_ids.short_name_loc_quantity')
    choose_loc_from = fields.Many2one('stock.quant', default = quantity_available_loc_ids, change_default = True )

    short_name_loc_quantity = fields.Char(string = "Disponibilidad")#, compute = 'compute_short_loc')

    @api.onchange('product_id')
    @api.depends('product_id', 'quantity_available_loc_ids')
    @api.multi
    def _get_available(self):
        _logger.info("\n\n_get_available: running\n\n")
        location_list = []
        product_list = []
        available_locations_ids = []

        if self.product_id:
            obj_location = self.env['stock.location'].search([('usage', '=', 'internal')])
                         
            for i in obj_location:
                location_list.append(i.id)
        
            _logger.info("\n\nfor i in obj_location: running\n\n")
            _logger.info("\nlocation_list: \n")
            _logger.info(location_list)

            obj_quant = self.env['stock.quant'].search([('product_id', '=', self.product_id.id),
                                                        ('location_id', 'in', location_list)])
        
            _logger.info("\obj_quant: \n")
            _logger.info(obj_quant)

            for obj in obj_quant:
                move_line = {'product_id': obj.product_id.id,
                            'stock_location': obj.location_id.id,
                            'qty_on_hand': obj.qty,
                            }
                product_list.append(move_line)

            _logger.info("\n\nfor obj in obj_quant: running\n\n")
            _logger.info("\product_list: \n")
            _logger.info(product_list)

            for i in product_list:
                if i['qty_on_hand'] > 0:
                    available_locations_ids.append(i['stock_location'])
                    self.quantity_available_loc_ids = self.env['stock.quant'].search([('location_id', 'in', available_locations_ids)])
                    
                    #_logger.info(available_locations_ids)

            _logger.info("\n\ni in product_list: running\n\n")
            _logger.info("\n available_locations_ids: \n")
            _logger.info(available_locations_ids)

            _logger.info("\aself.quantity_available_loc_ids: \n")
            _logger.info(self.quantity_available_loc_ids)
               
class StockMove(models.Model):
    _inherit = 'stock.quant'

    location_name = fields.Char(related='location_id.name')
    quantity = fields.Float(related='quantity')
    



    """ @api.onchange('product_id')
    @api.depends('product_id','quantity_available_loc_ids')
    @api.one
    def compute_short_loc(self): 
        #logger.info("\n\ncompute_short_loc running\n\n")
        short_n = ""
        if self.quantity_available_loc_ids:
            for n in self.quantity_available_loc_ids:
                short_n += str(n.location_id.name) + ": " + str(n.quantity) + " " + str(n.product_tmpl_id.uom_id.name) + "\n"
                #((" ".join((": ".join(str(n.stock_location.name),str(n.qty_on_hand))),str(n.product_id.uom_id.name)))+"\n")
            self.short_name_loc_quantity = short_n """


   


"""  @api.depends('quantity_available_loc_ids','product_id', 'move_line')
    @api.one
    def compute_short_loc(self): 
        #locations_p_ids = self.
        for move_line in move_lines:
            move_line.qu = self.product_id """



  
"""     
    quantity_available_loc = fields.One2many('stock.mini.lines', 'product_id', compute='compute_stock_quant_ids')
    short_name_loc_quantity = fields.Char(string='Disponibilidad', compute = 'compute_short_loc')


    @api.onchange('product_id')
    @api.depends('product_id')
    @api.model
    def compute_stock_quant_ids(self):
        location_list = []
        product_list = []
        obj_location = self.env['stock.location'].search([('usage', '=', 'internal')])
        for i in obj_location:
            location_list.append(i.id)
        obj_quant = self.env['stock.quant'].search([('product_id', '=', self.product_id.id),('location_id', 'in', location_list)])
        for obj in obj_quant:
            move_line = {'product_id': obj.product_id.id,
                         'stock_location': obj.location_id.id,
                         'qty_on_hand': obj.qty,
                         'product_name': obj.product_id.name
                         }
            product_list.append(move_line)
        for i in product_list:
            if i['qty_on_hand'] > 0:
                self.quantity_available_loc |= self.env['stock.mini.lines'].create(i)

    @api.onchange('product_id')
    @api.depends('product_id','quantity_available_loc')
    @api.one
    def compute_short_loc(self):
        short_n = ""
        for n in self.quantity_available_loc:
            short_n += str(n.stock_location.name) + ": " + str(n.qty_on_hand) + " " + str(n.product_id.product_tmpl_id.uom_id.name) + "\n"
        self.short_name_loc_quantity = short_n
"""

""" class InternalLocation(models.Model):
    _name = 'stock.mini.lines'
    _rec_name = 'short_name_loc_quantity'

    stock_location = fields.Many2one('stock.location', string='Location Name')
    qty_on_hand = fields.Float('On Hand')
    forecast = fields.Float('Forecast')
    incoming_qty = fields.Float('Incoming Quantity')
    outgoing_qty = fields.Float('Outgoing Quantity')
    product_id = fields.Many2one('product.product', string='Product')
    product_name = fields.Char('Product Name')

    short_name_loc_quantity = fields.Char('Ubicacion',compute = 'compute_short_loc')

    @api.depends('product_id')
    @api.one
    def compute_short_loc(self):
        short_n = ""
        for n in self:
            short_n += str(n.stock_location.name) + ": " + str(n.qty_on_hand) + " " + str(n.product_id.product_tmpl_id.uom_id.name) + "\n"
            #((" ".join((": ".join(str(n.stock_location.name),str(n.qty_on_hand))),str(n.product_id.uom_id.name)))+"\n")
        self.short_name_loc_quantity = short_n """



""" list_price = fields.Float('Precio Unitario',related='product_id.list_price') """

""" locations_ids = fields.One2many()
locations_name = fields.One2many('stoc') """

""" @api.onchange('product_id', 'product_uom_id')
def onchange_product_id(self):
    if self.product_id:
        self.lots_visible = self.product_id.tracking != 'none'
        if not self.product_uom_id or self.product_uom_id.category_id != self.product_id.uom_id.category_id:
            if self.move_id.product_uom:
                self.product_uom_id = self.move_id.product_uom.id
            else:
                self.product_uom_id = self.product_id.uom_id.id
        res = {'domain': {'product_uom_id': [('category_id', '=', self.product_uom_id.category_id.id)]}}
    else:
        res = {'domain': {'product_uom_id': []}}
    return res """

""" class product_stock(models.Model):
    _inherit = 'stock.quant'    """ 

""" class StockMode(models.Model):
    _inherit = 'stock.move'

    image_small = fields.Binary(string='Imagen', related='product_id.product_tmpl_id.image_medium')
"""

""" @api.multi
@api.depends('product_id')
def compute_qty(self):
    for rec in self:
        if rec.product_id:
            product = self.env['product.product'].search([('id', '=', rec.product_id.id)])
            rec.qty_available = product.qty_available
            print '=======>>>>>', product

_columns = {
'list_price':  fields.float('product', related='product_id.list_price'),
'qty_available': fields.integer(string=u'Disponible', compute='compute_qty', readonly=True),
} """
