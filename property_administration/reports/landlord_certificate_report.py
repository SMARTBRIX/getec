# -*- coding: utf-8 -*-


from odoo import api, models


class LandlordCertificateReport(models.AbstractModel):
    _name = 'report.property_administration.landlord_certificate'
    _description = 'Landlord Certificate Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        if data['context'].get('active_ids'):
            tenancy = self.env['property.tenancy'].browse(data['context']['active_ids'])
            partner = self.env['res.partner'].browse(data['docs'])
        return {
            'data': data,
            'tenancies': tenancy,
            'resident': partner
        }
