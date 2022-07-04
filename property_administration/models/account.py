# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    property_ids = fields.One2many('property.property', 'bill_id', string="Properties")
    expenditure_ids = fields.One2many('property.expenditure', 'bill_id', string="Expenditures")
