# -*- coding: utf-8 -*-

from odoo import models, fields


class BusinessPlanJournal(models.Model):
    _name = 'businessplan.journal'
    _description = "Business Plan Journal"

    expenditure_id = fields.Many2one('businessplan.expenditure', string="Expenditure")
    tenancy_id = fields.Many2one('property.tenancy', string="Tenancy")
    cost_type_id = fields.Many2one('property.cost.type', string="Cost Type")
    amount = fields.Float()
    date_start = fields.Date("Period Begin")
    date_end = fields.Date("Period End")
    cleared = fields.Boolean(readonly=True)
    documents = fields.Many2many('ir.attachment')
    reference = fields.Char('Reference')
    tax_id = fields.Many2one('account.tax', 'Tax')
