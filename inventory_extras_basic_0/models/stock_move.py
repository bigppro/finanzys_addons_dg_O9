# -*- coding: utf-8 -*-

from openerp import models, fields, api
#import random
from openerp.tools.translate import _ 
from openerp.exceptions import ValidationError
from random import randint
import logging
_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    #_name = 'stock.move'
    _inherit = 'stock.move'

    coments2 = fields.Text(string = "Comentarios")
    image_small = fields.Binary('Product Image', related='product_id.image_small')
    location_from_id_edit = fields.Many2one('stock.location', string = "Origen", required = True, 
        auto_join = True, help = "Especifique la ubicacion de origen a utilizar.")
    location_dest_id_edit = fields.Many2one('stock.location', string = "Destino", required = True, 
        auto_join = True, help = "Especifique la ubicacion de destino a utilizar.")

    location_from_id_edit_name = fields.Char(related = 'location_from_id_edit.name', string = "Origen",
                                            stored = True) 
    location_dest_id_edit_name = fields.Char(related = 'location_dest_id_edit.name', string = "Destino",
                                            stored = True) 


    # giving init values by default
    @api.onchange('location_id')
    @api.one
    def change_location_id_1(self):            
        if self.location_id:
            self.location_from_id_edit = self.location_id
        
    @api.onchange('location_dest_id')
    @api.one
    def change_locations_dest_1(self):
        if self.location_dest_id:
            self.location_dest_id_edit = self.location_dest_id


    # changing default master values
    @api.onchange('location_from_id_edit')
    @api.one
    def change_location_from(self):            
        if self.location_from_id_edit:
            self.location_id = self.location_from_id_edit
        
    @api.onchange('location_dest_id_edit')
    @api.one
    def change_locations_dest(self):
        if self.location_dest_id_edit:
            self.location_dest_id = self.location_dest_id_edit
