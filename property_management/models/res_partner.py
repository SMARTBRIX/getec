# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from math import sin, cos, sqrt, atan2, radians
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    property_search_profile_ids = fields.One2many('property.search.profile', 'partner_id')

    # property_type_id = fields.Many2one('property.type', string='Property Type')
    # min_living_space = fields.Integer('Min. Living Space')
    # max_living_space = fields.Integer('Max. Living Space')
    # max_price = fields.Float('Maximum Price')
    # property_street = fields.Char('Street')
    # property_zip = fields.Char('Zip')
    # property_city = fields.Char('City')
    # max_distance = fields.Integer('Maximum Distance')
    # property_ids = fields.Many2many('property.property', 'rel_customer_property', 'customer_id', 'property_id',
    #                                 compute='_match_properties', store=True, string="Properties")
    # contract_type = fields.Selection([('buy', 'Buy'), ('rent', 'Rent'), ('both', 'Both')])
    property_distance_ids = fields.One2many('property.distance', 'partner_id', 'Property Distance')
    longitude = fields.Float()
    latitude = fields.Float()
    business_hours = fields.Text('Business Hours')

    def find_distance(self, customer, property):
        # location1 = self.env['res.partner']._geo_localize(customer.street,
        #                                                   customer.zip,
        #                                                   customer.city,
        #                                                   customer.state_id.name,
        #                                                   customer.country_id.name
        #                                                   )

        # location2 = self.env['res.partner']._geo_localize(property.street,
        #                                                   property.zip,
        #                                                   property.city,
        #                                                   '',
        #                                                   property.country_id.name
        #                                                   )
        R = 6373.0
        lat1 = radians(customer.partner_latitude)
        lon1 = radians(customer.partner_longitude)
        lat2 = radians(property.latitude)
        lon2 = radians(property.longitude)
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        return distance

    def create_property_distance(self):
        all_property = self.env['property.property'].search([])
        customers = self.env['res.partner'].search([])
        for customer in customers:
            customer_property = self.env['property.distance'].search([('customer_id', '=', customer.id)]).mapped('property_id')
            missing_property = set(all_property) - set(customer_property)
            for property in missing_property:
                self.env['property.distance'].create({'property_id': property.id, 'customer_id': customer.id})

    def map_distance(self):
        distance_rec = self.env['property.distance'].search([])
        for rec in distance_rec:
            # if not rec.distance:
            distance = self.find_distance(rec.customer_id, rec.property_id)
            rec.distance = distance

    @api.model
    def create(self, vals):
        res = super(ResPartner, self).create(vals)
        location = self._geo_localize(res.street,
                                      res.zip,
                                      res.city,
                                      res.state_id.name,
                                      res.country_id.name
                                      )
        # if not location:
        #     raise UserError(_('Please Correct the address to Find Proper location !'))
        if location:
            res.write({'partner_latitude': location[0], 'partner_longitude': location[1]})
            property_ids = self.env['property.property'].search([])
            for property_id in property_ids:
                self.env['property.distance'].create({'partner_id': res.id, 'property_id': property_id.id})
        return res

    def write(self, vals):
        res = super().write(vals)
        if 'street' in vals or 'zip' in vals or 'city' in vals or 'country_id' in vals:
            for rec in self:
                location = self._geo_localize(rec.street,
                                              rec.zip,
                                              rec.city,
                                              rec.state_id.name,
                                              rec.country_id.name
                                              )
                if location:
                    rec.write({'partner_latitude': location[0], 'partner_longitude': location[1]})
        return res

    # @api.depends('property_type_id', 'min_living_space', 'max_living_space',
    #              'contract_type', 'max_distance', 'max_price')
    # def _match_properties(self):
    #     #        customers = self.env['res.partner'].search([])
    #     property_obj = self.env['property.property']
    #     for rec in self:
    #         args = [
    #                 #('property_type_id', '=', rec.property_type_id.id),
    #                 ('living_space', '>=', rec.min_living_space),
    #                 ('living_space', '<=', rec.max_living_space)]

    #         if rec.property_type_id:
    #             args.extend([('property_type_id', '=', rec.property_type_id.id)])
    #         if rec.contract_type == 'buy':
    #             args.extend([('for_sale', '=', True), ('for_rent', '=', False), ('purchase_price', '<=', rec.max_price)])
    #         elif rec.contract_type == 'rent':
    #             args.extend([('for_rent', '=', True), ('for_sale', '=', False), ('rent_incl_heat', '<=', rec.max_price)])
    #         elif rec.contract_type in ('both', False):
    #             args.extend(['|', ('purchase_price', '<=', rec.max_price), ('rent_incl_heat', '<=', rec.max_price)])

    #         match_distance_property = self.env['property.distance'].search(
    #             [('customer_id', '=', rec.id), ('distance', '<=', rec.max_distance)]).mapped('property_id')
    #         if match_distance_property:
    #             args.extend([('id', 'in', match_distance_property.ids)])
    #         property_ids = property_obj.search(args)
    #         if property_ids:
    #             rec.property_ids = property_ids.ids
    #         else:
    #             rec.property_ids = False
    #     return True

    # def create_opportuniy(self):
    #     partner_id = self.id
    #     property_id = self.env.context.get('property_id')
    #     price = 0
    #     lead_found = self.env['crm.lead'].search([('partner_id', '=', partner_id), ('property_id', '=', property_id)])
    #     if lead_found:
    #         raise UserError(_('opportunity already created for this Customer and Property !'))

    #     property = self.env['property.property'].browse(property_id)
    #     if property.for_rent:
    #         price = property.rent_incl_heat
    #     elif property.for_sale:
    #         price = property.purchase_price

    #     self.env['crm.lead'].create({'name': property.name,
    #                                  'planned_revenue': price,
    #                                  'partner_id': partner_id,
    #                                  'property_id': property_id,
    #                                  'type': 'opportunity'
    #                                  })
