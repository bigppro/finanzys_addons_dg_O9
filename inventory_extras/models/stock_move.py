# -*- coding: utf-8 -*-

from openerp import models, fields, api
#import random
from openerp.tools.translate import _ 
from openerp.exceptions import ValidationError
from random import randint
import logging
_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    default_qtity_show = fields.Char(string = "Cantidad de Ubicaciones", default = "3", readonly = False,
        help="""Digita una cantidad a partir de 1 para elegir cuantas ubicaciones desea proyectar en el formulario. 
            \n""""Tener en cuenta que mientras mas ubicaciones elije, espacio ocupara en el formulario!""")

    @api.onchange('default_qtity_show')
    @api.constrains('default_qtity_show')
    def _check_number(self):
        for rec in self:
            if rec.default_qtity_show:
                is_digits_only =  self.default_qtity_show.isdigit() # rec.match(r'^[0-9]+$', rec.default_qtity_show)
                _logger.info("\n is_digits_only \n")
                _logger.info(is_digits_only)
                if is_digits_only:
                    pass
                else:
                    raise ValidationError(_("Valor errado (%s). Debe introducir un numero entero positivo. (ej.: 3)"%rec.default_qtity_show))


class StockMove(models.Model):
    #_name = 'stock.move'
    _inherit = 'stock.move'

    quantity_available_loc_ids = fields.Many2many('stock.quant', string = "Disponibilidad", compute = '_get_available',
                                                help="Almacenes que tienen disponible este producto.")
    quantity_available_loc_ids2 = fields.Many2many('stock.quant', string = "Disponibles quants", compute = '_get_available',
                                                help="Almacenes que tienen disponible este producto.")
    limit_to_show = fields.Char(related = 'picking_id.default_qtity_show')
   
    def _get_default_color(self):
        return randint(1, 11)


    @api.onchange('product_id')
    @api.depends('product_id')
    @api.one
    def _get_disponibilidad(self):
        """ for rec in self:
            if rec.qty_available > 0: """
        if self.product_id.qty_available > 0:
            self.disponibilidad_quant = True


    @api.onchange('product_id')
    @api.depends('product_id','quantity_available_loc_ids2', 'choose_loc_from2', 'product_uom_qty', 'location_id')
    @api.one
    def _calculate_choose_loc_from(self):
        if self.quantity_available_loc_ids2:
            #ubicaciones disponibles globales
            loc_ids = []
            loc_to_calculate = []

            for q_ids in self.quantity_available_loc_ids2:
                loc_ids.append(q_ids.location_id.id)

            """ _logger.info("\nfor index, q_ids")
            _logger.info("\nloc_ids\n")
            _logger.info(loc_ids) """

            loc_all = self.env['stock.quant'].search([('location_id', 'in', loc_ids)], order='qty desc')
                                                               
            _logger.info("\nloc_all\n")
            _logger.info(loc_all)

            """ have_child = True
            all_childs = []
            picking = self.env['stock.picking'].search([('')])
            this_wh = self.location_id
            n = 0
            while have_child = True: """
                

            #loc_first_ids = self.env['stock.location'].search([('id', 'in', )])

            # ubicaciones cercanas (para calcular primero) (tomando el almacen elegido en la transferencia: "Source Location Zone")
            loc_to_calculate_first = self.env['stock.quant'].search([('location_id', '=', self.location_id.id),
                                                                     ('product_id', '=', self.product_id.id),
                                                                     ('qty', '>', 0)], order='qty desc')

            _logger.info("\nloc_to_calculate_first\n")
            _logger.info(loc_to_calculate_first)

            ordened_loc = []
            orden_first = []
            orden_second = []

            if len(loc_to_calculate_first) > 0:
                for index, loc_orden in enumerate(loc_all):
                    if loc_orden[index] in loc_to_calculate_first:
                        orden_first.append(loc_orden[index])
                    else:
                        orden_second.append(loc_orden[index])
                ordened_loc = [orden_first, orden_second]
            else:
                ordened_loc = loc_all

            loc_to_calculate = ordened_loc

            _logger.info("\nloc_to_calculate\n")
            _logger.info(loc_to_calculate)

            record_to_update_loc_ids = []
            for index,record_to_update in enumerate(loc_to_calculate):
                record_to_update.temp_numerate = index
                record_to_update_loc_ids.append(record_to_update.location_id.id)

            loc_to_calculate = self.env['stock.quant'].search([('location_id', 'in', record_to_update_loc_ids)], order='qty desc') #.sort(key=lambda x: x.temp_numerate, reverse=True) 

            _logger.info("\nloc_to_calculate after enumerate\n")
            _logger.info(loc_to_calculate)

            ################# prueba ####################
            for prueba in loc_all:
                _logger.info("\nloc_all temp_enumerate\n")
                _logger.info(prueba.temp_numerate)                     

            loc_qty_sum_ok = []
            x = 0
            q = 0

            _logger.info("\nself.product_uom_qty\n")
            _logger.info(self.product_uom_qty)

            while self.product_uom_qty > q:
                if x >= len(loc_to_calculate):
                    break
                else:
                    loc_qty_sum_ok.append(loc_to_calculate[x].location_id.id)
                    q+=loc_to_calculate[x].qty
                x+=1

                _logger.info("\nx+=1\n")
                _logger.info(x)

                _logger.info("\nq+=1\n")
                _logger.info(q)

            _logger.info("\nloc_qty_sum_ok\n")
            _logger.info(loc_qty_sum_ok)

            to_pass = self.env['stock.quant'].search([('location_id', 'in',loc_qty_sum_ok)],order='qty desc')

            _logger.info("\nto_pass\n")
            _logger.info(to_pass)

            self.choose_loc_from2 = self.env['stock.quant'].search([('location_id', 'in',loc_qty_sum_ok)],order='qty desc')

            #TODO choose_loc_from se debe elegir por defecto la ubicacion [0] luego de organizarla de menor a mayor segun cercania de almacen


    def _inverse_calculate_choose_loc_from(self):
        pass

    coments = fields.Text(string = "Comentarios")

    color = fields.Integer(string='Color Index', default=_get_default_color)
    disponibilidad_quant = fields.Boolean('Disponibilidad Boolean', compute = "_get_disponibilidad", default = False)#, default = False)
    """ choose_loc_from = fields.Many2many(related = 'quantity_available_loc_ids2', readonly = True
                                                help="Elija el o los almacenes desde donde desea sea retirada la mercancia.") """ #'stock.quant', readonly = False, domain= [('id', 'in', quantity_available_loc_ids)], default = default_choose_loc_from, change_default=True)
    choose_loc_from2 = fields.Many2many('stock.quant', compute = '_calculate_choose_loc_from', inverse='_inverse_calculate_choose_loc_from',
                        required = True, store = True, string = "Ubicaciones Salida",
                        help="""* Esta campo elije la o las ubicaciones de salida mas cercana(s) desde donde se estar??a realizando el conduce.
                              \n* Para que esta funci??n autom??tica pueda funcionar; debe asignar las asociaciones de las ubicaciones/almacenes 
                              donde se especifica las ubicaciones mas pr??ximos entre ellas. Ej: Contenedor 15; cercanos: (13,14,16,17) ya que 
                              no necesariamente el numero que le sigue puede estar justo al lado por esto se deben hacer las asociaciones manuales. 
                              \n* Puede elegir quitar o agregar ubicaciones.
                              \n* Por el momento el campo estar?? eligiendo la ubicaci??n con el mayor numero de itemes y en caso de no ser suficiente agrega 
                              otras ubicaciones. 
                             """,)#,  default = _calculate_choose_loc_from ,

    #short_name_loc_quantity = fields.Char(string = "Disponibilidad")#, compute = 'compute_short_loc')


    @api.onchange('product_id')
    @api.depends('product_id', 'quantity_available_loc_ids', 'limit_to_show')
    @api.one
    def _get_available(self):
        _logger.info("\n\n_get_available: running\n\n")
        location_list = []
        product_list = []
        available_locations_ids = []

        if self.product_id:
            obj_location = self.env['stock.location'].search([('usage', '=', 'internal')])
                         
            for i in obj_location:
                location_list.append(i.id)

            obj_quant = self.env['stock.quant'].search([('product_id', '=', self.product_id.id),
                                                        ('location_id', 'in', location_list)])
            for obj in obj_quant:
                move_line = {'product_id': obj.product_id.id,
                            'stock_location': obj.location_id.id,
                            'qty_on_hand': obj.qty,
                            }
                product_list.append(move_line)

            for i in product_list:
                if i['qty_on_hand'] > 0:
                    available_locations_ids.append(i['stock_location'])

            self.quantity_available_loc_ids = self.env['stock.quant'].search([('location_id', 'in', available_locations_ids)],order='temp_numerate desc', limit=int(self.limit_to_show))#,order='qty')
            self.quantity_available_loc_ids2 = self.env['stock.quant'].search([('location_id', 'in', available_locations_ids)],order='temp_numerate desc')#,order='qty')
                

    #TODO talvez deba independizar el short_name_loc_quantitys para que no afecte otros registros en _rec_name del stock.quant
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
               
class StockQuant(models.Model):
    _inherit = 'stock.quant'
    _rec_name = 'short_names_locs_quantitys'

    location_name = fields.Char(related='location_id.name')
    short_names_locs_quantitys = fields.Char(string = "Disponibilidad", compute = "compute_short_loc")
    temp_numerate = fields.Integer('para ordenar temporalmente')

    @api.depends('location_id')
    @api.one
    def compute_short_loc(self): 
        short_n = ""
        if self.location_id:
            for n in self:
                short_n += str(n.location_id.name) + ": " + str(n.qty) + " " + str(n.product_uom_id.name) + "\n\r"
            self.short_names_locs_quantitys = short_n


class StockLocation(models.Model):
    _inherit = 'stock.location'

    nearby_locs = fields.One2many('stock.location', 'location_id', string = "Ubicaciones cercanas", 
                                 help = """ Especificar una o varias ubicaciones que esten ubicadas proximo a este almacen o ubicacion
                                 para que el sistema pueda utilizarlo a la hora de determinar la ruta mas cercana de despacho.""")

    def _get_default_color(self):
        return randint(0, 11)

    color = fields.Integer(string='Color Index', default=_get_default_color)

