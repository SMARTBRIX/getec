# -*- coding: utf-8 -*-

from odoo import models, fields


class BusinessPlanExpenditure(models.Model):
    _name = 'businessplan.expenditure'
    _description = "Business Plan Expenditure"

    name = fields.Char()
    property_id = fields.Many2one('property.property', string="Property")
    cost_type_id = fields.Many2one('property.cost.type', string="Cost Type")
    vendor_id = fields.Many2one('res.partner', string="Vendor")
    date_start = fields.Date("Period Begin")
    date_end = fields.Date("Period End")
    amount = fields.Float()
    documents = fields.Many2many('ir.attachment')
    cleared = fields.Boolean(readonly=True)
    expenditure_factor_ids = fields.One2many(
        'property.expenditure.factor', 'expenditure_id', string="Property Factor")
    bill_id = fields.Many2one('account.move', string="Vendor Bill")
    allocation_formula = fields.Selection([('ls', 'Living Space (sqm)'), ('p', 'Persons'), (
        'ru', 'Number of Residential Units'), ('da', 'Direct Assignment'), ('co', 'Co-Ownership')], string="Allocation Formula", related="cost_type_id.allocation_formula")
    tax_id = fields.Many2one('account.tax', 'Tax')
