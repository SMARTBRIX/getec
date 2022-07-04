# -*- coding: utf-8 -*-

from odoo import models
from datetime import timedelta


class ExpenditureSplitCost(models.TransientModel):
    _name = 'expenditure.split.cost'
    _description = 'Expenditure Split Cost'

    def split_cost(self):
        expenditure_ids = self.env['property.expenditure'].browse(self.env.context.get('active_ids'))
        for rec in expenditure_ids:
            child_ids = rec.property_id.child_property_ids
            if not child_ids:
                child_ids = rec.property_id
            print("CHILDDDDDDDDDDD", child_ids)
            factor_property = 0
            total_child_living_space = sum(child_ids.mapped('living_space'))
            day_amount = round(rec.amount / (rec.date_end - rec.date_start).days, 5)
            # if rec.cost_type_id.allocation_formula == 'ls':
            #     factor_property = rec.property_id.living_space / sum(child_ids.mapped('living_space'))
            if rec.cost_type_id.allocation_formula == 'ru':
                factor_property = 1 / len(child_ids)
            elif rec.cost_type_id.allocation_formula == 'da':
                factor_property = sum(rec.expenditure_factor_ids.mapped('factor'))
            print("FACTORRRR property", factor_property)
            st_date = rec.date_start
            end_date = rec.date_end

            child_property_tenancy_ids = self.env['property.tenancy'].search([('property_id', 'in', child_ids.ids)])
            tenancy_dict = dict.fromkeys(child_property_tenancy_ids.ids, 0.0)
            for tenancy in child_property_tenancy_ids:
                while st_date < end_date:
                    tenancy_ids = child_property_tenancy_ids.filtered(lambda x: x.date_start <= st_date and x.date_end >= st_date)
                    for t in tenancy_ids:
                        if rec.cost_type_id.allocation_formula == 'p':
                            all_tenancy_residents = 0
                            for tenancy in tenancy_ids:
                                all_tenancy_residents = all_tenancy_residents + len(tenancy.resident_ids)
                            factor_tenancy = len(t.resident_ids) / all_tenancy_residents
                        elif rec.cost_type_id.allocation_formula == 'ls':
                            factor_tenancy = t.property_id.living_space / total_child_living_space
                        else:
                            factor_tenancy = factor_property

                        if t.id not in tenancy_dict.keys():
                            tenancy_dict[t.id] = day_amount * factor_tenancy
                        else:
                            tenancy_dict[t.id] = tenancy_dict[t.id] + round((day_amount * factor_tenancy), 5)
                    print("ST DATEEEEE", st_date, tenancy_dict)
                    st_date = st_date + timedelta(days=1)

            for ten_value in tenancy_dict:
                tenancy = self.env['property.tenancy'].browse(ten_value)
                if rec.date_start < tenancy.date_start:
                    date_start = tenancy.date_start
                else:
                    date_start = rec.date_start

                if rec.date_end > tenancy.date_end:
                    date_end = tenancy.date_end
                else:
                    date_end = rec.date_end

                vals = {'expenditure_id': rec.id,
                        'tenancy_id': ten_value,
                        'cost_type_id': rec.cost_type_id.id,
                        'amount': tenancy_dict[ten_value],
                        'date_start': date_start,
                        'date_end': date_end,
                        'documents': rec.documents
                        }
                self.env['property.journal'].create(vals)

            rec.cleared = True

        return True
