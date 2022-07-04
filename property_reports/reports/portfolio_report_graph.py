# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import fields, models
import datetime


class PortfolioReportGraph(models.Model):
    _name = "portfolio.report.graph"
    _description = "Portfolio Report Graph"
    _auto = False
    _rec_name = 'property_id'

    property_id = fields.Many2one('property.property', string='Property')
    available_from = fields.Date('Available From')
    property_type = fields.Many2one('property.category', readonly=True)
    property_active = fields.Integer()
    vacant = fields.Integer()
    under_renovation = fields.Integer()
    total_active = fields.Integer()
    planned = fields.Integer()
    total_planned = fields.Integer()
    start_date = fields.Date()

    def _query(self):
        context = self.env.context.copy()
        if context.get('start_year') and context.get('end_year'):
            # total_months = (context.get('end_year') - context.get('start_year')) * 12 + 12
            total_year = (context.get('end_year') - context.get('start_year')) + 1
            # m = 1
            y = context.get('start_year')
            final_query = ''
            for rec in range(0, total_year + 1):
                # if m > 12:
                # m = m % 12
                start_day = datetime.date(day=31, month=12, year=y - 1)
                query = """select pp.id as id, pp.id as property_id, pp.property_type as property_type, '%s' as start_date,
                        (case when pp.available_from <= '%s' and pt.property_id = pp.id  and pt.date_start <= '%s' and pt.date_end >= '%s' and pt.type != 'vacancy' then 1 end) as property_active,
                        (case when pp.available_from <= '%s' and pt.property_id = pp.id  and pt.date_start <= '%s' and pt.date_end >= '%s' and pt.type = 'vacancy' then 1 end) as vacant,
                        (case when pp.available_from > '%s' and p.property_id = pp.id and p.date_start <= '%s' then 1 end) as under_renovation,
                        (case when pp.available_from <= '%s' or (pp.available_from > '%s' and p.property_id in (select property_id from project_property_rel where project_id = p.id) and p.date_start <= '%s') then 1 end) as total_active,
                        (case when pp.available_from > '%s' and pp.purchase_date <= '%s' and p.property_id in (select property_id from project_property_rel where project_id = p.id) and p.date_start > '%s' then 1 end) as planned,
                        (case when pp.available_from <= '%s' or (pp.available_from > '%s' and pp.purchase_date <= '%s' and p.property_id in (select property_id from project_property_rel where project_id = p.id)) then 1 end) as total_planned
                        from property_property pp
                        left join property_tenancy pt on (pt.property_id = pp.id)
                        left join project_project p on (p.property_id = pp.id)
                        left join project_property_rel ppr on (ppr.property_id = pp.id)""" % (start_day, start_day, start_day, start_day, start_day, start_day, start_day, start_day, start_day, start_day, start_day, start_day, start_day, start_day, start_day, start_day, start_day, start_day)
                y = y + 1
                final_query = final_query + query + " union "
            return final_query[:-7]

    def init(self):
        if self.env.context.get('start_year'):
            tools.drop_view_if_exists(self.env.cr, self._table)
            self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self.with_context()._query()))
