# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class BudgetaryCategory(models.Model):
    _name = 'budgetary.category'
    _description = "Property Budgetary Category"

    name = fields.Char(string="Name")
    parent_id = fields.Many2one('budgetary.category', string="Parent Category")

    @api.constrains('parent_id')
    def _check_category_recursion_property(self):
        if not self._check_recursion():
            raise ValidationError(_('Error ! You cannot create recursive categories.'))
