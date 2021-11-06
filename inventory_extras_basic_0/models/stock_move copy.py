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

    coments = fields.Text(string = "Comentarios")
    location_from_id_edit = fields.Many2one('stock.location', string = "Origen", required = True, auto_join=True)
    location_dest_id_edit = fields.Many2one('stock.location', string = "Destino", required = True, auto_join=True)

    #change by default
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
