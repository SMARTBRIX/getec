# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    budget_pos_id = fields.Many2one('account.budget.post', string="Budgetary Position")
