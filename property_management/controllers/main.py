# -*- coding: utf-8 -*-

from odoo import http, _
from odoo.http import request
from odoo.osv import expression
from odoo.addons.website.controllers.main import QueryURL


class PropertyManagement(http.Controller):

    @http.route('/property_management/log_downloaded_protected_document', type='json', auth='user')
    def log_downloaded_protected_document(self, lead_id, attachment_id, model_name, **kwargs):
        lead_id = request.env['crm.lead'].sudo().browse(lead_id)
        attachment_id = request.env['ir.attachment'].sudo().browse(attachment_id)
        if model_name == 'protected.photo':
            lead_id.message_post(body=_("Downloaded protected photo %s.") % attachment_id.name)
        elif model_name == 'protected.document':
            lead_id.message_post(body=_("Downloaded protected document %s.") % attachment_id.name)
        return {}
