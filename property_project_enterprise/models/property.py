# -*- coding: utf-8 -*-

from odoo import models, fields


class Property(models.Model):
    _inherit = 'property.property'

    project_count = fields.Integer(compute="_compute_project_count")

    def _compute_project_count(self):
        property_ids = [self.id] + self.child_property_ids.ids
        project_ids = self.env['project.project'].search([('property_id', 'in', property_ids)])
        self.project_count = len(project_ids)

    def action_view_projects(self):
        property_ids = [self.id] + self.child_property_ids.ids
        project_ids = self.env['project.project'].search([('property_id', 'in', property_ids)])
        return {
            'name': ('Projects'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', project_ids.ids)],
            'res_model': 'project.project',
        }
