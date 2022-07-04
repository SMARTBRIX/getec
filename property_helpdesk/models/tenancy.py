# -*- coding: utf-8 -*-

from odoo import models, fields


class Property(models.Model):
    _inherit = 'property.tenancy'

    ticket_count = fields.Integer(compute='compute_tickets_count')

    def compute_tickets_count(self):
        for rec in self:
            rec.ticket_count = self.env['helpdesk.ticket'].search_count([('tenancy_id', '=', rec.id)])

    def show_tickets(self):
        return {
            'name': 'Ticket',
            'view_mode': 'tree,form',
            'res_model': 'helpdesk.ticket',
            'domain': [('tenancy_id', '=', self.id)],
            'context': {'default_tenancy_id': self.id},
            'type': 'ir.actions.act_window'
        }
