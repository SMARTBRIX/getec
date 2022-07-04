# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PropertyExpenditure(models.Model):
    _name = 'property.expenditure'
    _description = "Expenditure"

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
        'ru', 'Number of Residential Units'), ('da', 'Direct Assignment')], string="Allocation Formula", related="cost_type_id.allocation_formula")
    tax_id = fields.Many2one('account.tax', 'Tax')

    @api.model
    def create(self, vals):
        res = super(PropertyExpenditure, self).create(vals)
        wizard_id = self.env['expenditure.split.cost']
        wizard_id.with_context({'active_ids': [res.id]}).split_cost()
        return res

    @api.onchange('property_id')
    def onchange_property_id(self):
        list_property = []
        for rec in self.property_id.child_property_ids:
            list_property.append((0, 0, {'property_id': rec.id}))

        self.expenditure_factor_ids = [(5, 0)] + list_property


class PropertyExpenditureFactor(models.Model):
    _name = 'property.expenditure.factor'
    _description = "Expenditure Factor"

    property_id = fields.Many2one('property.property', string="Property")
    factor = fields.Float()
    expenditure_id = fields.Many2one('property.expenditure')
    child_property_ids = fields.Many2many(
        'property.property', compute="compute_child_property")

    @api.depends('property_id')
    def compute_child_property(self):
        for rec in self:
            rec.child_property_ids = rec.expenditure_id.property_id.child_property_ids.ids
