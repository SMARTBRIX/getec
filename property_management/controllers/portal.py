# -*- coding: utf-8 -*-

from odoo import http
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.http import request, route
from werkzeug.exceptions import NotFound


class PropertyPortal(CustomerPortal):

    SEARCH_PROFILE_FIELDS = ['property_type_id', 'contract_type', 'min_living_space', 'max_living_space',
                             'max_price', 'property_street', 'property_city', 'property_zip', 'max_distance', 'auto_marketing']

    def _prepare_portal_layout_values(self):
        values = super(PropertyPortal, self)._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        values['property_objects_count'] = request.env['crm.lead'].sudo().search_count(
            [('type', '=', 'opportunity'), ('property_id', '!=', False), ('partner_id', '=', partner.id)])
        values['property_search_profiles_count'] = len(partner.property_search_profile_ids)
        return values

    @route(['/my/property_objects', '/my/property_objects/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_objects(self, page=1, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        CrmLead = request.env['crm.lead']

        domain = [
            ('type', '=', 'opportunity'), ('property_id', '!=', False), ('partner_id', '=', partner.id)
        ]

        objects_count = CrmLead.sudo().search_count(domain)
        pager = portal_pager(
            url='/my/objects',
            total=objects_count,
            page=page,
            step=self._items_per_page
        )

        objects = CrmLead.sudo().search(domain, limit=self._items_per_page, offset=pager['offset'])

        values.update({
            'objects': objects,
            'page_name': 'property_objects',
            'pager': pager,
        })
        return request.render('property_management.portal_my_objects', values)

    @route(['/my/object/<int:lead_id>'], type='http', auth='user', website=True)
    def portal_my_property_object(self, lead_id, **kw):
        lead = request.env['crm.lead'].sudo().browse(lead_id)
        if lead.type != 'opportunity':
            raise NotFound()
        if lead.partner_id.id != request.env.user.partner_id.id:
            raise NotFound()

        return request.render('property_management.portal_my_property_object', {
            'lead': lead,
            'page_name': 'my_expose',
            'terms': lead.property_id.contract_type_id.terms_ids,
            'accepted_terms_ids': lead.accepted_terms_ids.ids,
        })

    @route(['/my/property_search_profiles'], type='http', auth='user', website=True)
    def portal_my_search_profiles(self, page=1, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        values.update({
            'profiles': partner.property_search_profile_ids,
            'page_name': 'property_search_profiles',
        })
        return request.render('property_management.portal_my_search_profiles', values)

    @route([
        '/my/property_search_profile/<model("property.search.profile"):profile_id>',
        '/my/property_search_profile'
    ], type='http', auth='user', website=True)
    def portal_property_search_profile(self, profile_id=None, **post):
        values = {}
        PropertySearchProfile = request.env['property.search.profile']

        if post and request.httprequest.method == 'POST':
            values.update({key: post[key] for key in self.SEARCH_PROFILE_FIELDS if key in post})
            for field in set(['property_type_id']) & set(values.keys()):
                try:
                    values[field] = int(values[field])
                except:
                    values[field] = False
            values['auto_marketing'] = values.get('auto_marketing') == 'on'
            if profile_id:
                profile_id = PropertySearchProfile.browse(int(profile_id))
                profile_id.write(values)
            else:
                profile_id = PropertySearchProfile.create(values)
            return request.redirect('/my/property_search_profile/%s?saved=1' % profile_id.id)

        values.update({
            'profile_id': profile_id,
            'property_types': request.env['property.type'].sudo().search([]),
            'contracts': PropertySearchProfile._fields['contract_type']._description_selection(request.env),
        })

        return request.render('property_management.portal_my_property_search_profile', values)

    @http.route('/my/property_search_profile_delete/<model("property.search.profile"):profile_id>', type='http', auth='user', website=True)
    def property_search_profile_delete(self, profile_id, **kwargs):
        if profile_id.partner_id.id != request.env.user.partner_id.id:
            raise NotFound()
        profile_id.unlink()
        return request.redirect('/my/property_search_profiles')
