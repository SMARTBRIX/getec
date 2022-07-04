# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AccountExpenditure(models.TransientModel):
    _name = 'account.expenditure'
    _description = 'Account Expenditure'

    name = fields.Char()
    property_id = fields.Many2one('property.property', string="Property")
    cost_type_id = fields.Many2one('property.cost.type', string="Cost Type")
    vendor_id = fields.Many2one('res.partner', string="Vendor")
    period_begin = fields.Date("Period Begin")
    period_end = fields.Date("Period End")
    amount = fields.Float()
    cost_type_ids = fields.Many2many('property.cost.type', related="property_id.cost_type_ids")
    tax_id = fields.Many2one('account.tax', 'Tax')

    @api.model
    def default_get(self, fields):
        res = super(AccountExpenditure, self).default_get(fields)
        res_id = self._context.get('active_id')

        invoice = self.env['account.move'].browse(res_id)
        vendor_amount = invoice.amount_untaxed
        expenditure_amount = sum(invoice.expenditure_ids.mapped('amount'))
        tax_id = invoice.invoice_line_ids[0].tax_ids and invoice.invoice_line_ids[0].tax_ids[0]

        if not invoice.type == 'in_invoice':
            raise ValidationError("Only create Expenditure from Vendor Bill")

        res.update({
            'name': invoice.name,
            'vendor_id': invoice.partner_id.id,
            'amount': vendor_amount - expenditure_amount,
            'tax_id': tax_id.id
        })
        return res

    def create_expenditure(self):
        expenditure_id = self.env['property.expenditure'].create({'bill_id': self.env.context.get('active_id'), 'name': self.name, 'property_id': self.property_id.id, 'cost_type_id': self.cost_type_id.id,
                                                'vendor_id': self.vendor_id.id, 'date_start': self.period_begin, 'date_end': self.period_end, 'amount': self.amount})
        self.property_id.write({'bill_id': self.env.context.get('active_id')})

        return {
            'name': ('Expenditure'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'domain': [('id', '=', expenditure_id.id)],
            'res_model': 'property.expenditure',
        }
