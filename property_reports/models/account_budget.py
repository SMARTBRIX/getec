# -*- coding: utf-8 -*-

from odoo import models, fields


class CrossoveredBudgetLines(models.Model):
    _inherit = "crossovered.budget.lines"

    theoritical_amount_stored = fields.Monetary(related='theoritical_amount', store=True)
    practical_amount_stored = fields.Monetary(related='practical_amount', store=True)
