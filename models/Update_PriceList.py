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
        #Se obtiene la fecha anterior
        yesterday = current_date - relativedelta(days=1)

        #Se obtiene el objeto donde se almacena el registro de cada ejecucion
        for record in self:
            #se obtiene el tipo de cambio del dia
            r_today = self.env['marvel.currency'].search([('currency_date','>=',current_date),('currency_date','<=',current_date)])
            #si ya existe un tipo de cambio de el dia Actualiza el precio de lista de los productos
            if r_today:
                #Se obtiene el Factor del dia
                for rate_t in r_today:
                    factor_today = rate_t.factor
                    #Se obtiene el tipo de cambio anterior
                    r_yesterday = self.env['marvel.currency'].search([('currency_date','=',yesterday)])
                    #Si Existe un tipo de cambio de ayer entra par aactualizar los productos
                    if r_yesterday:
                        factor_yesterday = 1.00
                        #Asigna el factor de ayer
                        for rate in r_yesterday:
                            factor_yesterday = rate.factor
                        #Se obtienen las categorias a actualizar
                        Categories_to_update = self.env['marvel.category'].search([('active','=',True)])
                        products = self.env['product.product']
                        for c in Categories_to_update:
                            print("Categories = " + str(c.category_name.display_name))

                            products += self.env['product.product'].search([('categ_id.complete_name','=',c.category_name.display_name)])
                            products+= self.env['product.product'].search([('categ_id.parent_id.complete_name','=',c.category_name.display_name)])

                        #products = self.env['product.product'].search(['|',('categ_id.complete_name','=','MARVEL / AGRICOLA / SISTEMAS DE RIEGO'),('categ_id.parent_id.complete_name','=','MARVEL / AGRICOLA / SISTEMAS DE RIEGO')])

                        #Se obtienen los productos de la categoria a actualizar


                        print("Products = " + str(products))
                        #busco si ya se realizaron ejecuciones el dia de hoy y si fueron exitosas
                        excecution = self.env['marvel.pricelist'].search([('excecution_date','>=',current_date),('excecution_date','<=',current_date),('successful','=',True)])
                        #Si existen ejecuciones anteriores el dia de hoy entra para actualizar los productos
                        if excecution:
                            #obtenemos la ultima ejecucion de hoy
                            excecution_list = [date for date in excecution.mapped('excecution_date') if date]
                            last_excecution_date = excecution_list and max(excecution_list)
                            last_excecution = self.env['marvel.pricelist'].search([('excecution_date','=',last_excecution_date)])
                            #Si el factor de la ultima ejecucion del  dia de hoy es diferente al del dia de hoy entra para actualizar los productos
                            print("last_excecution.factor = " + str(last_excecution.factor))
                            print("factor_today = " + str("{0:.8}".format(factor_today)))
                            if "{0:.8}".format(last_excecution.factor) != "{0:.8}".format(factor_today):
                                #Actualizamos el precio de lista de los productos
                                for product in products:
                                    pricelist_base=product.list_price/last_excecution.factor
                                    new_price = pricelist_base*factor_today
                                    print('old price = ' + str(product.list_price))
                                    print('base price = ' + str(pricelist_base))
                                    print('new price = ' + str(new_price))
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
                                print("Entro antes de la carita")
                                return {
                                    'effect': {
                                    'fadeout': 'slow',
                                    'message': "Yeah! The prices of the products were calculated and updated",
                                    'img_url': '/web/static/src/img/smile.svg',
                                    'type': 'rainbow_man',
                                    }}
                            else:
                                #almacenamos la ejecucion como exitosa
                                excecution_values = {
                                    'excecution_date':datetime.now(),
                                    'exchange_rate': rate_t.rate_today,
                                    'factor': factor_today,
                                    'successful': True,
                                    }
                                self.write(excecution_values)

                                raise exceptions.Warning(_('Marvel\'s exchange rate is already updated with today\'s exchange rate! \n It is not necessary to update the data again.'))
                        #Si no existen ejecuciones anteriores el dia de hoy entra para actualizar los productos ya que es la primera del dia
                        else:
                            #Actualizamos los Productos
                            for product in products:
                                pricelist_base=product.list_price/factor_yesterday
                                new_price = pricelist_base*factor_today
                                print('old price = ' + str(product.list_price))
                                print('base price = ' + str(pricelist_base))
                                print('new price = ' + str(new_price))
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
                    print("entro")
                    excecution_values = {
                        'excecution_date':datetime.now(),
                        #'exchange_rate': rate_t.rate_today,
                        #'factor': factor_today,
                        'successful': False,
                    }
                    self.write(excecution_values)

                    raise exceptions.Warning(_('Marvel\'s exchange rate doesn\'t have a Exchange rate registered for today! \n Please request the update to the corresponding department!'))
