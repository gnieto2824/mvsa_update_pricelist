# -*- coding: utf-8 -*-
{
    'name': 'mvsa_Update_PriceList',
    'author': 'Marvelsa',
    'website': 'http://www.marvelsa.com',
    'category': 'Uncategorized',
    'version': '1.0.0',
    'depends': [
        'product','stock', 'account'
    ],
    'data': [
        #Security
        'security/ir.model.access.csv',

        #Views
        'views/Update_PriceList.xml',
        'views/marvel_currency.xml',
        'views/marvel_category.xml'

    ],
}
