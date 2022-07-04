# -*- coding: utf-8 -*-

from odoo import models
from datetime import date


class BusinessExpenditureSplitCost(models.TransientModel):
    _name = 'business.expenditure.split.cost'
    _description = 'BusinessPlan Expenditure Split Cost'

    def split_cost(self):
        expenditure_ids = self.env['businessplan.expenditure'].browse(self.env.context.get('active_ids'))
        for rec in expenditure_ids:
            child_ids = rec.property_id.child_property_ids
            if not child_ids:
                child_ids = rec.property_id
            current_date = date.today()
            amount_per_day = round(rec.amount / ((rec.date_end - rec.date_start).days + 1), 5)
            child_property_tenancy_ids = self.env['property.tenancy'].search([('property_id', 'in', child_ids.ids),
                                                                              ('date_start', '<=', current_date),
                                                                              ('date_end', '>=', current_date)])
            tenancy_dict = dict.fromkeys(child_property_tenancy_ids.ids, 0.0)
            for tenancy in child_property_tenancy_ids:
                reference = 0
                amount = 0
                tenancy_ids = child_property_tenancy_ids.filtered(lambda x: x.date_start <= current_date and x.date_end >= current_date)
                sum_living_space = 0
                sum_heating_space = 0
                sum_persons = 0
                sum_co_ownership = 0
                sum_residential_units = 0
                for t in tenancy_ids:
                    rent = self.env['property.rent'].search([('tenancy_id', '=', t.id), ('date_start', '<=', current_date)], order='date_start desc', limit=1)
                    sum_living_space += rent.space
                    sum_heating_space += rent.heating_space
                    sum_persons += rent.persons
                    sum_co_ownership += rent.co_owenership
                    sum_residential_units += 1

                    if rec.cost_type_id.allocation_formula == 'ls':
                        reference += sum_living_space
                    if rec.cost_type_id.allocation_formula == 'hs':
                        reference += sum_heating_space
                    if rec.cost_type_id.allocation_formula == 'p':
                        reference += sum_persons
                    if rec.cost_type_id.allocation_formula == 'co':
                        reference += sum_co_ownership
                    if rec.cost_type_id.allocation_formula == 'ru':
                        reference += sum_residential_units

                    if tenancy in tenancy_ids:
                        rent = self.env['property.rent'].search([('tenancy_id', '=', t.id), ('date_start', '<=', current_date)], order='date_start desc', limit=1)
                        if rec.cost_type_id.allocation_formula == 'ls':
                            factor_tenancy = rent.space / sum_living_space
                        if rec.cost_type_id.allocation_formula == 'hs':
                            factor_tenancy = rent.heating_space / sum_heating_space
                        if rec.cost_type_id.allocation_formula == 'p':
                            factor_tenancy = rent.persons / sum_persons
                        if rec.cost_type_id.allocation_formula == 'co':
                            factor_tenancy = rent.co_owenership / sum_co_ownership
                        if rec.cost_type_id.allocation_formula == 'ru':
                            factor_tenancy = 1 / sum_residential_units
                        if rec.cost_type_id.allocation_formula == 'da':
                            factor_tenancy = rec.factor_of_this_property

                        amount_tenancy_day = amount_per_day * factor_tenancy
                        amount += amount_tenancy_day

                tenancy_dict[tenancy.id] = amount

                vals = {'expenditure_id': rec.id,
                        'tenancy_id': tenancy.id,
                        'cost_type_id': rec.cost_type_id.id,
                        'amount': rec.amount,
                        'tax_id': rec.tax_id.id,
                        'date_start': rec.date_start,
                        'date_end': rec.date_end,
                        'documents': rec.documents
                        }
                self.env['businessplan.journal'].create(vals)

            rec.cleared = True
        return True
