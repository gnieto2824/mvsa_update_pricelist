# -*- coding: utf-8 -*-
from odoo import models, fields, api

class marvel_currency(models.Model):
    _name="marvel.currency"

    currency_date= fields.Date(
        string='Date',
        required=True,
    )

    rate_base = fields.Float(
        string='Rate Base',
        default=19.07,
        required=True,
        digits=(2,4),
    )

    rate_today=fields.Float(
        string='Rate Today',
        required=True,
        digits=(2,4),
    )

    factor=fields.Float(
        string='Factor',
        readonly=True,
        digits=(2,6),
        compute='_calculate_Factor',
    )

    @api.one
    def _calculate_Factor(self):
        for record in self:
            value = 1+(-1*((record.rate_base-record.rate_today)/record.rate_base))
            record.factor= value
