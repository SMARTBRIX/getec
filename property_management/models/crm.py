# -*- coding: utf-8 -*-

import random
import logging
import werkzeug.urls
from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    property_id = fields.Many2one('property.property', string='Property')
    cover_photo = fields.Binary(related='property_id.cover_photo')
    accepted_terms_ids = fields.Many2many('property.terms')
    property_type = fields.Selection([('s', 'For Sale'), ('r', 'For Rent')], string='For Sale / For Rent')
    property_street = fields.Char()
    property_zip = fields.Char()
    property_city = fields.Char()
    property_price = fields.Float()
    construction_year = fields.Integer()
    rooms = fields.Integer()
    living_space = fields.Integer()
    property_type_id = fields.Many2one('property.type', 'Property Type')
    commission_client = fields.Float()
    search_profile_id = fields.Many2one('property.search.profile', string='Search Profile')

    def write(self, vals):
        if 'accepted_terms_ids' in vals:
            self.message_post(body=_("Property Terms Changed."))
        return super(CrmLead, self).write(vals)

    def change_property_terms(self, vals):
        self.sudo().write({'accepted_terms_ids': vals['accepted_terms_ids']})

    def convert_opportunity(self, partner_id, user_ids=False, team_id=False):
        res = super(CrmLead, self).convert_opportunity(partner_id, user_ids, team_id)
        if self.property_type_id:
            self.create_property()
        return res

    def create_property(self):
        for_sale = for_rent = False
        asking_price = rent_price = 0
        if self.property_type == 's':
            for_sale = True
            asking_price = self.property_price
        if self.property_type == 'r':
            for_rent = True
            rent_price = self.property_price

        new_property = self.env['property.property'].create({'name': self.name, 'internal_label': self.name,
                                                             'for_sale': for_sale, 'for_rent': for_rent, 'asking_price': asking_price, 'rent_price': rent_price,
                                                             'street': self.property_street, 'zip': self.property_zip, 'city': self.property_city,
                                                             'rooms': self.rooms, 'living_space': self.living_space, 'property_type_id': self.property_type_id.id,
                                                             'commission_client': self.commission_client})
        self.write({'property_id': new_property.id})

    @api.model
    def create(self, vals):
        is_new_user = False
        if 'property_id' in vals and 'type' in vals and vals['type'] == 'opportunity':
            if 'partner_id' not in vals:
                email = vals['email_from']
                existing_user_id = self.env['res.users'].with_context(active_test=False).search(['|', ('login', '=', email), ('email', '=', email)], limit=1)
                if existing_user_id:
                    existing_user_id.active = True
                    vals['partner_id'] = existing_user_id.partner_id.id
                else:
                    default_values = {'login': email, 'name': vals['contact_name'], 'email': email, 'active': True, 'groups_id': [
                        (6, 0, [self.env.ref('base.group_portal').id])]}
                    user = self.env['res.users'].with_context(signup_valid=True).create(default_values)
                    vals['partner_id'] = user.partner_id.id
                    is_new_user = True
            # Update the property related field : If opportunity is created from frontend contactus
            if vals.get('property_id', False):
                property_id = self.env['property.property'].browse(vals.get('property_id'))
                property_type = 's'
                price = property_id.purchase_price
                if property_id.for_rent:
                    property_type = 'r'
                    price = property_id.rent_price
                vals.update({'property_type': property_type, 'property_street': property_id.street,
                             'property_zip': property_id.zip, 'property_city': property_id.city,
                             'property_price': price, 'construction_year': property_id.construction_year,
                             'rooms': property_id.rooms, 'living_space': property_id.living_space,
                             'property_type_id': property_id.property_type_id.id, 'commission_client': property_id.commission_client
                             })

            res = super().create(vals)
            res._send_inquiry_mail(is_new_user)
            return res
        else:
            return super().create(vals)

    def _send_inquiry_mail(self, is_new_user):
        template = self.env.ref('property_management.inquiry_mail')
        if template:
            for user in self.partner_id.user_ids:
                partner = self.partner_id
                lang = user.lang
                ctx = {
                    'dbname': self._cr.dbname,
                    'lang': lang,
                    'portal_url': '',
                    'user': user,
                    'object_url': self._get_object_url(),
                    'is_new': is_new_user,
                }
                if is_new_user:
                    password = random.randint(100000, 999999)
                    user.write({'password': password})
                    ctx['password'] = password
                    ctx['portal_url'] = partner.with_context(signup_force_type_in_url='', lang=lang)._get_signup_url_for_action()[partner.id]
                    partner.signup_prepare()
                template.with_context(ctx).send_mail(self.id, force_send=True)
        else:
            _logger.warning("No email template found for sending email to the portal user")

    def _get_object_url(self):
        return werkzeug.urls.url_join(self.get_base_url(), '/my/object/%s' % self.id)
