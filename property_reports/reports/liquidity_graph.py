# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta
from datetime import date
import datetime
import calendar
from odoo import tools

from odoo import fields, models


class LiquidityReport(models.Model):
    _name = "liquidity.report"
    _description = "Liquidity Report"

    start_date = fields.Date()
    practical_budgets = fields.Float()
    start_value = fields.Float()
    charges = fields.Float()
    repayments = fields.Float()
    theoritical_budgets = fields.Float()
    rents = fields.Float()
    sale_price = fields.Float()
    amount = fields.Float()

    def _generate_report(self):
        current_month = date.today().month
        current_year = date.today().year
        last_day = calendar.monthrange(current_year, current_month)[1]
        number_of_months = self.env.context.get('number_of_months')
        if number_of_months:
            for i in range(1, number_of_months + 1):
                if current_month > 12:
                    current_year = current_year + 1
                    current_month = (current_month % 12)
                    last_day = calendar.monthrange(current_year, current_month)[1]
                    next_date = datetime.date(day=last_day, month=current_month, year=current_year)
                else:
                    current_year = current_year
                    last_day = calendar.monthrange(current_year, current_month)[1]
                    next_date = datetime.date(day=last_day, month=current_month, year=current_year)
                first_date_moth = datetime.date(day=1, month=current_month, year=current_year)
                current_month = current_month + 1
                property_ids = self.env.context.get('property_ids')
                start_value = practical_budgets = theoritical_budgets = rents = repayments = charges = sale_price = 0
                for property_id in property_ids:
                    charges_account_id = property_id.company_id.charges_account_id.id
                    child_property_ids = self.env['property.property'].search([('id', 'child_of', [property_id.id])])

                    practical_budgets += sum(self.env['crossovered.budget.lines'].search([('analytic_account_id', '=', property_id.analytic_account_id.id),
                        ('crossovered_budget_id.state', 'not in', ('cancel', 'draft'))]).mapped('practical_amount'))
                    journal_ids = self.env['account.journal'].sudo().search([('property_id', 'in', child_property_ids.ids), ('default_account_id.account_type', '!=', 'credit')])

                    statement_lines = self.env['account.bank.statement.line'].sudo().search([('journal_id', 'in', journal_ids.ids)])
                    start_value += sum(statement_lines.mapped('amount'))

                    charges -= sum(self.env['account.move.line'].sudo().search([('analytic_account_id', '=', property_id.analytic_account_id.id), 
                        ('account_id', '=', charges_account_id), ('date', '<', first_date_moth), ('parent_state', '=', 'posted')]).mapped('debit'))
                    
                    repayments -= sum(self.env['account.move.line'].sudo().search([('analytic_account_id', '=', property_id.analytic_account_id.id), 
                        ('account_id.account_type', '=', 'credit'), ('date', '<', first_date_moth), ('parent_state', '=', 'posted')]).mapped('debit'))

                    budget_lines = self.env['crossovered.budget.lines'].search([('analytic_account_id', '=', property_id.analytic_account_id.id),
                        ('crossovered_budget_id.state', 'not in', ('cancel', 'draft'))])
                    
                    # for line in budget_lines:
                    theoritical_budgets += self._compute_theoritical_amount(budget_lines, next_date)
                    tenancy_rents = self.env['property.rent'].search([('tenancy_id.property_id', 'in', child_property_ids.ids), ('date_start', '<', next_date)])
                    rent = sum(tenancy_rents.mapped('rent'))
                    ancillary_costs = sum(tenancy_rents.mapped('ancillary_costs'))
                    heating_costs = sum(tenancy_rents.mapped('heating_costs'))
                    rents += rent + ancillary_costs + heating_costs

                    if property_id.sale_date and next_date < property_id.sale_date:
                        sale_price += 0
                    elif property_id.sale_date and next_date > property_id.sale_date:
                        sale_price += property_id.purchase_price

                amount = theoritical_budgets - practical_budgets + start_value + (charges * i) + (repayments * i) + (rents * i)
                self.env['liquidity.report'].create({'start_date': next_date, 'practical_budgets': practical_budgets, 
                    'theoritical_budgets': theoritical_budgets, 'sale_price': sale_price,
                    'rents': rents * i, 'start_value': start_value, 'charges': (charges * i), 'repayments': (repayments * i), 'amount': amount})

    def _compute_theoritical_amount(self, budget_lines, last_date_month):
        # beware: 'today' variable is mocked in the python tests and thus, its implementation matter
        th_budget = 0
        for line in budget_lines:
            diff_startdate_date = last_date_month - line.date_from
            diff_startdate_enddate = line.date_to - line.date_from
            if line.date_from > last_date_month:
                th_budget += 0
            elif line.date_to < last_date_month:
                th_budget += line.planned_amount
            else:
                th_budget += line.planned_amount * diff_startdate_date / diff_startdate_enddate
        return th_budget

    def init(self):
        self.env['liquidity.report'].search([]).unlink()
        self.with_context(self.env.context)._generate_report()
