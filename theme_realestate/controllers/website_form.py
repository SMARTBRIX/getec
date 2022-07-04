# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.form import WebsiteForm


class RealEstateWebsiteForm(WebsiteForm):

    @http.route('/website_form/<string:model_name>', type='http', auth="public", methods=['POST'], website=True)
    def website_form(self, model_name, **kwargs):
        model_record = request.env['ir.model'].sudo().search([('model', '=', model_name), ('website_form_access', '=', True)])
        if model_record and hasattr(request.env[model_name], 'phone_format'):
            try:
                data = self.extract_data(model_record, request.params)
            except:
                # no specific management, super will do it
                pass
            else:
                record = data.get('record', {})
                if record.get('property_id'):
                    existing_partner = request.env['res.partner'].search([('email', '=', record.get('email_from'))], limit=1)
                    if existing_partner:
                        request.params.update({
                            'partner_id': existing_partner.id,
                        })
        return super(RealEstateWebsiteForm, self).website_form(model_name, **kwargs)

    def insert_record(self, request, model, values, custom, meta=None):
        is_lead_model = model.model == 'crm.lead'
        if is_lead_model:
            if 'property_id' in values:
                values.update({
                    'user_id': request.website.sudo().dr_property_sales_team.user_id.id,
                    'team_id': request.website.sudo().dr_property_sales_team.id,
                    'stage_id': request.website.sudo().dr_property_crm_stage.id,
                    'type': 'opportunity',
                })
        return super(RealEstateWebsiteForm, self).insert_record(request, model, values, custom, meta=meta)
