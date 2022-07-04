# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectProject(models.Model):
    _inherit = 'project.project'

    budget_count = fields.Integer(compute='_compute_budget_count', string='# Budgets')
    property_id = fields.Many2one('property.property', string='Property')
    child_property_ids = fields.Many2many('property.property', 'project_property_rel', 'project_id', 'property_id', compute="_compute_child_properties", store=True)
    date_start = fields.Date('Start Date')
    date_end = fields.Date('End Date')

    @api.depends('property_id', 'property_id.child_property_ids', 'property_id.parent_id')
    def _compute_child_properties(self):
        for rec in self:
            rec.child_property_ids = []
            if rec.property_id:
                rec.child_property_ids = self.env['property.property'].search([('id', 'child_of', [rec.property_id.id])]).ids

    def _compute_budget_count(self):
        self.budget_count = self.env['crossovered.budget'].search_count([('project_id', 'in', self.ids)])

    def open_budget_view(self):
        budget_id = self.env['crossovered.budget'].search([('project_id', '=', self.ids)])

        return {
            'type': 'ir.actions.act_window',
            'name': 'Budgets',
            'view_mode': 'tree,form',
            'domain': [('id', '=', budget_id.ids)],
            'res_model': 'crossovered.budget'
        }
