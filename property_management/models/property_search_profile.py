# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from math import sin, cos, sqrt, atan2, radians


class PropertySearchProfile(models.Model):
    _name = 'property.search.profile'
    _description = 'Property Search Profile'
    _rec_name = 'property_type_id'

    partner_id = fields.Many2one('res.partner', string='Customer', default=lambda self: self.env.user.partner_id.id)
    property_type_id = fields.Many2one('property.type', string='Property Type')
    contract_type = fields.Selection([('buy', 'Buy'), ('rent', 'Rent'), ('both', 'Both')])
    min_living_space = fields.Integer('Min. Living Space')
    max_living_space = fields.Integer('Max. Living Space')
    max_price = fields.Float('Maximum Price')
    # property_street = fields.Char('Street')
    # property_zip = fields.Char('Zip')
    # property_city = fields.Char('City')
    max_distance = fields.Integer('Maximum Distance')
    property_ids = fields.Many2many('property.property', 'rel_search_profile_property', 'search_profile_id', 'property_id',
                                    compute='_match_properties', store=True, string="Properties")
    property_ids_count = fields.Integer(compute='compute_property_count')
    auto_marketing = fields.Boolean('Automatic Marketing')

    def compute_property_count(self):
        for rec in self:
            rec.property_ids_count = len(rec.property_ids)

    def action_view_property(self):
        action = self.env.ref('property_management.action_property').read()[0]
        action['domain'] = [('id', 'in', self.property_ids.ids)]
        return action

    @api.depends('property_type_id', 'min_living_space', 'max_living_space',
                 'contract_type', 'max_distance', 'max_price', 'partner_id',
                 'property_ids.property_type_id', 'property_ids.living_space',
                 'property_ids.purchase_price', 'property_ids.rent_incl_heat')
    def _match_properties(self):
        property_obj = self.env['property.property']
        if not self:
            self = self.env['property.search.profile'].search([])
        for rec in self:
            args = [
                    #('property_type_id', '=', rec.property_type_id.id),
                    ('living_space', '>=', rec.min_living_space),
                    ('living_space', '<=', rec.max_living_space)]

            if rec.property_type_id:
                args.extend([('property_type_id', '=', rec.property_type_id.id)])
            if rec.contract_type == 'buy':
                args.extend([('for_sale', '=', True), ('purchase_price', '<=', rec.max_price)])
            elif rec.contract_type == 'rent':
                args.extend([('for_rent', '=', True), ('rent_incl_heat', '<=', rec.max_price)])
            elif rec.contract_type in ('both', False):
                args.extend(['|', ('purchase_price', '<=', rec.max_price), ('rent_incl_heat', '<=', rec.max_price)])

            match_distance_property = self.env['property.distance'].search(
                [('partner_id', '=', rec.partner_id.id), ('distance', '<=', rec.max_distance)]).mapped('property_id')
            if match_distance_property:
                args.extend([('id', 'in', match_distance_property.ids)])
            property_ids = property_obj.search(args)
            if property_ids:
                rec.property_ids = property_ids.ids
            else:
                rec.property_ids = False
        return True

    def create_property_distance(self):
        all_property = self.env['property.property'].search([])
        customers = self.env['res.partner'].search([])
        for customer in customers:
            customer_property = self.env['property.distance'].search([('customer_id', '=', customer.id)]).mapped('property_id')
            missing_property = set(all_property) - set(customer_property)
            for property in missing_property:
                self.env['property.distance'].create({'property_id': property.id, 'customer_id': customer.id})

    def create_opportuniy(self):
        for rec in self.env['property.search.profile'].search([]):
            if rec.auto_marketing:
                partner_id = rec.partner_id
                for property_id in rec.property_ids:
                    price = 0
                    lead_found = self.env['crm.lead'].search([('partner_id', '=', partner_id.id), ('property_id', '=', property_id.id)])
                    if not lead_found:
                        if property_id.for_rent:
                            price = property_id.rent_incl_heat
                        elif property_id.for_sale:
                            price = property_id.purchase_price

                        self.env['crm.lead'].create({'name': property_id.name,
                                                     'planned_revenue': price,
                                                     'partner_id': partner_id.id,
                                                     'property_id': property_id.id,
                                                     'search_profile_id': rec.id,
                                                     'type': 'opportunity',
                                                     'stage_id': self.env.ref('property_management.stage_lead_interest_property').id
                                                     })


class ProeprtyDistance(models.Model):
    _name = 'property.distance'
    _description = 'Property Distance'

    partner_id = fields.Many2one('res.partner', string='Customer')
    property_id = fields.Many2one('property.property', 'Property')
    distance = fields.Float('Distance')

    def create_property_distance(self):
        all_property = self.env['property.property'].search([])
        customers = self.env['res.partner'].search([])
        for customer in customers:
            customer_property = self.env['property.distance'].search([('partner_id', '=', customer.id)]).mapped('property_id')
            missing_property = set(all_property) - set(customer_property)
            for property in missing_property:
                self.env['property.distance'].create({'property_id': property.id, 'partner_id': customer.id})

    def find_distance(self, customer, property):
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

    def map_distance(self):
        distance_rec = self.env['property.distance'].search([])
        for rec in distance_rec:
            distance = self.find_distance(rec.partner_id, rec.property_id)
            rec.distance = distance
