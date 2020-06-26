# -*- coding: utf-8 -*-
from odoo import models, fields, api

class marvel_currency(models.Model):
    _name="marvel.category"

    active = fields.Boolean(
        string='Update'
    )

    category_name = fields.Many2one(
        'product.category', 'display_name',
        required=True,
    )
