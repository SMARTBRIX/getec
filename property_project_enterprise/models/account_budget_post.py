# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountBudgetPost(models.Model):
    _inherit = 'account.budget.post'

    budget_categ_id = fields.Many2one('budgetary.category', string="Budgetary Category")

    def _check_account_ids(self, vals):
        return True


class CrossoveredBudgetLines(models.Model):
    _inherit = "crossovered.budget.lines"

    budget_categ_id = fields.Many2one('budgetary.category', string="Budgetary Category")
    parent_id = fields.Many2one('budgetary.category', related='budget_categ_id.parent_id', string="Parent Category", store=True)

    @api.onchange('general_budget_id')
    def _onchange_general_budget(self):
        self.budget_categ_id = self.general_budget_id.budget_categ_id

    def _compute_practical_amount(self):
        for line in self:
            date_to = line.date_to
            date_from = line.date_from
            domain = [('budget_pos_id', '=', line.general_budget_id.id),
                      ('date', '>=', date_from), ('date', '<=', date_to), ('move_id.state', '=', 'posted')]

            if line.analytic_account_id.id:
                domain += [('analytic_account_id', '=', line.analytic_account_id.id)]

            aml_obj = self.env['account.move.line']
            where_query = aml_obj._where_calc(domain)
            aml_obj._apply_ir_rules(where_query, 'read')
            from_clause, where_clause, where_clause_params = where_query.get_sql()
            select = "SELECT sum(credit)-sum(debit) from " + from_clause + " where " + where_clause

            self.env.cr.execute(select, where_clause_params)
            line.practical_amount = self.env.cr.fetchone()[0] or 0.0

    def action_open_budget_entries(self):
        action = self.env['ir.actions.act_window'].for_xml_id('account', 'action_account_moves_all_a')
        domain = [('budget_pos_id', '=', self.general_budget_id.id), ('date', '>=', self.date_from), ('date', '<=', self.date_to)]
        if self.analytic_account_id:
            domain += [('analytic_account_id', '=', self.analytic_account_id.id)]
        action['domain'] = domain
        return action


class CrossoveredBudget(models.Model):
    _inherit = "crossovered.budget"

    project_id = fields.Many2one('project.project', string="Project")
