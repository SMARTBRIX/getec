# -*- coding: utf-8 -*-

from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.http import request, route


class PropertyPortalTenancy(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(PropertyPortalTenancy, self)._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        values['tenancies_count'] = request.env['property.tenancy'].sudo().search_count([('contractual_partner_ids', 'in', partner.id)])
        return values

    @route(['/my/tenancies', '/my/tenancies/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_tenancies(self, page=1, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        PropertyTenancy = request.env['property.tenancy']

        domain = [
            ('contractual_partner_ids', 'in', partner.id)
        ]

        objects_count = PropertyTenancy.sudo().search_count(domain)
        pager = portal_pager(
            url='/my/tenancies',
            total=objects_count,
            page=page,
            step=self._items_per_page
        )

        objects = PropertyTenancy.sudo().search(domain, limit=self._items_per_page, offset=pager['offset'])

        values.update({
            'objects': objects,
            'page_name': 'tenancies',
            'pager': pager,
        })
        return request.render('property_administration.portal_my_tenancies', values)

    @route(['/my/tenancy/<int:tenancy_id>'], type='http', auth='user', website=True)
    def portal_my_tenancy_object(self, tenancy_id, **kw):
        tenancy = request.env['property.tenancy'].sudo().browse(tenancy_id)
        contractual_partner = ""
        contractual_partner += ': %s' % ', '.join(tenancy.contractual_partner_ids.mapped('name'))

        return request.render('property_administration.portal_my_tenancy_object', {
            'tenancy': tenancy,
            'page_name': 'tenancies',
            'contractual_partner': contractual_partner
        })
