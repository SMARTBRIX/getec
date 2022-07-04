# -*- coding: utf-8 -*-

from odoo import models, fields


class PropertyCostCategory(models.Model):
    _name = 'property.cost.category'
    _description = "Cost Category"

    name = fields.Char(required=True)
    is_splittable = fields.Boolean("Splittable?")
    is_advance_payment = fields.Boolean("Advance Payment?")


class PropertyCostType(models.Model):
    _name = 'property.cost.type'
    _description = "Cost Type"

    name = fields.Text()
    allocation_formula = fields.Selection([('ls', 'Living Space (sqm)'), ('p', 'Persons'), (
        'ru', 'Number of Residential Units'), ('da', 'Direct Assignment')], string="Allocation Formula")
    product_id = fields.Many2one('product.product', string='Product', help='Invoice product for this cost type')
    property_cost_category_id = fields.Many2one('property.cost.category', string='Cost Category')
