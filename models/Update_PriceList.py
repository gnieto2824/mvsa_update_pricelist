# -*- coding: utf-8 -*-
from odoo import models, fields, api, _, exceptions
from dateutil.relativedelta import relativedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta



class Update_PriceList(models.TransientModel):
    #_inherit = "product.template"
    _name="marvel.pricelist"

    excecution_date= fields.Datetime(
        string='Excecution Date',
    )


    exchange_rate= fields.Float(
        string='Exchange Rate'
    )

    factor= fields.Float(
        string='factor'
    )
    successful = fields.Boolean(
        string='Succesfull Update?'
    )

    @api.multi
    #@api.depends('list_price')
    #Funcion que actualiza el precio de lista de la Categoria Sistema de Riego
    def compute_pricelist(self):
        # Se obtiene la fecha actual
        current_date = datetime.now().date()
        #current_date = current_date + relativedelta(days=3)

        #Se obtiene el objeto donde se almacena el registro de cada ejecucion
        for record in self:

            #se obtiene el tipo de cambio del dia
            r_today = self.env['marvel.currency'].search([('currency_date','>=',current_date),('currency_date','<=',current_date)])
            #si ya existe un tipo de cambio de el dia Actualiza el precio de lista de los productos
            if r_today:

                factor_today = 1
                for rate_t in r_today:
                    factor_today = rate_t.factor
                #se obtienen las categorias a actualizar
                Categories_to_update = self.env['marvel.category'].search([('active','=',True)])
                if not Categories_to_update:
                    raise exceptions.Warning(_('There isn\'t Categories to update on Marvel\'s Pricelist! \n Please add some Categories to update it\'s Prices!'))
                #se obtienen los productos correspondientes a las categorias
                products = self.env['product.product']

                for c in Categories_to_update:
                    #print("Categories = " + str(c.category_name.display_name))
                    products += self.env['product.product'].search([('categ_id.complete_name','=',c.category_name.display_name)])
                    products+= self.env['product.product'].search([('categ_id.parent_id.complete_name','=',c.category_name.display_name)])
                #print('Products inicial = '+ str(products))
                #Revisamos si existen ejecuciones anteriores exitosas
                excecution = self.env['marvel.pricelist'].search([('successful','=',True)])

                #si hay ejecuciones exitosas anteriores ya existe un tipo de cambio anterior
                if excecution:
                    #busca si ya tiene ejecuciones el dia de hoy
                    excecution_today = excecution.search([('excecution_date','>=',current_date),('excecution_date','<=',current_date)])
                    if excecution_today:

                        excecution_list = [date for date in excecution_today.mapped('excecution_date') if date]
                        last_excecution_date = excecution_list and max(excecution_list)
                        last_excecution = self.env['marvel.pricelist'].search([('excecution_date','=',last_excecution_date)])

                        if "{0:.8}".format(last_excecution.factor) != "{0:.8}".format(factor_today):

                            #Actualizamos el precio de lista de los productos
                            for product in products:
                                pricelist_base=product.list_price/last_excecution.factor
                                new_price = pricelist_base*factor_today
                                #print('old price = ' + str(product.list_price))
                                #print('base price = ' + str(pricelist_base))
                                #print('new price = ' + str(new_price))
                                prod_value = {'list_price': new_price}
                                product.write(prod_value)
                            #almacenamos la ejecucion como exitosa
                            excecution_values = {
                                'excecution_date':datetime.now(),
                                'exchange_rate': rate_t.rate_today,
                                'factor': factor_today,
                                'successful': True,
                                }
                            self.write(excecution_values)

                            return {
                                'effect': {
                                'fadeout': 'slow',
                                'message': "Yeah! The prices of the products were calculated and updated",
                                'img_url': '/web/static/src/img/smile.svg',
                                'type': 'rainbow_man',
                                }}
                        else:
                            #print('no actualiza nada por que el tipo de cambio es el mismo')
                            #almacenamos la ejecucion como exitosa
                            excecution_values = {
                                'excecution_date':datetime.now(),
                                'exchange_rate': rate_t.rate_today,
                                'factor': factor_today,
                                'successful': True,
                                }
                            self.write(excecution_values)

                            raise exceptions.Warning(_('Marvel\'s exchange rate is already updated with today\'s exchange rate! \n It is not necessary to update the data again.'))
                    else:
                        #print('entro a guardar la nueva ejecucion del dia de hoy')
                        #se obtiene la ultima ejecucion exitosa
                        excecution_list = [date for date in excecution.mapped('excecution_date') if date]
                        last_excecution_date = excecution_list and max(excecution_list)
                        last_excecution = self.env['marvel.pricelist'].search([('excecution_date','=',last_excecution_date)])

                        #Actualizamos los Productos
                        for product in products:
                            pricelist_base=product.list_price/last_excecution.factor
                            new_price = pricelist_base*factor_today
                            #print('old price = ' + str(product.list_price))
                            #print('base price = ' + str(pricelist_base))
                            #print('new price = ' + str(new_price))
                            prod_value = {'list_price': new_price}
                            product.write(prod_value)

                        #almacenamos la ejecucion como exitosa
                        excecution_values = {
                            'excecution_date':datetime.now(),
                            'exchange_rate': rate_t.rate_today,
                            'factor': factor_today,
                            'successful': True,
                            }
                        self.write(excecution_values)
                        return {
                            'effect': {
                            'fadeout': 'slow',
                            'message': "Yeah! The prices of the products were calculated and updated",
                            'img_url': '/web/static/src/img/smile.svg',
                            'type': 'rainbow_man',
                            }}

                #no existe una ejecucion exitosa por lo tanto es la primera vez que se ejecuta
                else:
                    #print('entro a la ejecucion por primera vez')
                    #Actualizamos los Productos
                    #print('factor today = ' + str(factor_today))
                    #print('products = ' + str(products))
                    for product in products:
                        pricelist_base=product.list_price
                        new_price = pricelist_base*factor_today
                        #print('old price = ' + str(product.list_price))
                        #print('base price = ' + str(pricelist_base))
                        #print('new price = ' + str(new_price))
                        prod_value = {'list_price': new_price}
                        product.write(prod_value)

                    #almacenamos la ejecucion como exitosa
                    excecution_values = {
                        'excecution_date':datetime.now(),
                        'exchange_rate': rate_t.rate_today,
                        'factor': factor_today,
                        'successful': True,
                        }
                    self.write(excecution_values)
                    return {
                        'effect': {
                        'fadeout': 'slow',
                        'message': "Yeah! The prices of the products were calculated and updated",
                        'img_url': '/web/static/src/img/smile.svg',
                        'type': 'rainbow_man',
                        }}
            # Si no existe tipo de cambio se almacena la ejecucion en Falso
            else:
                excecution_values = {
                    'excecution_date':datetime.now(),
                    #'exchange_rate': rate_t.rate_today,
                    #'factor': factor_today,
                    'successful': False,
                }
                raise exceptions.Warning(_('Marvel\'s exchange rate doesn\'t have a Exchange rate registered for today! \n Please request the update to the corresponding department!'))
                self.write(excecution_values)
