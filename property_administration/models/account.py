# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    property_ids = fields.One2many('property.property', 'bill_id', string="Properties")
    expenditure_ids = fields.One2many('property.expenditure', 'bill_id', string="Expenditures")
    tenancy_id = fields.Many2one('property.tenancy')


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    property_id = fields.Many2one('property.property', string="Property")


class AccountAccount(models.Model):
    _inherit = 'account.account'

    account_type = fields.Selection([('giro', 'Giro'), ('credit', 'Credit')], string="Account Type")
