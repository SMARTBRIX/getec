# -*- coding: utf-8 -*-

from odoo import models, fields
from datetime import timedelta


class TenancyUtilityBill(models.TransientModel):
    _name = 'tenancy.utility.bill'
    _description = 'Tenancy Utility Bill'

    date_start = fields.Date("Start Date")
    date_end = fields.Date("End Date")

    def create_utility_bill(self):
        tenancy_ids = self.env['property.tenancy'].browse(self.env.context.get('active_ids'))

        for rec in tenancy_ids:
            company_id = tenancy_ids.property_id.company_id
            attachment_ids = []
            final_dict = {}
            if rec.date_start < self.date_start:
                ten_date_start = self.date_start
            else:
                ten_date_start = rec.date_start
            if rec.date_end > self.date_end:
                ten_date_end = self.date_end
            else:
                ten_date_end = rec.date_end

            postings = self.env['property.journal'].search([('tenancy_id', '=', rec.id)]).filtered(lambda x: not (
                x.date_start < self.date_start and x.date_end < self.date_start)).filtered(lambda x: not (x.date_start > self.date_end and x.date_end > self.date_end))
            for posting in postings:
                if posting.date_start < self.date_start:
                    day_amount = round(posting.amount / (posting.date_end - posting.date_start).days, 5)
                    new_posting_dt_start = posting.date_start
                    new_posting_dt_end = self.date_start + timedelta(days=-1)
                    new_posting_dt_diff = (new_posting_dt_end - new_posting_dt_start).days
                    new_posting_amount = round(day_amount * new_posting_dt_diff, 5)
                    new_posting_vals = {'date_start': new_posting_dt_start,
                                        'date_end': new_posting_dt_end,
                                        'amount': new_posting_amount}
                    posting.copy(new_posting_vals)
                    posting.write({'date_start': self.date_start, 'cleared': True,
                                   'amount': round(day_amount * (posting.date_end - self.date_start).days, 1)})
                if posting.date_end > self.date_end:
                    day_amount = posting.amount / \
                        (posting.date_end - posting.date_start).days
                    new_posting_dt_start = self.date_end + timedelta(days=1)
                    new_posting_dt_end = posting.date_end
                    new_posting_dt_diff = (
                        new_posting_dt_end - new_posting_dt_start).days
                    new_posting_amount = day_amount * new_posting_dt_diff
                    new_posting_vals = {'date_start': new_posting_dt_start,
                                        'date_end': new_posting_dt_end,
                                        'amount': new_posting_amount}
                    posting.copy(new_posting_vals)
                    posting.write({'date_end': self.date_end, 'cleared': True,
                                   'amount': day_amount * (self.date_end - posting.date_start).days})

                if posting.cost_type_id not in final_dict.keys():
                    final_dict[posting.cost_type_id] = [posting]
                else:
                    final_dict[posting.cost_type_id].append(posting)

            if final_dict:
                narration = 'Customer:' + rec.partner_id.name
                narration = narration + "\n" + 'Company:' + rec.company_id.name
                narration = narration + "\n" + 'Reference:' + rec.name
                narration = narration + "\n" + 'Residents:' + \
                    ','.join([recident.name for recident in rec.resident_ids])
                narration = narration + "\n" + 'Utiltiy Period:' + \
                    self.date_start.strftime(
                        '%m/%d/%Y') + ' - ' + self.date_end.strftime('%m/%d/%Y')
                narration = narration + "\n" + 'Tenancy Period:' + \
                    ten_date_start.strftime(
                        '%m/%d/%Y') + ' - ' + ten_date_end.strftime('%m/%d/%Y')
                narration = narration + "\n" + 'Contractual Partners: ' + \
                    ', '.join(
                        [partner.name for partner in rec.contractual_partner_ids])

                journal_id = self.env['account.move'].with_context(
                    {'default_type': 'out_invoice'})._get_default_journal()
                if rec.property_id.parent_property_id:
                    property_ids = [rec.property_id.parent_property_id.ids]
                else:
                    property_ids = [rec.property_id.id]
                inv = self.env['account.move'].create({'partner_id': rec.partner_id.id or False, 'ref': rec.name, 'property_ids': [(6, 0, property_ids)],
                                                       'journal_id': journal_id.id, 'type': 'out_invoice', 'narration': narration})
                rec.property_id.bill_id = inv.id
                for d in final_dict:
                    # d = cost type
                    posting_lst = final_dict.get(d)
                    desc = ''
                    original_amount = 0
                    sum_amount = 0
                    # tax_product = d.product_id.taxes_id.filtered(lambda t: t.company_id == company_id.id)
                    taxes = rec.rent_product_id.taxes_id.filtered(lambda t: t.company_id.id == company_id.id)

                    for posting in posting_lst:
                        for attach in posting.documents:
                            attach.sudo().copy({'res_id': inv.id, 'res_model': 'account.move'})
                        original_amount += posting.expenditure_id.amount
                        sum_amount += posting.amount
                    tax_ids = rec.rent_product_id.taxes_id.filtered(lambda x: x.company_id.id == company_id.id)
                    if tax_ids and tax_ids[0].amount == 0:
                        if d.product_id and d.product_id.taxes_id:
                            sum_amount += posting.amount * (posting.tax_id.amount / 100 + 1)
                            original_amount += posting.expenditure_id.amount * (posting.tax_id.amount / 100 + 1)

                            # sum_amount = sum_amount * (d.product_id.taxes_id.filtered(lambda x: x.company_id.id == company_id.id).amount / 100 + 1)
                            # original_amount = original_amount * (d.product_id.taxes_id.filtered(lambda x: x.company_id.id == company_id.id).amount / 100 + 1)
                        else:
                            sum_amount += posting.amount
                            original_amount += posting.expenditure_id.amount

                    allocation_formula = dict(d._fields['allocation_formula'].selection).get(d.allocation_formula)
                    desc = "Cost Type:" + d.name + "\n"
                    desc += "Total Amount:" + str(original_amount) + "\n"
                    if d.allocation_formula:
                        desc += "Allocation Formula:" + str(allocation_formula)

                    # account_id = inv.journal_id.default_credit_account_id.id
                    account_id = rec.rent_product_id.get_product_accounts()['income']
                    analytic_account = False
                    if rec.property_id.parent_property_id:
                        analytic_account = rec.property_id.parent_property_id.analytic_account_id.id or False
                    else:
                        analytic_account = rec.property_id.analytic_account_id.id or False

                    inv_line = {'product_id': d.product_id.id, 'product_uom_id': d.product_id.uom_id.id, 'name': desc,
                                'move_id': inv.id, 'account_id': account_id.id, 'analytic_account_id': analytic_account,
                                'quantity': 1, 'price_unit': sum_amount, 'tax_ids': taxes.ids}
                    self.env['account.move.line'].with_context(
                        {'check_move_validity': False}).create(inv_line)
            inv.with_context({'check_move_validity': False})._recompute_tax_lines()
            inv.with_context({'check_move_validity': False})._onchange_recompute_dynamic_lines()
