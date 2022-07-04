# -*- coding: utf-8 -*-

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    tenancy_count = fields.Integer(compute="_compute_tenancy_count")
    responsibility_count = fields.Integer(compute="_compute_responsibility_count")

    def _compute_tenancy_count(self):
        tenancy_ids = self.env['property.tenancy'].search(['|', '|', ('partner_id', '=', self.id), ('contractual_partner_ids', 'ilike', self.id), ('resident_ids', 'ilike', self.id)])
        self.tenancy_count = len(tenancy_ids)

    def action_view_tenancies(self):
        tenancy_ids = self.env['property.tenancy'].search(['|', '|', ('partner_id', '=', self.id), ('contractual_partner_ids', 'ilike', self.id), ('resident_ids', 'ilike', self.id)])
        return {
            'name': ('Tenancy'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', tenancy_ids.ids)],
            'res_model': 'property.tenancy',
        }

    def _compute_responsibility_count(self):
        property_ids = self.env['property.property'].search(['|', '|', '|', '|', '|', '|', ('facility_manager_id', '=', self.id),
                                                             ('winter_service_id', '=', self.id), ('gardener_id', '=', self.id),
                                                             ('cleaning_id', '=', self.id), ('electrician_id', '=', self.id),
                                                             ('plumber_id', '=', self.id), ('external_admin_id', '=', self.id)])
        self.responsibility_count = len(property_ids)

    def action_view_responsibilities(self):
        property_ids = self.env['property.property'].search(['|', '|', '|', '|', '|', '|', ('facility_manager_id', '=', self.id),
                                                             ('winter_service_id', '=', self.id), ('gardener_id', '=', self.id),
                                                             ('cleaning_id', '=', self.id), ('electrician_id', '=', self.id),
                                                             ('plumber_id', '=', self.id), ('external_admin_id', '=', self.id)])
        return {
            'name': ('Properties'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', property_ids.ids)],
            'res_model': 'property.property',
        }
