# -*- coding: utf-8 -*-

from odoo import models, fields, api


class LandlordCertificate(models.TransientModel):
    _name = 'landlord.certificate'
    _description = 'Landlord Certificate'

    def default_resident(self):
        tenancy_id = self.env['property.tenancy'].search([('id', 'in', self.env.context.get('active_ids'))])
        return tenancy_id.resident_ids

    resident_ids = fields.Many2many('res.partner', default=default_resident)
    resident_id = fields.Many2one('res.partner', string="Resident")

    def create_landlord_report(self):
        self.ensure_one()
        tenancy_id = self.env['property.tenancy'].search([('id', 'in', self.env.context.get('active_ids'))])
        datas = {
            'ids': self.resident_id,
            'model': 'property.tenancy',
            'active_ids': tenancy_id,
            'docs': self.resident_id.id
        }
        return self.env.ref('property_administration.action_landlord_certificate_report').report_action(tenancy_id, data=datas)
