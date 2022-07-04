# -*- coding: utf-8 -*-

from odoo import fields, models


class PropertyProperty(models.Model):
    _inherit = 'property.property'

    document_count = fields.Integer("Documents", compute='compute_document_cnt')

    def compute_document_cnt(self):
        for rec in self:
            rec.document_count = self.env['documents.document'].search_count([('property_id', '=', rec.id)])

    def action_view_properties_documents(self):
        return {
            'name': ('Property Documents'),
            'type': 'ir.actions.act_window',
            'view_mode': 'kanban',
            'domain': [('property_id', '=', self.id)],
            'res_model': 'documents.document',
        }
