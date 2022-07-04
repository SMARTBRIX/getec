# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_rent = fields.Boolean("Rent?")
    is_ancillary_costs = fields.Boolean("Ancillary Costs?")
    is_heating_costs = fields.Boolean("Heating Costs?")
