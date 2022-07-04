# -*- coding: utf-8 -*-

from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.exceptions import AccessError, MissingError
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.http import request, route


class PropertyPortalTenancy(CustomerPortal):

    def _prepare_portal_domain(self, partner):
        return [('contractual_partner_ids', 'in', partner.id)]

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id
        if 'tenancies_count' in counters:
            tenancy = request.env['property.tenancy']
            values['tenancies_count'] = tenancy.search_count(self._prepare_portal_domain(partner)) \
                if tenancy.check_access_rights('read', raise_exception=False) else 0
        return values

    @route(['/my/tenancies', '/my/tenancies/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_tenancies(self, page=1, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        PropertyTenancy = request.env['property.tenancy']

        domain = self._prepare_portal_domain(partner)

        objects_count = PropertyTenancy.search_count(domain)
        pager = portal_pager(
            url='/my/tenancies',
            total=objects_count,
            page=page,
            step=self._items_per_page
        )

        objects = PropertyTenancy.search(domain, limit=self._items_per_page, offset=pager['offset'])

        values.update({
            'objects': objects.sudo(),
            'page_name': 'tenancies',
            'pager': pager,
        })
        return request.render('property_administration.portal_my_tenancies', values)

    @route(['/my/tenancy/<int:tenancy_id>'], type='http', auth='user', website=True)
    def portal_my_tenancy_object(self, tenancy_id, access_token=None, **kw):
        try:
            tenancy_sudo = self._document_check_access('property.tenancy', tenancy_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        # tenancy = request.env['property.tenancy'].browse(tenancy_id)
        contractual_partner = ""
        contractual_partner += ': %s' % ', '.join(tenancy_sudo.contractual_partner_ids.mapped('name'))

        resident_ids_name = ""
        resident_ids_name += ': %s' % ', '.join(tenancy_sudo.resident_ids.mapped('name'))

        return request.render('property_administration.portal_my_tenancy_object', {
            'tenancy': tenancy_sudo,
            'page_name': 'tenancies',
            'contractual_partner': contractual_partner,
            'resident_ids_name': resident_ids_name
        })
