# -*- coding: utf-8 -*-

from odoo import fields, models
from datetime import date


class PropertyStage(models.Model):
    _inherit = 'property.stage'

    administration_stage = fields.Boolean("Administration Stage?")


class PropertyProperty(models.Model):
    _inherit = 'property.property'

    cost_type_ids = fields.Many2many('property.cost.type', string="Cost Types")
    bill_id = fields.Many2one('account.move')
    journal_entry_count = fields.Integer(compute="_compute_journal_entries")
    expenditure_count = fields.Integer(compute="_compute_expenditure_count")
    tenancy_count = fields.Integer(compute="_compute_tenancy_count")
    analytic_account_id = fields.Many2one('account.analytic.account', string="Analytic Account")
    co_owenership = fields.Integer(string='Co-Ownership')

    facility_manager_id = fields.Many2one('res.partner', string="Facility Manager")
    winter_service_id = fields.Many2one('res.partner', string="Winter Service")
    gardener_id = fields.Many2one('res.partner', string="Gardener")
    cleaning_id = fields.Many2one('res.partner', string="Cleaning")
    electrician_id = fields.Many2one('res.partner', string="Electrician")
    plumber_id = fields.Many2one('res.partner', string="Plumber")
    external_admin_id = fields.Many2one('res.partner', string='External administrator')

    key_safe = fields.Char("Key Safe")

    def _compute_journal_entries(self):
        property_ids = [self.id] + self.child_property_ids.ids
        tenancy_ids = self.env['property.tenancy'].search([('property_id', 'in', property_ids)])
        journal_ids = self.env['property.journal'].search([('cleared', '=', False), ('tenancy_id', 'in', tenancy_ids.ids)])
        self.journal_entry_count = len(journal_ids)

    def _compute_expenditure_count(self):
        property_ids = [self.id] + self.child_property_ids.ids
        expenditure_ids = self.env['property.expenditure'].search([('property_id', 'in', property_ids)])
        self.expenditure_count = len(expenditure_ids)

    def _compute_tenancy_count(self):
        property_ids = [self.id] + self.child_property_ids.ids
        tenancy_ids = self.env['property.tenancy'].search([('property_id', 'in', property_ids)])
        self.tenancy_count = len(tenancy_ids)

    def action_view_journal_entry(self):
        property_ids = [self.id] + self.child_property_ids.ids
        tenancy_ids = self.env['property.tenancy'].search([('property_id', 'in', property_ids)])
        if tenancy_ids:
            journal_ids = self.env['property.journal'].search([('cleared', '=', False), ('tenancy_id', 'in', tenancy_ids.ids)])
            return {
                'name': ('Expenditure'),
                'type': 'ir.actions.act_window',
                'view_mode': 'tree,form',
                'domain': [('id', 'in', journal_ids.ids)],
                'res_model': 'property.journal',
            }

    def action_redirect_administration(self):
        form_view_ref = self.env.ref(
            'property_administration.property_form_administration', False)
        return {
            'name': ('Managed Objects'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_id': self.id,
            'views': [(form_view_ref.id, 'form')],
            'res_model': 'property.property'
        }

    def action_view_expenditure(self):
        property_ids = [self.id] + self.child_property_ids.ids
        expenditure_ids = self.env['property.expenditure'].search([('property_id', 'in', property_ids)])
        return {
            'name': ('Expenditure'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', expenditure_ids.ids)],
            'res_model': 'property.expenditure',
        }

    def action_view_data_acquisition(self):
        return {
            'name': ('Property'),
            'res_model': 'property.property',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'current',
        }

    def action_view_tenancies(self):
        property_ids = [self.id] + self.child_property_ids.ids
        tenancy_ids = self.env['property.tenancy'].search([('property_id', 'in', property_ids)])
        return {
            'name': ('Tenancy'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', tenancy_ids.ids)],
            'res_model': 'property.tenancy',
        }

    def action_create_tenancy(self):
        tenancy_id = self.env['property.tenancy'].create(
            {'property_id': self.id, 'name': self.name, 'date_start': date.today(), 'date_end': date.today()})
        tenancy_ids = self.env['property.tenancy'].search(
            [('property_id', '=', self.id)])
        self.tenancy_count = len(tenancy_ids)
        return {
            'name': ('Tenancy'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'domain': [('id', '=', tenancy_id.id)],
            'res_model': 'property.tenancy',
        }

    def action_create_expenditure(self):
        expenditure_id = self.env['property.expenditure'].create(
            {'property_id': self.id})
        expenditure_ids = self.env['property.expenditure'].search(
            [('property_id', '=', self.id)])
        self.expenditure_count = len(expenditure_ids)
        return {
            'name': ('Expenditure'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'domain': [('id', '=', expenditure_id.id)],
            'res_model': 'property.expenditure',
        }
