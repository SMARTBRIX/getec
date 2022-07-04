# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class PortfolioReport(models.Model):
    _name = "portfolio.report"
    _description = "Portfolio Report"
    _auto = False
    _rec_name = 'property_id'

    property_id = fields.Many2one('property.property', readonly=True, string='Property')
    parent_property_id = fields.Many2one('property.property', readonly=True, string='Parent Property')
    available_from = fields.Date('Available From', readonly=True)
    property_type = fields.Many2one('property.category', readonly=True)
    property_active = fields.Integer(readonly=True)
    vacant = fields.Integer(readonly=True)
    under_renovation = fields.Integer(readonly=True)
    total_active = fields.Integer(readonly=True)
    planned = fields.Integer(readonly=True)
    total_planned = fields.Integer(readonly=True)

    def _query(self):
        query = """select pp.id as id, pp.id as property_id, pp.parent_property_id as parent_property_id,pp.property_type as property_type, pp.available_from as available_from,
                    (case when pp.available_from <= %s and pt.property_id = pp.id  and pt.date_start <= %s and pt.date_end >= %s and pt.type != 'vacancy' then 1 else 0 end) as property_active,
                    (case when pp.available_from <= %s and pt.property_id = pp.id  and pt.date_start <= %s and pt.date_end >= %s and pt.type = 'vacancy' then 1 else 0 end) as vacant,
                    (case when pp.available_from > %s and p.property_id = pp.id and p.date_start <= %s then 1 else 0 end) as under_renovation,
                    (case when pp.available_from <= %s or (pp.available_from > %s and p.property_id in (select property_id from project_property_rel where project_id = p.id) and p.date_start <= %s) then 1 else 0 end) as total_active,
                    (case when pp.available_from > %s and pp.purchase_date <= %s and p.property_id in (select property_id from project_property_rel where project_id = p.id) and p.date_start > %s then 1 else 0 end) as planned,
                    (case when pp.available_from <= %s or (pp.available_from > %s and pp.purchase_date <= %s and p.property_id in (select property_id from project_property_rel where project_id = p.id)) then 1 else 0 end) as total_planned
                    from property_property pp
                    left join property_tenancy pt on (pt.property_id = pp.id)
                    left join project_project p on (p.property_id = pp.id)
                    left join project_property_rel ppr on (ppr.property_id = pp.id)"""
        return query

    def init(self):
        context = self.env.context.copy()
        date = context.get('date')
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self.with_context()._query()), (date, date, date, date, date, date, date, date, date, date, date, date, date, date, date, date, date))
