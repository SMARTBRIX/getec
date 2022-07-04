# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PropertyRent(models.Model):
    _name = 'property.rent'
    _description = 'Rent'
    _rec_name = 'tenancy_id'

    def select_day(self):
        lst = []
        for i in range(1, 29):
            lst.append((str(i), str(i)))
        return lst

    @api.model
    def default_get(self, vals):
        res = super(PropertyRent, self).default_get(vals)
        context = self.env.context.copy()
        if context.get('property_id'):
            property_id = self.env['property.property'].browse(context['property_id'])
            res['rent'] = property_id.rent_price
            res['space'] = property_id.living_space
            res['heating_space'] = property_id.heating_space
            res['co_owenership'] = property_id.co_owenership
            res['ancillary_costs'] = property_id.ancillary_costs
        if context.get('resident_ids') and context.get('resident_ids')[0]:
            res['persons'] = len(context.get('resident_ids')[0][2])
        res['day_of_invoice'] = "1"
        res['billing_period'] = 'monthly'
        return res

    tenancy_id = fields.Many2one('property.tenancy', string="Tenancy")
    rent = fields.Float()
    heating_costs = fields.Float("Heating Costs")
    ancillary_costs = fields.Float("Ancillary Costs")
    # combined_costs = fields.Float("Combined")
    # advance_payment = fields.Float("Advance Payment")
    # flatrate_rent = fields.Float("Flatrate Rent")
    date_start = fields.Date("Start Date")
    billing_type = fields.Selection([('separate', 'Separate advance payments for ancillary costs and heating'), (
        'combined', 'Combined advance payment for all ancillary costs'), ('flatrate', 'Flatrate Rent')], string="Billing Type", related="tenancy_id.billing_type")
    billing_period = fields.Selection(
        [('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('yearly', 'Yearly')], string="Billing Period")
    day_of_invoice = fields.Selection(selection=select_day)
    persons = fields.Integer("Persons")
    space = fields.Float("Space")
    heating_space = fields.Float("Heating Space")
    co_owenership = fields.Integer(string='Co-Ownership')
